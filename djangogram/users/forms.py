from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model,forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django import forms as django_forms

User = get_user_model()
class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User
class UserCreationForm(forms.UserCreationForm):
    error_message = forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )
    class Meta(forms.UserCreationForm.Meta):
        model = User
    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        error_messages = {
            "username": {"unique": _("This username has already been taken.")},
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """
class SignUpForm(django_forms.ModelForm):
    class Meta:
        # model = User
        # fields = ['email', 'name', 'username', 'password']

        # labels ={
        #     'email':'이메일 주소',
        #     'name': '성명',
        #     'username': '사용자 이름',
        #     'password': '비밀번호 '
        # }

        # widgets ={
        #     #패스워드가 보이는 것 방지
        #     'password': django_forms.PasswordInput()
        # }

        model = User
        fields = ['email', 'name', 'username', 'password']

        labels = {
            'email': '이메일 주소',
            'name': '성명',
            'username': '사용자 이름',
            'password': '비밀번호'
        }
        # labels = {
        #     'email': '이메일 주소',
        #     'name': '성명',
        #     'username': '사용자 이름',
        #     'password': '비밀번호'
        # }

        widgets = {
            'password': django_forms.PasswordInput(),
            'email': django_forms.TextInput(attrs={'placeholder': '이메일 주소'}),
            'name': django_forms.TextInput(attrs={'placeholder': '성명'}),
            'username': django_forms.TextInput(attrs={'placeholder': '사용자 이름'}),
            'password': django_forms.PasswordInput(attrs={'placeholder': '비밀번호'}),
        }

        
    # 로그 인시  admin 에서 보면 비밀번호가 오류남 -> save 재 정의
    def save(self, commit=True):
        user =super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user