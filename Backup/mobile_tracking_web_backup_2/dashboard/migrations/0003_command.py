# Generated by Django 2.2.6 on 2019-11-01 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_macro'),
    ]

    operations = [
        migrations.CreateModel(
            name='Command',
            fields=[
                ('truck_id', models.TextField(blank=True, null=True)),
                ('timestamp', models.IntegerField(blank=True, primary_key=True, serialize=False)),
                ('command_id', models.TextField(blank=True, null=True)),
                ('command', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'command',
                'managed': True,
            },
        ),
    ]
