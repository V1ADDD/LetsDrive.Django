# Generated by Django 4.1.3 on 2022-12-16 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_tarify_time_limit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarify',
            name='time_limit',
            field=models.IntegerField(),
        ),
    ]
