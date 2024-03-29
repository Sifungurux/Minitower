# Generated by Django 3.1.1 on 2020-09-10 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Host Name')),
                ('ip', models.CharField(max_length=12, verbose_name='IP Address')),
                ('description', models.TextField(max_length=120, verbose_name='Give short description')),
                ('cores', models.IntegerField(verbose_name='Number of cores')),
                ('ram', models.IntegerField(verbose_name='Amount of memory in Giga')),
                ('storage', models.IntegerField(verbose_name='Total space in Giga')),
            ],
        ),
    ]
