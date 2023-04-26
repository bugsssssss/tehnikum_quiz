# Generated by Django 4.2 on 2023-04-26 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_tempuser_alter_question_answers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Type', to='mainapp.questiontype'),
        ),
        migrations.CreateModel(
            name='UserAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.answer')),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Question', to='mainapp.question')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='User', to='mainapp.botusers')),
            ],
        ),
    ]
