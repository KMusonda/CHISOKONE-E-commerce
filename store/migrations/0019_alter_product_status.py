# Generated by Django 4.1.5 on 2023-02-15 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_alter_category_slug_alter_product_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('True', 'True'), ('False', 'False'), ('DELETED', 'deleted'), ('DRAFT', 'draft'), ('ACTIVE', 'Active')], default='active', max_length=10),
        ),
    ]
