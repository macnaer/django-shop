# Generated by Django 4.2.2 on 2023-06-29 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order_basket',
            name='product',
        ),
        migrations.RemoveField(
            model_name='order_basket',
            name='user',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='Order_basket',
        ),
    ]
