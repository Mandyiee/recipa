# Generated by Django 4.0.6 on 2022-08-01 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0008_remove_recipe_tag_recipe_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]