# Generated by Django 4.0.6 on 2022-07-30 09:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, null=True)),
                ('id_user', models.IntegerField()),
                ('profileimg', models.ImageField(default='avatar.jpg', upload_to='profile_images')),
                ('phonenumber', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('twitter', models.CharField(blank=True, max_length=100, null=True)),
                ('instagram', models.CharField(blank=True, max_length=100, null=True)),
                ('facebook', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(default='r.jpg', upload_to='recipe_images')),
                ('video_url', models.URLField(blank=True, null=True)),
                ('tags', models.CharField(blank=True, max_length=200, null=True)),
                ('directions', models.JSONField(blank=True, null=True)),
                ('ingredients', models.JSONField(blank=True, null=True)),
                ('nutritions', models.JSONField(blank=True, null=True)),
                ('people', models.IntegerField(default=0)),
                ('cooktime', models.IntegerField(default=0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.profile')),
            ],
        ),
    ]
