# Generated by Django 2.1.7 on 2019-02-20 01:48

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [("auth", "0009_alter_user_last_name_max_length")]

    operations = [
        migrations.CreateModel(
            name="Fencer",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "password",
                    models.CharField(max_length=128, verbose_name="password"),
                ),
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
                        blank=True, max_length=30, verbose_name="first name"
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
                        blank=True,
                        max_length=254,
                        verbose_name="email address",
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
                        default=django.utils.timezone.now,
                        verbose_name="date joined",
                    ),
                ),
                (
                    "foil_rating",
                    models.CharField(
                        choices=[
                            ("A", "A"),
                            ("B", "B"),
                            ("C", "C"),
                            ("D", "D"),
                            ("E", "E"),
                            ("U", "U"),
                        ],
                        default="U",
                        max_length=1,
                    ),
                ),
                (
                    "foil_year",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    "epee_rating",
                    models.CharField(
                        choices=[
                            ("A", "A"),
                            ("B", "B"),
                            ("C", "C"),
                            ("D", "D"),
                            ("E", "E"),
                            ("U", "U"),
                        ],
                        default="U",
                        max_length=1,
                    ),
                ),
                (
                    "epee_year",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    "sabre_rating",
                    models.CharField(
                        choices=[
                            ("A", "A"),
                            ("B", "B"),
                            ("C", "C"),
                            ("D", "D"),
                            ("E", "E"),
                            ("U", "U"),
                        ],
                        default="U",
                        max_length=1,
                    ),
                ),
                (
                    "sabre_year",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
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
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[("objects", django.contrib.auth.models.UserManager())],
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField()),
                (
                    "weapon",
                    models.CharField(
                        choices=[("E", "Epee"), ("F", "Foil"), ("S", "Sabre")],
                        default="E",
                        max_length=1,
                    ),
                ),
                (
                    "fee",
                    models.DecimalField(
                        decimal_places=2, default=0.0, max_digits=10
                    ),
                ),
                (
                    "rating_min",
                    models.CharField(
                        choices=[
                            ("A", "A"),
                            ("B", "B"),
                            ("C", "C"),
                            ("D", "D"),
                            ("E", "E"),
                            ("U", "U"),
                        ],
                        default="U",
                        max_length=1,
                        verbose_name="Minimum Rating",
                    ),
                ),
                (
                    "rating_max",
                    models.CharField(
                        choices=[
                            ("A", "A"),
                            ("B", "B"),
                            ("C", "C"),
                            ("D", "D"),
                            ("E", "E"),
                            ("U", "U"),
                        ],
                        default="A",
                        max_length=1,
                        verbose_name="Maximum Rating",
                    ),
                ),
                (
                    "fencers_max",
                    models.IntegerField(
                        verbose_name="Maximum Number of Fencers"
                    ),
                ),
                (
                    "fencers",
                    models.ManyToManyField(
                        blank=True, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Result",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("place", models.IntegerField()),
                ("comments", models.TextField()),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tournament.Event",
                    ),
                ),
                (
                    "fencer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Tournament",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True)),
                ("registration_open", models.DateTimeField()),
                ("registration_close", models.DateTimeField()),
                (
                    "registration_fee",
                    models.DecimalField(
                        decimal_places=2, default=0.0, max_digits=10
                    ),
                ),
            ],
            options={
                "ordering": ("-registration_close", "-registration_open")
            },
        ),
        migrations.AddField(
            model_name="event",
            name="tournament",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="tournament.Tournament",
            ),
        ),
    ]
