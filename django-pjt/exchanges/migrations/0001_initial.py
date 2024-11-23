# Generated by Django 4.2.16 on 2024-11-23 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.IntegerField()),
                ('cur_unit', models.CharField(max_length=10)),
                ('cur_nm', models.CharField(max_length=100)),
                ('ttb', models.FloatField(blank=True, null=True)),
                ('tts', models.FloatField(blank=True, null=True)),
                ('deal_bas_r', models.FloatField(blank=True, null=True)),
                ('bkpr', models.FloatField(blank=True, null=True)),
                ('yy_efee_r', models.FloatField(blank=True, null=True)),
                ('ten_dd_efee_r', models.FloatField(blank=True, null=True)),
                ('kftc_bkpr', models.FloatField(blank=True, null=True)),
                ('kftc_deal_bas_r', models.FloatField(blank=True, null=True)),
                ('update_date', models.DateField()),
            ],
            options={
                'db_table': 'exchanges',
            },
        ),
    ]
