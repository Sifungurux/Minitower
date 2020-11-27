from django import forms


class UploadData(forms.Form):
    File = forms.FileField(
        label="File Upload"
    )
    