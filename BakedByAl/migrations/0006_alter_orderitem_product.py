# Generated by Django 4.2.1 on 2023-05-13 04:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BakedByAl', '0005_remove_orderitem_description_remove_orderitem_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BakedByAl.galleryitem'),
        ),
    ]
