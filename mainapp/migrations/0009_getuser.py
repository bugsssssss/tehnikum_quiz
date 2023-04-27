# Generated by Django 4.2 on 2023-04-27 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_userdetail'),
    ]

    operations = [
        migrations.CreateModel(
            name='GetUser',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='user_id')),
                ('username', models.CharField(max_length=255)),
                ('category_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.category')),
                ('questions', models.ManyToManyField(to='mainapp.question')),
                ('selected_answer', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='mainapp.answer')),
            ],
        ),
    ]
