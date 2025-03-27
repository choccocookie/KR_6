from django import forms
from .models import Client, Message, Mailing


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'fullname', 'comment']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['topic', 'content']


class MailingForm(forms.ModelForm):
    clients = forms.ModelMultipleChoiceField(
        queryset=Client.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    messages = forms.ModelChoiceField(
        queryset=Message.objects.all(),
        required=True
    )
    first_sanding_data = forms.DateTimeField(
        label="Дата отправки",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=['%Y-%m-%d']
    )

    class Meta:
        model = Mailing
        fields = ['first_sanding_data', 'intervals',
                  'status', 'message', 'clients']
