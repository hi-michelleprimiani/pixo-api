# Generated by Django 5.0.1 on 2024-01-04 19:21

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_date', models.DateTimeField(blank=True, null=True)),
                ('paid', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Collectible',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('description', models.CharField(max_length=10000)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('material', models.CharField(max_length=300)),
                ('color', models.CharField(blank=True, max_length=300, null=True)),
                ('size', models.CharField(max_length=300)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_url', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_cart', to='pixoapi.cart')),
                ('collectible', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_in_cart', to='pixoapi.collectible')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(related_name='carts', through='pixoapi.CartItem', to='pixoapi.collectible'),
        ),
        migrations.CreateModel(
            name='CollectibleCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pixoapi.category')),
                ('collectible', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pixoapi.collectible')),
            ],
        ),
        migrations.AddField(
            model_name='collectible',
            name='categories',
            field=models.ManyToManyField(related_name='collectibles', through='pixoapi.CollectibleCategory', to='pixoapi.category'),
        ),
        migrations.CreateModel(
            name='ImageGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collectible', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_gallery', to='pixoapi.collectible')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_collection', to='pixoapi.image')),
            ],
        ),
        migrations.AddField(
            model_name='collectible',
            name='images',
            field=models.ManyToManyField(related_name='collectibles', through='pixoapi.ImageGallery', to='pixoapi.image'),
        ),
        migrations.CreateModel(
            name='PixoUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(blank=True, max_length=1000)),
                ('location', models.CharField(max_length=300)),
                ('img_url', models.URLField()),
                ('created_on', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pixo_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=10000)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incoming_message', to='pixoapi.pixouser')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_message', to='pixoapi.pixouser')),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collectible', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='pixoapi.collectible')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorited_by', to='pixoapi.pixouser')),
            ],
        ),
        migrations.AddField(
            model_name='collectible',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller_collectibles', to='pixoapi.pixouser'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carts', to='pixoapi.pixouser'),
        ),
        migrations.CreateModel(
            name='UserReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comment', models.CharField(max_length=500)),
                ('review_date', models.DateTimeField(auto_now_add=True)),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews_given', to='pixoapi.pixouser')),
                ('target_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews_received', to='pixoapi.pixouser')),
            ],
        ),
    ]
