from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from candidates.models import Candidate

from .forms import AnswerForm, AssignChallengeForm
from .models import ChallengeAssignment


@require_POST
def assign_challenge(request, candidate_pk):
    """Recruiter action: assign a challenge to a candidate and create a private link."""
    candidate = get_object_or_404(Candidate, pk=candidate_pk)
    form = AssignChallengeForm(request.POST)
    if form.is_valid():
        assignment = ChallengeAssignment.objects.create(
            candidate=candidate, challenge=form.cleaned_data["challenge"]
        )
        messages.success(
            request, f"Assigned “{assignment.challenge.title}”. Send {candidate.first_name} the link below."
        )
    else:
        messages.error(request, "Please choose a challenge to assign.")
    return redirect(candidate.get_absolute_url())


@require_POST
def delete_assignment(request, pk):
    """Recruiter action: revoke an assignment (its link stops working)."""
    assignment = get_object_or_404(ChallengeAssignment, pk=pk)
    candidate = assignment.candidate
    assignment.delete()
    messages.success(request, "Challenge assignment removed.")
    return redirect(candidate.get_absolute_url())


def take_challenge(request, token):
    """Candidate portal: view the snippet and submit an answer (one attempt)."""
    assignment = get_object_or_404(
        ChallengeAssignment.objects.select_related("challenge", "candidate"), token=token
    )

    if assignment.is_submitted:
        return render(request, "challenges/submitted.html", {"assignment": assignment})

    form = AnswerForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        assignment.submit(form.cleaned_data["answer"])
        return redirect(assignment.get_absolute_url())

    return render(request, "challenges/take.html", {"assignment": assignment, "form": form})
