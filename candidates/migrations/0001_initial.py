from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Candidate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("phone", models.CharField(blank=True, max_length=30)),
                ("position", models.CharField(max_length=150, verbose_name="Position applied for")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("applied", "Applied"),
                            ("screening", "Screening"),
                            ("interview", "Interviewing"),
                            ("offer", "Offer"),
                            ("hired", "Hired"),
                            ("rejected", "Rejected"),
                        ],
                        default="applied",
                        max_length=20,
                    ),
                ),
                ("linkedin_url", models.URLField(blank=True, verbose_name="LinkedIn URL")),
                ("resume_url", models.URLField(blank=True, verbose_name="Resume URL")),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
