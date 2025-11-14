from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Note
from .forms import NoteForm

class NoteModelTest(TestCase):
    def setUp(self):
        self.note = Note.objects.create(title='Test Title', content='Test Content')

    def test_str_method(self):
        self.assertEqual(str(self.note), 'Test Title')

    def test_title_max_length(self):
        long_title = 'x' * 201
        self.note.title = long_title
        with self.assertRaises(Exception):
            self.note.full_clean()  # Explicitly validate
        self.note.refresh_from_db()
        self.assertNotEqual(self.note.title, long_title)  # Still original)

    def test_content_required(self):
        note = Note(title='Title', content='')
        with self.assertRaises(Exception):  # ValidationError from blank=False
            note.full_clean()  # Explicitly validate

class NoteFormTest(TestCase):
    def test_form_valid(self):
        form_data = {'title': 'Valid Title', 'content': 'Valid Content'}
        form = NoteForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_blank_title(self):
        form_data = {'title': '', 'content': 'Content'}
        form = NoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_form_invalid_blank_content(self):
        form_data = {'title': 'Title', 'content': ''}
        form = NoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

class NoteViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.note = Note.objects.create(title='Test Note', content='Test Content')
        self.list_url = reverse('note_list')
        self.detail_url = reverse('note_detail', args=[self.note.pk])
        self.create_url = reverse('note_create')
        self.update_url = reverse('note_update', args=[self.note.pk])
        self.delete_url = reverse('note_delete', args=[self.note.pk])

    def test_note_list_view(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['notes']), 1)
        self.assertTemplateUsed(response, 'notes/note_list.html')
        self.assertContains(response, 'Test Note')

    def test_note_detail_view(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['note'].title, 'Test Note')
        self.assertTemplateUsed(response, 'notes/note_detail.html')

    def test_note_create_view_get(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_form.html')

    def test_note_create_view_post_valid(self):
        form_data = {'title': 'New Note', 'content': 'New Content'}
        response = self.client.post(self.create_url, form_data)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertEqual(Note.objects.count(), 2)
        new_note = Note.objects.get(title='New Note')
        self.assertEqual(new_note.content, 'New Content')

    def test_note_create_view_post_invalid(self):
        form_data = {'title': '', 'content': 'Content'}
        response = self.client.post(self.create_url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_form.html')
        self.assertFormError(response, 'form', 'title', 'This field is required.')

    def test_note_update_view_get(self):
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')  # Pre-filled
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
        self.assertTemplateUsed(response, 'notes/note_confirm_delete.html')
        self.assertContains(response, 'Test Note')

    def test_note_delete_view_post(self):
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())
        self.assertEqual(Note.objects.count(), 0)

    def test_nonexistent_detail_view(self):
        invalid_url = reverse('note_detail', args=[999])
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 404)

    def test_empty_list_view(self):
        Note.objects.all().delete()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['notes']), 0)
        self.assertContains(response, 'No notes yet.')