# Generated by Django 2.1.1 on 2018-12-04 11:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=300, unique=True)),
                ('first_name', models.CharField(max_length=30, null=True)),
                ('last_name', models.CharField(max_length=30, null=True)),
                ('direct_manager', models.CharField(max_length=30, null=True)),
                ('years_of_experience', models.IntegerField(null=True)),
                ('years_within_organization', models.IntegerField(null=True)),
                ('years_in_role', models.IntegerField(null=True)),
                ('study_field', models.CharField(max_length=30, null=True)),
                ('is_mentor', models.BooleanField(default=False)),
                ('work_location', models.CharField(max_length=30, null=True)),
                ('position', models.CharField(max_length=30, null=True)),
                ('departement', models.CharField(max_length=30, null=True)),
            ],
        ),
    ]
