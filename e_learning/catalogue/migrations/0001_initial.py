# Generated by Django 4.2.5 on 2023-09-28 02:29

import __common__.base_model
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("meta", models.JSONField(blank=True, default=dict, null=True)),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "name",
                    models.CharField(
                        blank=True, max_length=128, null=True, unique=True
                    ),
                ),
                (
                    "description",
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                (
                    "display_text",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
                ("icon", models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                "verbose_name": "categories",
                "db_table": "categories",
            },
            managers=[
                ("objects", __common__.base_model.BaseManager()),
            ],
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("meta", models.JSONField(blank=True, default=dict, null=True)),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("heading", models.CharField(max_length=64)),
                (
                    "description",
                    models.TextField(blank=True, max_length=2000, null=True),
                ),
                (
                    "amount",
                    models.DecimalField(decimal_places=2, default=99.0, max_digits=8),
                ),
                (
                    "currency",
                    models.CharField(
                        blank=True, default="INR", max_length=20, null=True
                    ),
                ),
                ("max_seats", models.IntegerField(default=25, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("inactive", "Inactive"),
                            ("accepting_registrations", "Accepting Registrations"),
                            ("paused_registrations", "Paused Registrations"),
                            ("ended", "Ended"),
                        ],
                        default="inactive",
                        max_length=64,
                    ),
                ),
                ("start_date", models.DateTimeField(blank=True, null=True)),
                ("end_date", models.DateTimeField(blank=True, null=True)),
                ("sessions", models.IntegerField(default=10, null=True)),
                ("duration", models.IntegerField(default=90, null=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalogue.category",
                    ),
                ),
            ],
            options={
                "verbose_name": "courses",
                "db_table": "courses",
            },
            managers=[
                ("objects", __common__.base_model.BaseManager()),
            ],
        ),
    ]
