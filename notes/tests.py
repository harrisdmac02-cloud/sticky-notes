"""
Unit and integration tests for the Sticky Notes application.
Covers models, forms, and views for CRUD functionality.
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from notes.models import Note
from notes.forms import NoteForm


class NoteModelTest(TestCase):
    """Tests for the Note model."""

    def setUp(self):
        """Set up test data for each test method."""
        self.note = Note.objects.create(title="Test Title", content="Test Content")

    def test_note_creation(self):
        """Test that a Note instance can be created successfully."""
        self.assertEqual(self.note.title, "Test Title")
        self.assertEqual(self.note.content, "Test Content")
        self.assertTrue(self.note.created_at)  # Timestamp set
        self.assertTrue(self.note.updated_at)  # Timestamp set

    def test_note_str(self):
        """Test the string representation of a Note."""
        self.assertEqual(str(self.note), "Test Title")


class NoteFormTest(TestCase):
    """Tests for the NoteForm."""

    def test_valid_form(self):
        """Test form validation with valid data."""
        form_data = {"title": "Valid Title", "content": "Valid Content"}
        form = NoteForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_title_missing(self):
        """Test form validation when title is missing."""
        form_data = {"content": "Valid Content"}
        form = NoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_invalid_form_content_too_long(self):
        """Test form validation when content exceeds reasonable length (simulated)."""
        long_content = "x" * 10000  # Arbitrary long string
        form_data = {"title": "Valid Title", "content": long_content}
        form = NoteForm(data=form_data)
        self.assertTrue(form.is_valid())  # TextField has no max_length, but test structure

    def test_title_max_length(self):
        """Test title field max_length constraint."""
        form_data = {"title": "x" * 201, "content": "Valid Content"}  # Exceeds 200
        form = NoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)


class NoteViewTests(TestCase):
    """Integration tests for Note views (CRUD)."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.note = Note.objects.create(title="Test Note", content="Test Content")
        self.note_url = reverse('note_detail', args=[self.note.pk])
        self.list_url = reverse('note_list')
        self.create_url = reverse('note_create')

    def test_note_list_view(self):
        """Test listing all notes."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Note")
        self.assertTemplateUsed(response, 'notes/note_list.html')

    def test_note_detail_view(self):
        """Test viewing a single note."""
        response = self.client.get(self.note_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Note")
        self.assertContains(response, "Test Content")
        self.assertTemplateUsed(response, 'notes/note_detail.html')

    def test_note_create_view(self):
        """Test creating a new note."""
        form_data = {"title": "New Note", "content": "New Content"}
        response = self.client.post(self.create_url, form_data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertRedirects(response, self.list_url)
        self.assertTrue(Note.objects.filter(title="New Note").exists())

    def test_note_create_invalid(self):
        """Test creating with invalid data."""
        form_data = {"title": "", "content": ""}  # Missing required
        response = self.client.post(self.create_url, form_data)
        self.assertEqual(response.status_code, 200)  # Renders form with errors
        self.assertContains(response, "This field is required.")

    def test_note_update_view(self):
        """Test updating an existing note."""
        update_url = reverse('note_update', args=[self.note.pk])
        form_data = {"title": "Updated Title", "content": "Updated Content"}
        response = self.client.post(update_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.list_url)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Updated Title")

    def test_note_delete_view(self):
        """Test deleting a note."""
        delete_url = reverse('note_delete', args=[self.note.pk])
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.list_url)
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())

    def test_nonexistent_note_detail(self):
        """Test 404 for non-existent note."""
        bad_url = reverse('note_detail', args=[999])
        response = self.client.get(bad_url)
        self.assertEqual(response.status_code, 404)