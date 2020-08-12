# Generated by Django 3.0.3 on 2020-08-10 15:04

import chemreg.common.utils
import chemreg.lists.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('substance', '0005_mago_sprint'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessibilityType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.SlugField(max_length=49, unique=True)),
                ('label', models.CharField(max_length=99, unique=True)),
                ('short_description', models.CharField(max_length=499)),
                ('long_description', models.TextField()),
                ('deprecated', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(default=chemreg.common.utils.get_current_user_pk, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='accessibilitytype_created_by_set', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='accessibilitytype_updated_by_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['pk'],
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='ExternalContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=49, unique=True)),
                ('email', models.CharField(max_length=49, unique=True)),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('created_by', models.ForeignKey(default=chemreg.common.utils.get_current_user_pk, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='externalcontact_created_by_set', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='externalcontact_updated_by_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['pk'],
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='IdentifierType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.SlugField(max_length=49, unique=True)),
                ('label', models.CharField(max_length=99, unique=True)),
                ('short_description', models.CharField(max_length=499)),
                ('long_description', models.TextField()),
                ('deprecated', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(default=chemreg.common.utils.get_current_user_pk, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='identifiertype_created_by_set', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='identifiertype_updated_by_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['pk'],
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.SlugField(max_length=49, unique=True)),
                ('label', models.CharField(max_length=255, unique=True)),
                ('short_description', models.TextField(max_length=1000)),
                ('long_description', models.TextField()),
                ('source_url', models.CharField(blank=True, max_length=500)),
                ('source_reference', models.CharField(blank=True, max_length=500)),
                ('source_doi', models.CharField(blank=True, max_length=500)),
                ('date_of_source_collection', models.DateTimeField()),
                ('created_by', models.ForeignKey(default=chemreg.common.utils.get_current_user_pk, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='list_created_by_set', to=settings.AUTH_USER_MODEL)),
                ('external_contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='lists.ExternalContact')),
                ('list_accessibility', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lists.AccessibilityType')),
                ('owners', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['pk'],
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('rid', models.CharField(default=chemreg.lists.utils.build_rid, max_length=50, unique=True)),
                ('external_id', models.CharField(max_length=500)),
                ('message', models.CharField(blank=True, max_length=500)),
                ('score', models.FloatField(null=True)),
                ('is_validated', models.BooleanField()),
                ('created_by', models.ForeignKey(default=chemreg.common.utils.get_current_user_pk, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='record_created_by_set', to=settings.AUTH_USER_MODEL)),
                ('list', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lists.List')),
                ('substance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='substance.Substance')),
                ('updated_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='record_updated_by_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['pk'],
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='RecordIdentifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('identifier', models.TextField()),
                ('identifier_label', models.CharField(max_length=100)),
                ('created_by', models.ForeignKey(default=chemreg.common.utils.get_current_user_pk, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='recordidentifier_created_by_set', to=settings.AUTH_USER_MODEL)),
                ('identifier_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='lists.IdentifierType')),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='identifiers', to='lists.Record')),
                ('updated_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='recordidentifier_updated_by_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['pk'],
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='ListType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.SlugField(max_length=49, unique=True)),
                ('label', models.CharField(max_length=99, unique=True)),
                ('short_description', models.CharField(max_length=499)),
                ('long_description', models.TextField()),
                ('deprecated', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(default=chemreg.common.utils.get_current_user_pk, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='listtype_created_by_set', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='listtype_updated_by_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['pk'],
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.AddField(
            model_name='list',
            name='types',
            field=models.ManyToManyField(blank=True, related_name='lists', to='lists.ListType'),
        ),
        migrations.AddField(
            model_name='list',
            name='updated_by',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='list_updated_by_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
