# Generated by Django 4.0.5 on 2022-07-29 05:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0023_choice_alter_test_options_remove_question_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learning.test'),
        ),
        migrations.AlterField(
            model_name='testinstance',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learning.test'),
        ),
    ]