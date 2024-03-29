# Generated by Django 2.2.7 on 2019-11-19 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('airlines', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rank', models.IntegerField(blank=True, null=True)),
                ('name_eng', models.CharField(blank=True, max_length=40, null=True)),
                ('name_chn', models.CharField(blank=True, max_length=40, null=True)),
                ('province', models.CharField(blank=True, max_length=50, null=True)),
                ('longitude', models.TextField(blank=True, null=True)),
                ('latitude', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'city',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('flight_name', models.CharField(blank=True, max_length=60, null=True)),
                ('departure_city', models.CharField(blank=True, max_length=60, null=True)),
                ('arrival_city', models.CharField(blank=True, max_length=60, null=True)),
                ('departure_airport', models.CharField(blank=True, max_length=50, null=True)),
                ('departure_time', models.CharField(blank=True, max_length=40, null=True)),
                ('arrival_airport', models.CharField(blank=True, max_length=50, null=True)),
                ('arrival_time', models.CharField(blank=True, max_length=50, null=True)),
                ('price', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'flight',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('password', models.CharField(max_length=256)),
                ('c_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
