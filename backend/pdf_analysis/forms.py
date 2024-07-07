from django import forms
from User.models import Pdf

class PdfUploadForm(forms.ModelForm):
    class Meta:
        model = Pdf
        fields = ['pdf']
        
