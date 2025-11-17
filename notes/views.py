from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Note
from .forms import NoteForm

class NoteListView(ListView):
    """
    View to display a list of all notes, ordered by creation date (newest first).
    
    Attributes:
        model: Note
        template_name: 'notes/note_list.html'
        context_object_name: 'notes'
        ordering: ['-created_at']
    """
    model = Note
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'
    ordering = ['-created_at']

class NoteDetailView(DetailView):
    """
    View to display a single note's details.
    
    Attributes:
        model: Note
        template_name: 'notes/note_detail.html'
        context_object_name: 'note'
    """
    model = Note
    template_name = 'notes/note_detail.html'
    context_object_name = 'note'

class NoteCreateView(CreateView):
    """
    View to create a new note using NoteForm.
    
    Attributes:
        model: Note
        form_class: NoteForm
        template_name: 'notes/note_form.html'
        success_url: URL to note list
    """
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('note_list')

class NoteUpdateView(UpdateView):
    """
    View to update an existing note using NoteForm.
    
    Attributes:
        model: Note
        form_class: NoteForm
        template_name: 'notes/note_form.html'
        success_url: URL to note list
    """
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('note_list')

class NoteDeleteView(DeleteView):
    """
    View to delete a note with confirmation.
    
    Attributes:
        model: Note
        template_name: 'notes/note_confirm_delete.html'
        success_url: URL to note list
    """
    model = Note
    template_name = 'notes/note_confirm_delete.html'
    success_url = reverse_lazy('note_list')