# Generated by Django 4.2.5 on 2023-10-05 06:37

import __common__.base_model
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("meta", models.JSONField(blank=True, default=dict, null=True)),
                ("name", models.CharField(max_length=64)),
                ("phone", models.CharField(max_length=20)),
                ("email", models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                "verbose_name": "e_learning users",
                "verbose_name_plural": "e_learning_users",
            },
            managers=[
                ("objects", __common__.base_model.BaseManager()),
            ],
        ),
    ]
