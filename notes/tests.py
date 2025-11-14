from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Note
from .forms import NoteForm

class NoteModelTest(TestCase):
    def setUp(self):
        self.note = Note.objects.create(title='Test Title', content='Test Content')

    def test_note_creation(self):
        self.assertEqual(self.note.title, 'Test Title')
        self.assertEqual(self.note.content, 'Test Content')
        self.assertTrue(self.note.created_at)
        self.assertTrue(self.note.updated_at)

    def test_note_str(self):
        self.assertEqual(str(self.note), 'Test Title')

    def test_title_max_length(self):
        long_title = 'A' * 201
        self.note.title = long_title
        with self.assertRaises(ValidationError):
            self.note.full_clean()  # Validates fields, raises ValidationError

class NoteFormTest(TestCase):
    def test_valid_form(self):
        form_data = {'title': 'Valid Title', 'content': 'Valid Content'}
        form = NoteForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_title(self):
        form_data = {'content': 'Content only'}
        form = NoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_invalid_form_missing_content(self):
        form_data = {'title': 'Title only'}
        form = NoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

class NoteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.note = Note.objects.create(title='Test Note', content='Test Content')
        self.note_url = reverse('note_detail', args=[self.note.pk])
        self.list_url = reverse('note_list')
        self.create_url = reverse('note_create')
        self.update_url = reverse('note_update', args=[self.note.pk])
        self.delete_url = reverse('note_delete', args=[self.note.pk])

    def test_note_list_view(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')
        self.assertTemplateUsed(response, 'notes/note_list.html')

    def test_note_detail_view(self):
        response = self.client.get(self.note_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')
        self.assertTemplateUsed(response, 'notes/note_detail.html')

    def test_note_create_view_get(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_form.html')

    def test_note_create_view_post_valid(self):
        form_data = {'title': 'New Note', 'content': 'New Content'}
        response = self.client.post(self.create_url, form_data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertTrue(Note.objects.filter(title='New Note').exists())

    def test_note_create_view_post_invalid(self):
        form_data = {'title': '', 'content': ''}  # Invalid
        response = self.client.post(self.create_url, form_data)
        self.assertEqual(response.status_code, 200)  # No redirect
        self.assertContains(response, 'This field is required.')

    def test_note_update_view_get(self):
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')
        self.assertTemplateUsed(response, 'notes/note_form.html')

    def test_note_update_view_post_valid(self):
        form_data = {'title': 'Updated Title', 'content': 'Updated Content'}
        response = self.client.post(self.update_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Updated Title')

    def test_note_delete_view_get(self):
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')
        self.assertTemplateUsed(response, 'notes/note_confirm_delete.html')

    def test_note_delete_view_post(self):
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())

    def test_nonexistent_note_detail(self):
        response = self.client.get(reverse('note_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_empty_note_list(self):
        Note.objects.all().delete()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No notes yet.')