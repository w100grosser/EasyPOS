# Generated by Django 3.2.10 on 2021-12-07 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POS', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]