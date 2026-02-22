from django import forms
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template import loader

from .models import BookingRequest, ContactMessage, NewsletterSubscriber, UserPreference


class ContactMessageForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = ContactMessage
        fields = ('full_name', 'email', 'message')
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Ismingiz'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email manzil'}),
            'message': forms.Textarea(attrs={'placeholder': 'Xabaringiz', 'rows': 5}),
        }

    def clean_website(self):
        if self.cleaned_data.get('website'):
            raise ValidationError("Spam aniqlandi.")
        return ''


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email manzil'}),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Bu email allaqachon ro'yxatdan o'tgan.")
        return email


class NewsletterSubscribeForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Newsletter uchun email'}),
        }


class BookingRequestForm(forms.ModelForm):
    class Meta:
        model = BookingRequest
        fields = ('full_name', 'email', 'preferred_datetime', 'note')
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Ismingiz'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'preferred_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'note': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Qisqacha izoh'}),
        }


class ThemePreferenceForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        fields = ('theme',)


class OTPTokenForm(forms.Form):
    token = forms.CharField(max_length=6, min_length=6, widget=forms.TextInput(attrs={'placeholder': '123456'}))


class SafePasswordResetForm(PasswordResetForm):
    """
    Django default form swallows SMTP errors. We bubble them up so the view can
    show debug fallback / user-facing error.
    """

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        subject = loader.render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()
