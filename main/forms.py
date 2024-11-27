from django import forms

class UploadForm(forms.Form):
    image = forms.ImageField()
    source = forms.ChoiceField(choices=[('Bank Document', 'Bank Document'), ('Government Document', 'Government Document')])
