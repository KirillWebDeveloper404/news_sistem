# Generated by Django 3.2.8 on 2022-09-05 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0003_auto_20220905_2038'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tema',
            options={'verbose_name': 'Тематика', 'verbose_name_plural': 'Тематика'},
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(blank=True, choices=[('m', 'Муж'), ('w', 'Жен')], max_length=10, null=True, verbose_name='Пол'),
        ),
        migrations.RemoveField(
            model_name='user',
            name='tema',
        ),
        migrations.AddField(
            model_name='user',
            name='tema',
            field=models.ManyToManyField(null=True, to='panel.Tema', verbose_name='Тематика(выбор)'),
        ),
    ]