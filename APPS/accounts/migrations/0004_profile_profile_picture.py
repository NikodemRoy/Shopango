# Generated by Django 4.0.4 on 2022-05-23 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(default='default.png', upload_to='user_profiles'),
        ),
    ]
