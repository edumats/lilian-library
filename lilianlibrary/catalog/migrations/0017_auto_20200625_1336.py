# Generated by Django 3.0.7 on 2020-06-25 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_auto_20200625_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='google_id',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
