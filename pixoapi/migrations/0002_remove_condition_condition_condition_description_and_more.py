# Generated by Django 5.0 on 2023-12-04 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pixoapi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='condition',
            name='condition',
        ),
        migrations.AddField(
            model_name='condition',
            name='description',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='condition',
            name='title',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
