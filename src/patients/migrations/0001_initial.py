# Generated by Django 5.1.7 on 2025-04-13 22:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TemporaryPatient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10)),
                ('age_range', models.CharField(choices=[('05-15', '05-15 ans'), ('16-25', '16-25 ans'), ('26-35', '26-35 ans'), ('36-45', '36-45 ans'), ('46+', '46 ans et plus')], max_length=10)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('height', models.FloatField(blank=True, null=True)),
                ('diabetes_type', models.CharField(choices=[('Type 1', 'Type 1'), ('Type 2', 'Type 2'), ('Gestational', 'Gestational'), ('Pre-diabetes', 'Pre-diabetes')], max_length=20)),
                ('fasting_glucose', models.FloatField(blank=True, null=True)),
                ('postprandial_glucose', models.FloatField(blank=True, null=True)),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10)),
                ('age_range', models.CharField(choices=[('05-15', '05-15 ans'), ('16-25', '16-25 ans'), ('26-35', '26-35 ans'), ('36-45', '36-45 ans'), ('46+', '46 ans et plus')], max_length=10)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('height', models.FloatField(blank=True, null=True)),
                ('imc', models.FloatField(blank=True, null=True)),
                ('diabetes_type', models.CharField(choices=[('Type 1', 'Type 1'), ('Type 2', 'Type 2'), ('Gestational', 'Gestational'), ('Pre-diabetes', 'Pre-diabetes')], max_length=20)),
                ('fasting_glucose', models.FloatField(blank=True, null=True)),
                ('postprandial_glucose', models.FloatField(blank=True, null=True)),
                ('hypertension', models.BooleanField(default=False)),
                ('dyslipidemia', models.BooleanField(default=False)),
                ('kidney_disease', models.BooleanField(default=False)),
                ('obesity', models.BooleanField(default=False)),
                ('complications', models.JSONField(default=dict)),
                ('completed', models.BooleanField(default=False)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patient', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
