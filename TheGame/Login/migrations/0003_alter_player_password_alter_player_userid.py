# Generated by Django 4.0.2 on 2022-02-27 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0002_player_userid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='password',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='player',
            name='userID',
            field=models.CharField(max_length=64),
        ),
    ]
