# Generated by Django 4.0.3 on 2022-03-25 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='descripiton2',
            field=models.TextField(blank=True, max_length=255),
        ),
    ]
