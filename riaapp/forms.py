from django import forms

class DocumentForm(forms.Form):
    reqs_file = forms.FileField(
        label='Select a file',
        help_text='max. 200 megabytes'
    )


class CreateProjForm(forms.Form):
    proj_name = forms.CharField(label='Project Name', max_length=80)
    proj_desc = forms.CharField(label='Project Description', max_length=1000, required=False)