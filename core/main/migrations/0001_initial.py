# Generated by Django 5.1.4 on 2025-03-13 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text1', models.CharField(max_length=100, verbose_name='Slider text1')),
                ('text2', models.CharField(max_length=100, verbose_name='Slider text2')),
                ('image', models.ImageField(upload_to='slider', verbose_name='Slider image')),
            ],
        ),
    ]
