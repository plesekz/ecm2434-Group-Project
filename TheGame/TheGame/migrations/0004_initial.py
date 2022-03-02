# Generated by Django 4.0.2 on 2022-03-01 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('TheGame', '0003_delete_player'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pHealth', models.PositiveIntegerField(default=0)),
                ('pToughness', models.PositiveIntegerField(default=0)),
                ('pEvasion', models.PositiveIntegerField(default=0)),
                ('damage', models.PositiveIntegerField(default=0)),
                ('accuracy', models.PositiveIntegerField(default=0)),
                ('attackSpeed', models.PositiveIntegerField(default=0)),
                ('aHealth', models.PositiveIntegerField(default=0)),
                ('aToughness', models.PositiveIntegerField(default=0)),
                ('aEvasion', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
