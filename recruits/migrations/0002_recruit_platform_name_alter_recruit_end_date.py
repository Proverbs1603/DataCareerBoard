# Generated by Django 5.1.2 on 2024-10-15 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruits', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recruit',
            name='platform_name',
            field=models.CharField(default='saramin', max_length=50, verbose_name='가져온 플랫폼 이름'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recruit',
            name='end_date',
            field=models.CharField(default='수시채용', max_length=11, verbose_name='마감일'),
        ),
    ]