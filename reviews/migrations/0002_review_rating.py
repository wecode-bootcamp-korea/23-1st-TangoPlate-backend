# Generated by Django 3.2.6 on 2021-08-09 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
