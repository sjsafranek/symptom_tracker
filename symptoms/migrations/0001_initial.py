# Generated by Django 2.2.9 on 2020-02-19 22:16

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('agency_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('client_id', models.AutoField(primary_key=True, serialize=False)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=8)),
                ('age', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(150)])),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('session_id', models.AutoField(primary_key=True, serialize=False)),
                ('note', models.TextField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('agency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='symptoms.Agency')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='symptoms.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Therapist',
            fields=[
                ('therapist_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('agencies', models.ManyToManyField(blank=True, to='symptoms.Agency')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Symptom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('rank', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='symptoms.Session')),
            ],
        ),
        migrations.AddField(
            model_name='session',
            name='therapist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='symptoms.Therapist'),
        ),
        migrations.AddField(
            model_name='client',
            name='therapist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='symptoms.Therapist'),
        ),
        migrations.AddField(
            model_name='client',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
