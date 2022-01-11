# Generated by Django 4.0.1 on 2022-01-11 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NutsPostcode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nuts', models.CharField(max_length=16)),
                ('postcode', models.CharField(max_length=16)),
            ],
            options={
                'unique_together': {('nuts', 'postcode')},
            },
        ),
        migrations.CreateModel(
            name='Geography',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.PositiveSmallIntegerField()),
                ('original_name', models.CharField(max_length=256)),
                ('en_name', models.CharField(max_length=256, null=True)),
                ('code', models.CharField(max_length=16, unique=True)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='geographical_module.geography')),
                ('top_parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bottom_children', to='geographical_module.geography')),
            ],
        ),
    ]
