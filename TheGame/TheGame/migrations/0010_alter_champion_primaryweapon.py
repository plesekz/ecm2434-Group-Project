# Generated by Django 4.0.3 on 2022-03-22 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TheGame', '0009_alter_item_sprite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='champion',
            name='primaryWeapon',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='pWeapon', to='TheGame.specificweapon'),
            preserve_default=False,
        ),
    ]