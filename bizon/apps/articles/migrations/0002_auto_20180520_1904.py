# Generated by Django 2.0.4 on 2018-05-20 16:04

from django.db import migrations, models
import django.db.models.deletion
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', sorl.thumbnail.fields.ImageField(upload_to='gallery', verbose_name='изображение')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
                ('author', models.CharField(blank=True, max_length=254, verbose_name='автор')),
            ],
            options={
                'verbose_name_plural': 'изображения',
                'verbose_name': 'изображение',
            },
        ),
        migrations.AlterField(
            model_name='article',
            name='template_name',
            field=models.CharField(choices=[('articles/articles_template/branding.html', 'branding'), ('articles/articles_template/default.html', 'default')], default='articles/articles_template/default.html', max_length=254, verbose_name='шаблон'),
        ),
        migrations.AddField(
            model_name='photo',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery', to='articles.Article', verbose_name='статья'),
        ),
    ]
