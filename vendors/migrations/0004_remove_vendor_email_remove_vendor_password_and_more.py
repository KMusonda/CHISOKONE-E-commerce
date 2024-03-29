# Generated by Django 4.1.5 on 2023-03-13 15:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vendors', '0003_remove_vendor_created_by_alter_vendor_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='email',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='password',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='phone',
        ),
        migrations.AddField(
            model_name='vendor',
            name='created_by',
            field=models.OneToOneField(default=True, on_delete=django.db.models.deletion.CASCADE, related_name='vendor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
