# Generated by Django 5.1.5 on 2025-06-08 08:14

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

import leaderboard.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="codechefUser",
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
                ("username", models.CharField(max_length=64, unique=True)),
                ("max_rating", models.PositiveIntegerField(default=0)),
                ("Global_rank", models.CharField(default="NA", max_length=10)),
                ("Country_rank", models.CharField(default="NA", max_length=10)),
                ("rating", models.PositiveIntegerField(default=0)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                ("avatar", models.CharField(default="", max_length=256)),
            ],
            options={
                "ordering": ["-rating"],
            },
        ),
        migrations.CreateModel(
            name="codeforcesUser",
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
                ("username", models.CharField(max_length=64, unique=True)),
                ("max_rating", models.PositiveIntegerField(default=0)),
                ("rating", models.PositiveIntegerField(default=0)),
                ("last_activity", models.BigIntegerField(default=1749370480.070475)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                ("avatar", models.CharField(default="", max_length=256)),
                ("total_solved", models.PositiveIntegerField(default=0)),
                ("total_submissions", models.PositiveIntegerField(default=0)),
            ],
            options={
                "ordering": ["-rating"],
            },
        ),
        migrations.CreateModel(
            name="githubUser",
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
                ("username", models.CharField(max_length=64, unique=True)),
                ("contributions", models.PositiveIntegerField(default=0)),
                ("repositories", models.PositiveIntegerField(default=0)),
                ("stars", models.PositiveIntegerField(default=0)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                ("avatar", models.CharField(default="", max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name="LeetcodeUser",
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
                ("username", models.CharField(max_length=64, unique=True)),
                ("ranking", models.PositiveIntegerField(default=0)),
                ("easy_solved", models.PositiveIntegerField(default=0)),
                ("medium_solved", models.PositiveIntegerField(default=0)),
                ("hard_solved", models.PositiveIntegerField(default=0)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                ("avatar", models.CharField(default="", max_length=256)),
                ("total_solved", models.PositiveIntegerField(default=0)),
            ],
            options={
                "ordering": ["ranking"],
            },
        ),
        migrations.CreateModel(
            name="openlakeContributor",
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
                ("username", models.CharField(max_length=64, unique=True)),
                ("contributions", models.PositiveIntegerField(default=0)),
                ("last_updated", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-contributions"],
            },
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("uid", models.CharField(max_length=64, unique=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="codeforcesUserRatingUpdate",
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
                ("index", models.PositiveIntegerField(default=0)),
                ("prev_index", models.PositiveIntegerField(default=0)),
                ("rating", models.PositiveIntegerField(default=0)),
                ("timestamp", models.BigIntegerField(default=0)),
                (
                    "cf_user",
                    models.ForeignKey(
                        default=leaderboard.models.get_default_cf_user,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rating_updates",
                        to="leaderboard.codeforcesuser",
                    ),
                ),
            ],
            options={
                "ordering": ["timestamp"],
            },
        ),
        migrations.CreateModel(
            name="DiscussionPost",
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
                ("title", models.CharField(max_length=64, unique=True)),
                ("discription", models.CharField(max_length=256)),
                ("posted", models.DateTimeField(auto_now_add=True)),
                ("likes", models.PositiveIntegerField(default=0)),
                ("dislikes", models.PositiveIntegerField(default=0)),
                ("comments", models.PositiveIntegerField(default=0)),
                (
                    "username",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ReplyPost",
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
                ("discription", models.CharField(max_length=256)),
                ("posted", models.DateTimeField(auto_now_add=True)),
                ("likes", models.PositiveIntegerField(default=0)),
                ("dislikes", models.PositiveIntegerField(default=0)),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="leaderboard.discussionpost",
                    ),
                ),
                (
                    "username",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserNames",
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
                ("cc_uname", models.CharField(max_length=64)),
                ("cf_uname", models.CharField(max_length=64)),
                ("gh_uname", models.CharField(max_length=64)),
                ("lt_uname", models.CharField(default="", max_length=64)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserTasks",
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
                ("problem", models.PositiveIntegerField(default=0)),
                ("dueDate", models.DateTimeField()),
                ("title", models.CharField(max_length=64, unique=True)),
                ("discription", models.CharField(max_length=256)),
                ("completed", models.BooleanField(default=False)),
                ("starred", models.BooleanField(default=False)),
                ("solved", models.PositiveIntegerField(default=0)),
                ("total_solved_now", models.PositiveBigIntegerField(default=0)),
                (
                    "username",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
