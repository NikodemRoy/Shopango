# Generated by Django 4.0.3 on 2022-03-25 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=48, unique=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('descripiton', models.TextField(blank=True, max_length=255)),
                ('image', models.ImageField(blank=True, upload_to='categories_images')),
            ],
            options={
                'verbose_name': 'Ca',
                'verbose_name_plural': 'Category',
            },
        ),
    ]
