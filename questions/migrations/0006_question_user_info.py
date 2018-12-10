from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0005_auto_20181031_0939'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='user_info',
            field=models.CharField(default='', max_length=300),
            preserve_default=False,
        ),
    ]