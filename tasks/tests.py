from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskViewTests(TestCase):
    def test_index_lists_tasks(self):
        Task.objects.create(title="Write tests")
        response = self.client.get(reverse("tasks:index"))
        self.assertContains(response, "Write tests")

    def test_create_returns_row_partial(self):
        response = self.client.post(reverse("tasks:create"), {"title": "Ship it"})
        self.assertContains(response, "Ship it")
        self.assertNotContains(response, "<html")
        self.assertTrue(Task.objects.filter(title="Ship it").exists())

    def test_create_ignores_blank_title(self):
        response = self.client.post(reverse("tasks:create"), {"title": "  "})
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Task.objects.exists())

    def test_toggle_flips_done(self):
        task = Task.objects.create(title="Toggle me")
        self.client.post(reverse("tasks:toggle", args=[task.pk]))
        task.refresh_from_db()
        self.assertTrue(task.done)

    def test_delete_removes_task(self):
        task = Task.objects.create(title="Delete me")
        response = self.client.delete(reverse("tasks:delete", args=[task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.exists())
