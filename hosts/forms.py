from django import forms
ENV =[
    (u'UDV', u'UDV'),
    (u'TST', u'TST'),
    (u'PRE', u'PRE'),
    (u'PROD', u'PROD'),
    ]

class AddHost(forms.Form):
    hostname    = forms.CharField(
        label="Hostname",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
                }
            )
        )
    description = forms.CharField(
        label   = "Describtion",
        widget  = forms.Textarea(
            attrs={
                'class': 'form-control',
                "row": 5,
                "cols": 25
            }
        )
    )
    systemproduct   = forms.CharField(
        label       = "System",
        widget      = forms.TextInput(
            attrs   = {
                'class': 'form-control'
                }
            )
        )
    environment     = forms.CharField(
        label="Environment",
        widget=forms.Select(
            choices=ENV,
            attrs = {
                'class': 'form-control'
                }
            )
        )
    system_owner      = forms.CharField(
        label="Supplier",
        initial = "DVU",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
                }
            )
        )