# Generated by Django 2.2.24 on 2021-09-04 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0010_auto_20210904_0616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=500),
        ),
    ]
