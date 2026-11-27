from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CandidateForm
from .models import Candidate


class CandidateListView(ListView):
    model = Candidate
    context_object_name = "candidates"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        status = self.request.GET.get("status", "")
        if q:
            qs = qs.filter(
                Q(first_name__icontains=q)
                | Q(last_name__icontains=q)
                | Q(email__icontains=q)
                | Q(position__icontains=q)
            )
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["status_choices"] = Candidate.Status.choices
        ctx["q"] = self.request.GET.get("q", "")
        ctx["current_status"] = self.request.GET.get("status", "")
        ctx["total_count"] = Candidate.objects.count()
        return ctx


class CandidateDetailView(DetailView):
    model = Candidate
    context_object_name = "candidate"

    def get_context_data(self, **kwargs):
        from challenges.forms import AssignChallengeForm

        ctx = super().get_context_data(**kwargs)
        ctx["assign_form"] = AssignChallengeForm()
        ctx["assignments"] = self.object.challenge_assignments.select_related("challenge")
        return ctx


class CandidateCreateView(SuccessMessageMixin, CreateView):
    model = Candidate
    form_class = CandidateForm
    success_message = "%(first_name)s %(last_name)s was added."


class CandidateUpdateView(SuccessMessageMixin, UpdateView):
    model = Candidate
    form_class = CandidateForm
    success_message = "%(first_name)s %(last_name)s was updated."


class CandidateDeleteView(DeleteView):
    model = Candidate
    context_object_name = "candidate"
    success_url = reverse_lazy("candidates:list")

    def form_valid(self, form):
        messages.success(self.request, f"{self.object.full_name} was deleted.")
        return super().form_valid(form)
