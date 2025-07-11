# Generated by Django 5.2.1 on 2025-05-31 14:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_grade'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GradeOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')),
                ('name', models.CharField(max_length=100, verbose_name="Nom de l'option")),
                ('abbreviation', models.CharField(blank=True, max_length=20, verbose_name='Abréviation')),
                ('order', models.PositiveSmallIntegerField(help_text='Numéro pour organiser les options', verbose_name='Ordre')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Créé par')),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='core.grade', verbose_name='Cycle')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL, verbose_name='Modifié par')),
            ],
            options={
                'verbose_name': 'Option du cycle',
                'verbose_name_plural': 'Options des cycles',
                'ordering': ['grade', 'order'],
                'unique_together': {('grade', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')),
                ('name', models.CharField(max_length=100, verbose_name='Nom du niveau')),
                ('abbreviation', models.CharField(blank=True, max_length=20, verbose_name='Abréviation')),
                ('order', models.PositiveSmallIntegerField(help_text='Numéro pour organiser les niveaux', verbose_name='Ordre')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Créé par')),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='levels', to='core.grade', verbose_name='Cycle')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL, verbose_name='Modifié par')),
            ],
            options={
                'verbose_name': 'Niveau',
                'verbose_name_plural': 'Niveaux',
                'ordering': ['grade', 'order'],
                'unique_together': {('grade', 'name')},
            },
        ),
    ]
