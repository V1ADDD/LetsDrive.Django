# Generated by Django 4.1.3 on 2022-12-13 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_users_form1'),
    ]

    operations = [
        migrations.CreateModel(
            name='Drives',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.FloatField()),
                ('time_start', models.DateTimeField()),
                ('time_finish', models.DateTimeField()),
                ('price', models.FloatField()),
                ('auto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.auto')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.users')),
            ],
        ),
        migrations.DeleteModel(
            name='Users_Form1',
        ),
    ]
