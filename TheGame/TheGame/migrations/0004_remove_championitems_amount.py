# Generated by Django 4.0.3 on 2022-03-19 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TheGame', '0003_championitems_amount_championitems_itemlevel_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='championitems',
            name='amount',
        ),
    ]
