from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    """
    Form for creating and editing Note instances.
    
    Inherits from ModelForm to auto-map fields from Note model.
    Customizes widgets for Bootstrap styling and placeholders.
    
    Meta:
        model: Note
        fields: ['title', 'content']
    """
    class Meta:
        model = Note
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter note title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter note content', 'rows': 5}),
        }