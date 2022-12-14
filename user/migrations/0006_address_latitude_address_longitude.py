# Generated by Django 4.1.4 on 2022-12-27 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_users_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='longitude',
            field=models.DecimalField(decimal_places=9, max_digits=9, null=True),
        ),
    ]
