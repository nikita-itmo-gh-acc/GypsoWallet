# Generated by Django 4.2.2 on 2023-06-29 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0005_alter_token_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='count',
            field=models.FloatField(default=0),
        ),
    ]
