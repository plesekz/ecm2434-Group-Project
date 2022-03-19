# Generated by Django 4.0.3 on 2022-03-19 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TheGame', '0002_alter_item_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='championitems',
            name='amount',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='championitems',
            name='itemLevel',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='championitems',
            name='champion',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='TheGame.champion'),
        ),
        migrations.AlterField(
            model_name='championitems',
            name='item',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='TheGame.item'),
        ),
    ]