# Generated by Django 3.1.3 on 2020-12-26 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_boughtitem_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boughtitem',
            name='time',
        ),
    ]