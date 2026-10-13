from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods, require_POST

from .models import Task


def index(request):
    return render(request, "tasks/index.html", {"tasks": Task.objects.all()})


@require_POST
def create(request):
    title = request.POST.get("title", "").strip()
    if not title:
        return HttpResponse(status=204)
    task = Task.objects.create(title=title[:200])
    return render(request, "tasks/_task.html", {"task": task})


@require_POST
def toggle(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.done = not task.done
    task.save(update_fields=["done"])
    return render(request, "tasks/_task.html", {"task": task})


@require_http_methods(["DELETE"])
def delete(request, pk):
    get_object_or_404(Task, pk=pk).delete()
    # Empty 200 so htmx swaps the row out of the page.
    return HttpResponse("")
