# Generated by Django 2.2.3 on 2019-08-17 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20190817_1642'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deploy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='标题')),
                ('status', models.IntegerField(choices=[(1, '在线'), (2, '离线')], verbose_name='状态')),
            ],
        ),
    ]