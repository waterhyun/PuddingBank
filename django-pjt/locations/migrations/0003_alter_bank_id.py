# Generated by Django 4.2.16 on 2024-11-21 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_alter_bank_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
