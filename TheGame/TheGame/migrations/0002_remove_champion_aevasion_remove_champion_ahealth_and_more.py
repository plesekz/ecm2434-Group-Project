# Generated by Django 4.0.3 on 2022-03-18 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TheGame', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='champion',
            name='aEvasion',
        ),
        migrations.RemoveField(
            model_name='champion',
            name='aHealth',
        ),
        migrations.RemoveField(
            model_name='champion',
            name='aToughness',
        ),
        migrations.RemoveField(
            model_name='champion',
            name='accuracy',
        ),
        migrations.RemoveField(
            model_name='champion',
            name='attackSpeed',
        ),
        migrations.RemoveField(
            model_name='champion',
            name='damage',
        ),
        migrations.RemoveField(
            model_name='champion',
            name='pEvasion',
        ),
        migrations.RemoveField(
            model_name='champion',
            name='pToughness',
        ),
        migrations.RemoveField(
            model_name='championitems',
            name='amount',
        ),
        migrations.AddField(
            model_name='baseweapon',
            name='associated',
            field=models.CharField(default='d', max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='champion',
            name='armour',
            field=models.ForeignKey(
                default=2,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='armour',
                to='TheGame.specificitem'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='champion',
            name='auxItem1',
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='aux1',
                to='TheGame.specificitem'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='champion',
            name='auxItem2',
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='aux2',
                to='TheGame.specificitem'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='champion',
            name='auxItem3',
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='aux3',
                to='TheGame.specificitem'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='champion',
            name='pAthletics',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='champion',
            name='pBrain',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='champion',
            name='pControl',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='champion',
            name='primaryWeapon',
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='pWeapon',
                to='TheGame.specificweapon'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='champion',
            name='secondaryWeapon',
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='sWeapon',
                to='TheGame.specificweapon'),
            preserve_default=False,
        ),
    ]
