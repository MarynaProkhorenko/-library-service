# Generated by Django 4.2 on 2023-04-19 10:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("borrowing_service", "0003_alter_borrowing_borrow_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="borrowing",
            name="actual_return_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]