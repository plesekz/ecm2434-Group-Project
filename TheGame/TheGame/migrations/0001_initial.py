# Generated by Django 4.0.3 on 2022-03-18 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('Login', '0004_merge_20220227_1644'),
    ]

    operations = [
        migrations.CreateModel(
            name='Champion',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('pHealth', models.PositiveIntegerField(default=100)),
                ('pToughness', models.PositiveIntegerField(default=1)),
                ('pEvasion', models.PositiveIntegerField(default=0)),
                ('damage', models.PositiveIntegerField(default=1)),
                ('accuracy', models.PositiveIntegerField(default=1)),
                ('attackSpeed', models.PositiveIntegerField(default=1)),
                ('aHealth', models.PositiveIntegerField(default=0)),
                ('aToughness', models.PositiveIntegerField(default=0)),
                ('aEvasion', models.PositiveIntegerField(default=0)),
                ('player',
                 models.ForeignKey(null=True,
                                   on_delete=django.db.models.deletion.CASCADE,
                                   to='Login.player')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('polymorphic_ctype',
                 models.ForeignKey(editable=False,
                                   null=True,
                                   on_delete=django.db.models.deletion.CASCADE,
                                   related_name='polymorphic_%(app_label)s.%(class)s_set+',
                                   to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='BaseItem',
            fields=[
                ('item_ptr',
                 models.OneToOneField(auto_created=True,
                                      on_delete=django.db.models.deletion.CASCADE,
                                      parent_link=True,
                                      primary_key=True,
                                      serialize=False,
                                      to='TheGame.item')),
                ('armourValue', models.IntegerField()),
                ('vitalityBoost', models.IntegerField()),
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
                ('item_ptr',
                 models.OneToOneField(auto_created=True,
                                      on_delete=django.db.models.deletion.CASCADE,
                                      parent_link=True,
                                      primary_key=True,
                                      serialize=False,
                                      to='TheGame.item')),
                ('damageNumber', models.IntegerField()),
                ('damageInstances', models.IntegerField()),
                ('range', models.IntegerField()),
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
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('champion', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='TheGame.champion')),
                ('item', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='TheGame.item')),
            ],
        ),
        migrations.CreateModel(
            name='SpecificItem',
            fields=[
                ('baseitem_ptr',
                 models.OneToOneField(auto_created=True,
                                      on_delete=django.db.models.deletion.CASCADE,
                                      parent_link=True,
                                      primary_key=True,
                                      serialize=False,
                                      to='TheGame.baseitem')),
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
                ('baseweapon_ptr',
                 models.OneToOneField(auto_created=True,
                                      on_delete=django.db.models.deletion.CASCADE,
                                      parent_link=True,
                                      primary_key=True,
                                      serialize=False,
                                      to='TheGame.baseweapon')),
                ('level', models.IntegerField()),
                ('glory', models.IntegerField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('TheGame.baseweapon',),
        ),
    ]
