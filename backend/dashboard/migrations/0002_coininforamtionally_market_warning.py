# Generated by Django 4.1.2 on 2022-11-07 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coininforamtionally',
            name='market_warning',
            field=models.CharField(default=1, max_length=15),
            preserve_default=False,
        ),
    ]