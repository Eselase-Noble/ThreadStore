# Generated by Django 4.0.4 on 2022-05-31 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_alter_product_image_alter_review_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AddField(
            model_name='review',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='review',
            name='title',
            field=models.CharField(default='I am satisfied', max_length=100),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.CharField(default='Anonymous', max_length=100),
        ),
    ]