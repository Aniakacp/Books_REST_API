# Generated by Django 2.2.24 on 2021-09-03 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_auto_20210903_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='published_date',
            field=models.CharField(max_length=10),
        ),
    ]
