# Generated by Django 3.2.25 on 2024-04-23 05:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UsageFor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usage_for_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('product_image', models.ImageField(blank=True, default='default.png', null=True, upload_to='')),
                ('product_title', models.CharField(max_length=200)),
                ('product_description', models.TextField()),
                ('product_price', models.FloatField()),
                ('product_brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='design.brand')),
                ('product_usage_for', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='design.usagefor')),
            ],
        ),
    ]
