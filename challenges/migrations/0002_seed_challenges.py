"""Seed a few starter 'what does this print?' challenges."""
from django.db import migrations

SEED = [
    {
        "title": "Sum the odd numbers",
        "language": "python",
        "code_snippet": (
            "nums = [3, 1, 4, 1, 5]\n"
            "total = 0\n"
            "for n in nums:\n"
            "    if n % 2 == 1:\n"
            "        total += n\n"
            "print(total)"
        ),
        "expected_output": "10",
    },
    {
        "title": "List references",
        "language": "python",
        "code_snippet": (
            "a = [1, 2, 3]\n"
            "b = a\n"
            "b.append(4)\n"
            "print(len(a))"
        ),
        "expected_output": "4",
    },
    {
        "title": "Map and filter",
        "language": "javascript",
        "code_snippet": (
            'const words = ["gazelle", "lion", "zebra"];\n'
            "const result = words.map(w => w.length).filter(n => n > 4);\n"
            'console.log(result.join(","));'
        ),
        "expected_output": "7,5",
    },
]


def seed(apps, schema_editor):
    Challenge = apps.get_model("challenges", "Challenge")
    for data in SEED:
        Challenge.objects.get_or_create(title=data["title"], defaults=data)


def unseed(apps, schema_editor):
    Challenge = apps.get_model("challenges", "Challenge")
    Challenge.objects.filter(title__in=[d["title"] for d in SEED], assignments__isnull=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("challenges", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
