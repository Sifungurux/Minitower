from django import forms
PROC =[
    (u'TCP', u'TCP'),
    (u'UDP', u'UDP'),
    (u'FTP', u'FTP')
    ]

class AddFirewall(forms.Form):
    source    = forms.CharField(
        label="Src",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
                }
            )
        )
    sourcenat = forms.CharField(
        label   = "Src Nat",
        widget  = forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    dest   = forms.CharField(
        label       = "Destination",
        widget      = forms.TextInput(
            attrs   = {
                'class': 'form-control'
                }
            )
        )
    destnat      = forms.CharField(
        label="Dest Nat",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
                }
            )
        )
    port      = forms.CharField(
        label="Port nr.",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
                }
            )
        )
    protocol     = forms.CharField(
        label="Protocol",
        widget=forms.Select(
            choices=PROC,
            attrs = {
                'class': 'form-control'
                }
            )
        )
    ref      = forms.CharField(
        label="Reference nr.",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
                }
            )
        )
    ticket      = forms.CharField(
        label="Ticket nr.",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
                }
            )
        )
    status      = forms.CharField(
        label="Status.",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
                }
            )
        )
    description      = forms.CharField(
        label="Description.",
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
                }
            )
        )
    note      = forms.CharField(
        label="Note.",
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
                }
            )
        )
    
    