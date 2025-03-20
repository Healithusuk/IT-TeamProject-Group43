from django import forms
from allModels.models import Accounts

class AccountSettingsForm(forms.ModelForm):
    class Meta:
        model = Accounts
        fields = ['username', 'email', 'first_name', 'last_name', 'birthday', 'bio', 'avatar']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'maxlength':'21'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'maxlength': '250'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }  
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        default_path = 'user_avatar/avatar_default.png'
        
        # If the avatar field is cleared in the form submission, then form.cleaned_data['avatar'] is False/None
        if 'avatar' in self.changed_data and not self.cleaned_data.get('avatar'):
            # If an avatar file already exists in the database, delete the actual file first
            if instance.pk:
                try:
                    old_instance = Accounts.objects.get(pk=instance.pk)
                    # Determines if the old avatar exists and is not the default image.
                    if old_instance.avatar and str(old_instance.avatar) != default_path:
                        old_instance.avatar.delete(save=False)
                except Accounts.DoesNotExist:
                    pass
            # instance.avatar will then be set to None
            instance.avatar = None

        # If the user has not uploaded an avatar and avatar is None, the default path is set
        if not instance.avatar:
            instance.avatar = default_path

        if commit:
            instance.save()
        return instance
