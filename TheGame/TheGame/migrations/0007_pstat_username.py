# Generated by Django 4.0.2 on 2022-03-01 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TheGame', '0006_rename_pstats_pstat'),
    ]

    operations = [
        migrations.AddField(
            model_name='pstat',
            name='username',
            field=models.CharField(default='aaa', max_length=50),
            preserve_default=False,
        ),
    ]