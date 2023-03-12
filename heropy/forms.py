from django import forms


class FileForm(forms.Form):
    newfile = forms.FileField()
