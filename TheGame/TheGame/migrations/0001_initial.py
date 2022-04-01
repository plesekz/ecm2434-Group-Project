# Generated by Django 4.0.2 on 2022-04-01 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('Login', '0001_initial'),
        ('Resources', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Champion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('sprite', models.CharField(default='hacker', max_length=50)),
                ('pHealth', models.PositiveIntegerField(default=100)),
                ('pAthletics', models.PositiveIntegerField(default=1)),
                ('pBrain', models.PositiveIntegerField(default=1)),
                ('pControl', models.PositiveIntegerField(default=1)),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Login.player')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('sprite', models.CharField(default='shiv', max_length=50)),
                ('price1', models.IntegerField()),
                ('price2', models.IntegerField(null=True)),
                ('price3', models.IntegerField(null=True)),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_%(app_label)s.%(class)s_set+', to='contenttypes.contenttype')),
                ('priceRes1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='priceRes1', to='Resources.resource')),
                ('priceRes2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='priceRes2', to='Resources.resource')),
                ('priceRes3', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='priceRes3', to='Resources.resource')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='BaseItem',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='TheGame.item')),
                ('armourValue', models.IntegerField()),
                ('vitalityBoost', models.IntegerField()),
                ('shieldValue', models.IntegerField()),
                ('specialAbilities', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('TheGame.item',),
        ),
        migrations.CreateModel(
            name='BaseWeapon',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='TheGame.item')),
                ('damageNumber', models.IntegerField()),
                ('damageInstances', models.IntegerField()),
                ('range', models.IntegerField()),
                ('associated', models.CharField(max_length=1)),
                ('ap_cost', models.IntegerField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('TheGame.item',),
        ),
        migrations.CreateModel(
            name='ChampionItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('champion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TheGame.champion')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TheGame.item')),
            ],
        ),
        migrations.CreateModel(
            name='SpecificItem',
            fields=[
                ('baseitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='TheGame.baseitem')),
                ('level', models.IntegerField()),
                ('glory', models.IntegerField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('TheGame.baseitem',),
        ),
        migrations.CreateModel(
            name='SpecificWeapon',
            fields=[
                ('baseweapon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='TheGame.baseweapon')),
                ('level', models.IntegerField()),
                ('glory', models.IntegerField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('TheGame.baseweapon',),
        ),
        migrations.AddField(
            model_name='champion',
            name='armour',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='armour', to='TheGame.specificitem'),
        ),
        migrations.AddField(
            model_name='champion',
            name='auxItem1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='aux1', to='TheGame.specificitem'),
        ),
        migrations.AddField(
            model_name='champion',
            name='auxItem2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='aux2', to='TheGame.specificitem'),
        ),
        migrations.AddField(
            model_name='champion',
            name='auxItem3',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='aux3', to='TheGame.specificitem'),
        ),
        migrations.AddField(
            model_name='champion',
            name='primaryWeapon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pWeapon', to='TheGame.specificweapon'),
        ),
        migrations.AddField(
            model_name='champion',
            name='secondaryWeapon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sWeapon', to='TheGame.specificweapon'),
        ),
    ]
