# Generated by Django 4.0.3 on 2023-05-10 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bus', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='nos',
            field=models.IntegerField(default=0),
        ),
    ]
