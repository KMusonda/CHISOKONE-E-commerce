# Generated by Django 4.1.5 on 2023-01-27 21:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_images'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='images',
            options={'verbose_name': 'Images', 'verbose_name_plural': 'Images'},
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='images/'),
            preserve_default=False,
        ),
    ]
