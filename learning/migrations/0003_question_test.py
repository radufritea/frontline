# Generated by Django 4.0.5 on 2022-07-16 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0002_remove_textobject_chapter_remove_videoobject_chapter_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]