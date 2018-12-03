# Generated by Django 2.1.1 on 2018-11-26 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20181118_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='matched',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='_user_matched_+', to='users.User'),
        ),
    ]
