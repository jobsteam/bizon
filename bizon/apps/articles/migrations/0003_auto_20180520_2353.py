# Generated by Django 2.0.4 on 2018-05-20 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20180520_1904'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='title',
            field=models.CharField(blank=True, max_length=254, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='article',
            name='template_name',
            field=models.CharField(choices=[('articles/articles_template/fullpage.html', 'fullpage'), ('articles/articles_template/default.html', 'default'), ('articles/articles_template/branding.html', 'branding')], default='articles/articles_template/default.html', max_length=254, verbose_name='шаблон'),
        ),
    ]
