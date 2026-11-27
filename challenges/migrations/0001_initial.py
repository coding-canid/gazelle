import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("candidates", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Challenge",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=150)),
                ("prompt", models.TextField(default="What does this code print?")),
                (
                    "language",
                    models.CharField(
                        choices=[
                            ("python", "Python"),
                            ("javascript", "JavaScript"),
                            ("ruby", "Ruby"),
                            ("java", "Java"),
                            ("other", "Other"),
                        ],
                        default="python",
                        max_length=20,
                    ),
                ),
                ("code_snippet", models.TextField()),
                ("expected_output", models.TextField(help_text="Exact output the code prints.")),
                (
                    "is_active",
                    models.BooleanField(default=True, help_text="Inactive challenges can't be assigned."),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["title"]},
        ),
        migrations.CreateModel(
            name="ChallengeAssignment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("token", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("answer", models.TextField(blank=True)),
                ("is_correct", models.BooleanField(blank=True, null=True)),
                ("assigned_at", models.DateTimeField(auto_now_add=True)),
                ("submitted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "candidate",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="challenge_assignments",
                        to="candidates.candidate",
                    ),
                ),
                (
                    "challenge",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="assignments",
                        to="challenges.challenge",
                    ),
                ),
            ],
            options={"ordering": ["-assigned_at"]},
        ),
    ]
