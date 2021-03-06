# Generated by Django 3.2.7 on 2021-09-23 04:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StoreType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_type', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Store Type',
                'verbose_name_plural': 'Store Types',
                'db_table': 'store_type',
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=200)),
                ('store_address', models.TextField()),
                ('store_city', models.CharField(max_length=50)),
                ('store_state', models.CharField(max_length=50)),
                ('store_zip', models.CharField(max_length=20)),
                ('store_phone', models.CharField(max_length=20)),
                ('store_latitude', models.CharField(default=None, max_length=20)),
                ('store_longitude', models.CharField(default=None, max_length=20)),
                ('store_type', models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='store.storetype')),
            ],
            options={
                'verbose_name': 'Store',
                'verbose_name_plural': 'Stores',
                'db_table': 'store',
            },
        ),
    ]
