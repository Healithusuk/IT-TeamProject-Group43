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
        
        # 如果表单提交中 avatar 字段被清除，则 form.cleaned_data['avatar'] 为 False/None
        if 'avatar' in self.changed_data and not self.cleaned_data.get('avatar'):
            # 如果数据库中已经存在一个 avatar 文件，则先删除实际文件
            if instance.pk:
                try:
                    old_instance = Accounts.objects.get(pk=instance.pk)
                    # 判断旧的 avatar 是否存在且不是默认图片
                    if old_instance.avatar and str(old_instance.avatar) != default_path:
                        old_instance.avatar.delete(save=False)
                except Accounts.DoesNotExist:
                    pass
            # 此时 instance.avatar 会被设置为 None
            instance.avatar = None

        # 如果用户没有上传头像且 avatar 为 None，则设置默认路径
        if not instance.avatar:
            instance.avatar = default_path

        if commit:
            instance.save()
        return instance
