# Generated by Django 4.0.2 on 2022-02-27 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0002_player_userid'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='role',
            field=models.CharField(default='user', max_length=16),
            preserve_default=False,
        ),
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
