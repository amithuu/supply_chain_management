# Generated by Django 3.2.25 on 2024-07-04 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supply', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='Customer',
            new_name='customer',
        ),
    ]