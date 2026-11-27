from django import forms

from .models import Challenge


class AssignChallengeForm(forms.Form):
    challenge = forms.ModelChoiceField(
        queryset=Challenge.objects.filter(is_active=True),
        empty_label="Choose a challenge…",
        widget=forms.Select(attrs={"class": "input"}),
    )


class AnswerForm(forms.Form):
    answer = forms.CharField(
        label="Your answer",
        widget=forms.Textarea(
            attrs={
                "class": "input mono",
                "rows": 4,
                "placeholder": "Type exactly what the code prints",
                "spellcheck": "false",
                "autocomplete": "off",
            }
        ),
    )
