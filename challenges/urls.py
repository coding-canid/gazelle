from django.urls import path

from . import views

app_name = "challenges"

urlpatterns = [
    path("take/<uuid:token>/", views.take_challenge, name="take"),
    path("assign/<int:candidate_pk>/", views.assign_challenge, name="assign"),
    path("assignments/<int:pk>/delete/", views.delete_assignment, name="delete_assignment"),
]
