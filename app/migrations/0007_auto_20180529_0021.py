# Generated by Django 2.0.1 on 2018-05-29 00:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_portfolio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfolio',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='portfolio_info',
        ),
        migrations.DeleteModel(
            name='Portfolio',
        ),
    ]
