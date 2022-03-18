# Generated by Django 4.0.2 on 2022-03-17 21:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TheGame', '0010_champion_delete_pstat'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('type', models.CharField(max_length=32)),
                ('Stat1', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='ChampionItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('itemLevel', models.IntegerField()),
                ('champion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='TheGame.champion')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='TheGame.item')),
            ],
        ),
    ]
