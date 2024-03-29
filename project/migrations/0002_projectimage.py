# Generated by Django 4.2.8 on 2024-01-22 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='projects/')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='project.project')),
            ],
        ),
    ]
