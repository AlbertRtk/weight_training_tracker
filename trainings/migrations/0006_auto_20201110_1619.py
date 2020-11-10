# Generated by Django 3.1.3 on 2020-11-10 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0005_auto_20201110_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='reps_s1',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='reps_s2',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='reps_s3',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='reps_s4',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='series',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='weight_def',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='weight_kg',
            field=models.FloatField(blank=True, null=True),
        ),
    ]