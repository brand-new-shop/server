# Generated by Django 4.1.4 on 2023-01-04 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0002_replytoticket_created_at_alter_replytoticket_answer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='replytoticket',
            options={'verbose_name': 'reply', 'verbose_name_plural': 'replies'},
        ),
        migrations.AlterField(
            model_name='replytoticket',
            name='answer',
            field=models.TextField(blank=True, max_length=4096, null=True),
        ),
        migrations.AlterField(
            model_name='replytoticket',
            name='issue',
            field=models.TextField(max_length=4096),
        ),
    ]