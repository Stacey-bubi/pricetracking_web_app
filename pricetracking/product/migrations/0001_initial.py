# Generated by Django 4.0.2 on 2022-04-29 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('current_price', models.FloatField()),
                ('old_price', models.FloatField()),
                ('price_difference', models.FloatField()),
                ('date_updated', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date_created', 'name', '-date_updated'],
            },
        ),
    ]
