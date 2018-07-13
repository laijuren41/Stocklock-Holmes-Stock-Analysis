# Generated by Django 2.0.1 on 2018-05-29 00:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0007_auto_20180529_0021'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPortfolio',
            fields=[
                ('portfolio_id', models.AutoField(primary_key=True, serialize=False)),
                ('symbols', models.CharField(default='', max_length=100)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('portfolio_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.StockCompany')),
            ],
        ),
    ]
