# Generated by Django 3.2.5 on 2024-05-25 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserAccount', '0004_profile_amount_to_pay'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='img',
            field=models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics/'),
        ),
    ]
