# Generated by Django 4.0.6 on 2022-07-30 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0006_remove_recipe_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='tag',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='recipe.tag'),
        ),
    ]
