# Generated by Django 3.1.3 on 2020-11-11 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0009_auto_20201111_0829'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='duration',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
