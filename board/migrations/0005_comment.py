# Generated by Django 4.0.1 on 2022-02-09 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_alter_post_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_contents', models.TextField(max_length=100, verbose_name='댓글작성')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='작성일')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='최종수정일')),
                ('connect', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='board.post')),
            ],
        ),
    ]