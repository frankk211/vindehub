# Generated by Django 4.2.1 on 2024-01-10 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0004_alter_item_image_2_alter_item_image_3_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image_2',
            field=models.ImageField(blank=True, default='item_images/default-image.png', null=True, upload_to='item_images'),
        ),
        migrations.AlterField(
            model_name='item',
            name='image_3',
            field=models.ImageField(blank=True, default='item_images/default-image.png', null=True, upload_to='item_images'),
        ),
        migrations.AlterField(
            model_name='item',
            name='image_4',
            field=models.ImageField(blank=True, default='item_images/default-image.png', null=True, upload_to='item_images'),
        ),
    ]
