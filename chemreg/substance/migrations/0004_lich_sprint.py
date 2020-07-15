# Generated by Django 3.0.3 on 2020-07-15 19:02

import chemreg.common.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('substance', '0003_kaus_borealis_sprint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='synonymquality',
            name='is_restrictive',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Synonym',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('identifier', models.TextField(max_length=1024)),
                ('qc_notes', models.TextField(max_length=1024, null=True)),
                ('created_by', models.ForeignKey(default=chemreg.common.utils.get_current_user_pk, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='synonym_created_by_set', to=settings.AUTH_USER_MODEL)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='substance.Source')),
                ('synonym_quality', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='substance.SynonymQuality')),
                ('synonym_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='substance.SynonymType')),
                ('updated_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='synonym_updated_by_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['pk'],
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
    ]
