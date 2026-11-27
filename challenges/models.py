import uuid

from django.db import models
from django.urls import reverse
from django.utils import timezone


def normalize_output(text):
    """Normalize output for comparison: unify newlines, strip trailing spaces
    on each line, and drop leading/trailing blank lines."""
    lines = (text or "").replace("\r\n", "\n").replace("\r", "\n").split("\n")
    return "\n".join(line.rstrip() for line in lines).strip("\n")


class Challenge(models.Model):
    """A 'what does this code print?' problem."""

    class Language(models.TextChoices):
        PYTHON = "python", "Python"
        JAVASCRIPT = "javascript", "JavaScript"
        RUBY = "ruby", "Ruby"
        JAVA = "java", "Java"
        OTHER = "other", "Other"

    title = models.CharField(max_length=150)
    prompt = models.TextField(default="What does this code print?")
    language = models.CharField(max_length=20, choices=Language.choices, default=Language.PYTHON)
    code_snippet = models.TextField()
    expected_output = models.TextField(help_text="Exact output the code prints.")
    is_active = models.BooleanField(default=True, help_text="Inactive challenges can't be assigned.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} ({self.get_language_display()})"

    def check_answer(self, answer):
        return normalize_output(answer) == normalize_output(self.expected_output)


class ChallengeAssignment(models.Model):
    """A challenge sent to a specific candidate, reachable by a private link."""

    candidate = models.ForeignKey(
        "candidates.Candidate", on_delete=models.CASCADE, related_name="challenge_assignments"
    )
    challenge = models.ForeignKey(Challenge, on_delete=models.PROTECT, related_name="assignments")
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    answer = models.TextField(blank=True)
    is_correct = models.BooleanField(null=True, blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-assigned_at"]

    def __str__(self):
        return f"{self.challenge.title} → {self.candidate}"

    @property
    def is_submitted(self):
        return self.submitted_at is not None

    def submit(self, answer):
        self.answer = answer
        self.is_correct = self.challenge.check_answer(answer)
        self.submitted_at = timezone.now()
        self.save(update_fields=["answer", "is_correct", "submitted_at"])

    def get_absolute_url(self):
        return reverse("challenges:take", kwargs={"token": self.token})
