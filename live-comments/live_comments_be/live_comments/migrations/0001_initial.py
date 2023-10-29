# Generated by Django 4.2.6 on 2023-10-29 19:59

import __common__.base_model
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Channel",
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
            ],
            options={
                "verbose_name": "channels",
                "verbose_name_plural": "channels",
            },
            managers=[
                ("objects", __common__.base_model.BaseManager()),
            ],
        ),
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
                "verbose_name": "users",
                "verbose_name_plural": "users",
            },
            managers=[
                ("objects", __common__.base_model.BaseManager()),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
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
                ("text", models.CharField(max_length=300)),
                ("user_ts", models.BigIntegerField()),
                (
                    "channel",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="live_comments.channel",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="live_comments.user",
                    ),
                ),
            ],
            options={
                "verbose_name": "comments",
                "verbose_name_plural": "comments",
            },
            managers=[
                ("objects", __common__.base_model.BaseManager()),
            ],
        ),
    ]
