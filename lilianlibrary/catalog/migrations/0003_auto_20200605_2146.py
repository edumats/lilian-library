# Generated by Django 3.0.3 on 2020-06-06 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20200605_2107'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='date_of_death',
            field=models.DateField(blank=True, null=True, verbose_name='Died'),
        ),
        migrations.AlterField(
            model_name='author',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]
