from django.urls import path

from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.index, name="index"),
    path("tasks/", views.create, name="create"),
    path("tasks/<int:pk>/toggle/", views.toggle, name="toggle"),
    path("tasks/<int:pk>/", views.delete, name="delete"),
]
