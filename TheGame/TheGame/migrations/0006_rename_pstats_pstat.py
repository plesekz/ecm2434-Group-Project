# Generated by Django 4.0.2 on 2022-03-01 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TheGame', '0005_rename_player_pstats'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='pStats',
            new_name='pStat',
        ),
    ]