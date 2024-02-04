from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login

from conversation.models import Conversation
from item.models import Category, Item, User

from django.contrib import messages
from django.contrib.auth import logout

from .forms import SignupForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    items = Item.objects.filter(is_sold=False).order_by('-created_at')
    categories = Category.objects.all()
    conversations = Conversation.objects.filter(members__in=[request.user.id])
    nr_conversatii = conversations.count()

    banner_closed_cookie = request.COOKIES.get('bannerClosed')
    if banner_closed_cookie and banner_closed_cookie.lower() == 'true':
        # Dacă bannerClosed este 'true', setăm o variabilă de ședință pentru a arăta că banner-ul ar trebui să fie ascuns
        request.session['show_banner'] = False
    else:
        # Altfel, setăm variabila de ședință pentru a arăta că banner-ul ar trebui să fie afișat
        request.session['show_banner'] = True

    user = request.user

    numbers_list = range(1, 1000)
    page = request.GET.get('page', 1)
    paginator = Paginator(numbers_list, 20)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)

    return render(request, 'core/index.html', {
        'show_banner': request.session.get('show_banner', True),
        'categories': categories,
        'items': items,
        'user': user,
        'numbers': numbers,
        'nr_conversatii': nr_conversatii
    })

def contact(request):
    return render(request, 'core/contact.html')

def loginViewTemp(request):

    if request.user.is_authenticated:
        messages.warning(request, "Esti deja autentificat")
       
        return redirect('core:index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        

        try:
            user = User.objects.get(username=username)

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Bine ai revenit, {user.username} !")
                next_url = request.GET.get("next", "core:index")
                print(next_url)
                return redirect(next_url)
            else:
                messages.error(request, 'Parolă incorectă. Reîncercați !')
        
        except:
            messages.error(request, 'Userul nu exista în baza noastră de date')

    return render(request, "core/login.html")

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })


def logout_view(request):
    user = request.user 
    logout(request)
    messages.success(request, f"Te-ai delogat cu succes. Așteptăm să te revedem curând, {user.username}")  # Mesajul adăugat pentru logout reușit
    return redirect('/')

def category(request, pk):
    category_name = get_object_or_404(Category, pk=pk)
    
    category_items = Item.objects.filter(category=category_name.id).order_by('-access_count')

    return render(request, 'core/category.html', {
        'category_name': category_name,
        'category_items': category_items,
    })
