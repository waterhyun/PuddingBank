# Generated by Django 4.2.16 on 2024-11-22 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_name', models.CharField(max_length=100)),
                ('address_name', models.CharField(max_length=200)),
                ('road_address_name', models.CharField(blank=True, max_length=200, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('place_url', models.URLField()),
                ('category_name', models.CharField(max_length=100)),
                ('category_group_code', models.CharField(max_length=10)),
                ('category_group_name', models.CharField(max_length=100)),
                ('x', models.DecimalField(decimal_places=16, max_digits=20)),
                ('y', models.DecimalField(decimal_places=16, max_digits=20)),
                ('distance', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'banks',
                'ordering': ['distance'],
            },
        ),
    ]
