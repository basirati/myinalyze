from django import forms

class DocumentForm(forms.Form):
    reqs_file = forms.FileField(
        label='Select a file',
        help_text='max. 200 megabytes'
    )