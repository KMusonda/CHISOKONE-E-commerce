# Generated by Django 4.1.5 on 2023-03-05 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_remove_order_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('SHIPPED', 'shipped'), ('DELETED', 'deleted'), ('ACTIVE', 'Active')], default='active', max_length=10),
        ),
    ]
