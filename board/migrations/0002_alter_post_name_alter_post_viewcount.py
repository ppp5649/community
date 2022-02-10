# Generated by Django 4.0.1 on 2022-01-30 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='name',
            field=models.CharField(default='job', max_length=200, null=True, verbose_name='게시판명'),
        ),
        migrations.AlterField(
            model_name='post',
            name='viewCount',
            field=models.PositiveIntegerField(default=0, verbose_name='조회수'),
        ),
    ]