# Generated by Django 4.0.6 on 2022-08-01 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_delete_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='unit',
            new_name='measurement_unit',
        ),
    ]
