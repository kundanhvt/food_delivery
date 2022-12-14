# Generated by Django 4.1.3 on 2022-12-12 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reastaurant', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='image',
            field=models.ManyToManyField(to='reastaurant.image'),
        ),
        migrations.AlterField(
            model_name='food',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food_items', to='reastaurant.item'),
        ),
        migrations.AlterField(
            model_name='reastaurant',
            name='food',
            field=models.ManyToManyField(related_name='reastaurants_foods', to='reastaurant.food'),
        ),
        migrations.AlterField(
            model_name='reastaurant',
            name='image',
            field=models.ManyToManyField(related_name='reastaurant_image_name', to='reastaurant.image'),
        ),
    ]
