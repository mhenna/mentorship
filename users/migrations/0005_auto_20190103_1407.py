# Generated by Django 2.1.1 on 2019-01-03 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cycles', '0003_remove_cycle_skills'),
        ('users', '0004_auto_20181230_1841'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='skills',
        ),
        migrations.DeleteModel(
            name='Skill',
        ),
    ]
