# Generated by Django 3.0.6 on 2020-06-22 16:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20200622_1042'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="Enter the book's publisher", max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='author1',
            field=models.ManyToManyField(related_name='books', to='catalog.Author'),
        ),
        migrations.AddField(
            model_name='book',
            name='date_added_to_library',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(blank=True, help_text='Genre(s) of the book', related_name='books', to='catalog.Genre'),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Publisher'),
        ),
    ]
