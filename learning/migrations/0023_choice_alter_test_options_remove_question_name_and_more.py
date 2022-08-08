# Generated by Django 4.0.5 on 2022-07-29 05:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('learning', '0022_lecture_zip_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(default='', max_length=500)),
                ('position', models.IntegerField(verbose_name='position')),
                ('is_correct', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Choices',
                'ordering': ('position',),
            },
        ),
        migrations.AlterModelOptions(
            name='test',
            options={'ordering': ['date_created'], 'verbose_name_plural': 'Teste'},
        ),
        migrations.RemoveField(
            model_name='question',
            name='name',
        ),
        migrations.AddField(
            model_name='question',
            name='feedback',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='label',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='question',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='test',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='learning.test'),
        ),
        migrations.AddField(
            model_name='test',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='test',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='test',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='test',
            name='questions_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='test',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='test',
            name='name',
            field=models.CharField(max_length=150),
        ),
        migrations.CreateModel(
            name='UserChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learning.choice')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learning.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TestInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('completed', models.BooleanField(default=False)),
                ('date_finished', models.DateTimeField(auto_now_add=True)),
                ('test', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='learning.test')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='learning.question'),
        ),
        migrations.AlterUniqueTogether(
            name='choice',
            unique_together={('question', 'label'), ('question', 'position')},
        ),
    ]