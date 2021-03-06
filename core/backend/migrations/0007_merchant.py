# Generated by Django 4.0.4 on 2022-05-27 11:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backend', '0006_remove_product_extr_images_extraproductimage_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('company_address', models.CharField(max_length=100)),
                ('company_phone', models.CharField(max_length=100)),
                ('company_email', models.EmailField(max_length=100)),
                ('company_website', models.URLField(max_length=100)),
                ('company_logo', models.ImageField(upload_to='merchant_logo')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('approved', models.BooleanField(default=False)),
                ('live', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'merchants',
            },
        ),
    ]
