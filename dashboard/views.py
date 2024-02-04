from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from item.models import Item
from conversation.models import Conversation

@login_required
def index(request):
    items = Item.objects.filter(created_by=request.user).order_by('-created_at')
    conversations = Conversation.objects.filter(members__in=[request.user.id])
    nr_conversatii = conversations.count()

    return render(request, 'dashboard/index.html', {
        'items': items,
        'nr_conversatii': nr_conversatii
    })
