from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.db.models import Q
from django.contrib.auth.forms import UserChangeForm
from .models import Profile
from stats.models import Match, Pit_stats
from teams.models import Team


def getProfileFirstName(request):
    f_placeholder = Profile.objects.get(request.user).first_name
    print(f_placeholder)
    return f_placeholder


User = get_user_model()


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "appearance-none rounded-none relative block w-full px-3 py-2 border border-black placeholder-black text-gray-900 focus:outline-none focus:ring-black focus:border-black focus:z-10 sm:text-sm darK:bg-secondary dark:placeholder-white dark:text-white",
                "placeholder": "Password",
            }
        ),
    )
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                "class": "appearance-none rounded-none relative block w-full px-3 py-2 border border-black placeholder-black text-gray-900 rounded-t-md focus:outline-none focus:ring-black focus:border-black focus:z-10 sm:text-sm darK:bg-secondary dark:placeholder-white dark:text-white",
                "placeholder": "Username",
            }
        ),
    )
    email = forms.EmailField(
        validators=[validate_email],
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "appearance-none rounded-none relative block w-full px-3 py-2 border border-black placeholder-black text-gray-900   focus:outline-none focus:ring-black focus:border-black focus:z-10 sm:text-sm darK:bg-secondary dark:placeholder-white dark:text-white",
                "placeholder": "Email",
                "id": "email-form",
            }
        ),
    )
    team_num = forms.IntegerField(
        label="Username",
        widget=forms.NumberInput(
            attrs={
                "class": "appearance-none rounded-none relative block w-full px-3 py-2 border border-black placeholder-black text-gray-900 rounded-b-md focus:outline-none focus:ring-black focus:border-black focus:z-10 sm:text-sm darK:bg-secondary dark:placeholder-white dark:text-white",
                "placeholder": "Team Number",
                "id": "team_num_reg",
            }
        ),
    )
    is_team_admin = forms.BooleanField(
        label="Is Admin",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "inp-cbx",
                "style": "display: none;",
                "id": "cbx",
                "name": "is_team_admin",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["username", "email", "team_num"]

    def clean_password(self):
        password = self.cleaned_data.get("password")
        return password

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    query = forms.CharField(
        label="Username / Email",
        widget=forms.TextInput(
            attrs={
                "id": "email-address",
                "class": "appearance-none rounded-none relative block w-full px-3 py-2 border border-black placeholder-black text-gray-900 rounded-t-md focus:outline-none focus:ring-black focus:border-black focus:z-10 sm:text-sm darK:bg-secondary dark:placeholder-white dark:text-white",
                "placeholder": "Username",
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "appearance-none rounded-none relative block w-full px-3 py-2 border border-black placeholder-black text-gray-900 rounded-b-md focus:outline-none focus:ring-black focus:border-black focus:z-10 sm:text-sm darK:bg-secondary dark:placeholder-white dark:text-white",
                "placeholder": "Password",
            }
        ),
    )

    def clean(self, *args, **kwargs):
        query = self.cleaned_data.get("query")
        password = self.cleaned_data.get("password")
        user_qs_final = User.objects.filter(
            Q(username__iexact=query) | Q(email__iexact=query)
        ).distinct()

        # TODO: Need to create non active user error message

        if not user_qs_final.exists() and user_qs_final.count != 1:
            raise forms.ValidationError("Invalid credentials - user does note exist")
        user_obj = user_qs_final.first()
        if not user_obj.check_password(password):
            raise forms.ValidationError("credentials are not correct")
        self.cleaned_data["user_obj"] = user_obj
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserEditForm(UserChangeForm):

    email = forms.CharField(
        label="Email",
        widget=forms.TextInput(
            attrs={
                "id": "email-address",
                "name": "email-address",
                "class": "appearance-none rounded-none relative block w-full px-3 py-2 border border-black placeholder-black text-gray-900 rounded-t-md focus:outline-none focus:ring-black focus:border-black focus:z-10 sm:text-sm",
                "placeholder": "Email",
            }
        ),
    )

    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                "id": "username",
                "class": "appearance-none rounded-none relative block w-full px-3 py-2 border border-black placeholder-black text-gray-900 rounded-t-md focus:outline-none focus:ring-black focus:border-black focus:z-10 sm:text-sm",
                "placeholder": "Username",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("email", "username")


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("image",)


class GameEditForm(forms.ModelForm):
    class Meta:
        model = Match
        exclude = ["competition", "stat", "scout"]


class PitEditForm(forms.ModelForm):
    class Meta:
        model = Pit_stats
        exclude = ["competition", "stat_id", "scout", "date_entered"]


class TeamEditForm(forms.ModelForm):

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "form-single",
                "placeholder": "Email",
                "id": "email-form",
            }
        ),
    )

    pit_stats_hide = forms.BooleanField(
        label="Hide Pit Stat",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "inp-cbx",
                "style": "display: none;",
                "id": "cbx",
            }
        ),
    )

    class Meta:
        model = Team
        fields = ["email", "pit_stats_hide"]


class NameEditForm(forms.ModelForm):

    first_name = forms.CharField(
        label="First Name",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-single", "id": "form-first_name"}),
    )

    last_name = forms.CharField(
        label="Last Name",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-single", "id": "form-last_name"}),
    )

    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
        )


class ProfileSettingsForm(forms.ModelForm):

    viewPitResubmit = forms.BooleanField(
        label="viewPitResubmit",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "inp-cbx",
                "style": "display: none;",
                "id": "cbx",
            }
        ),
    )

    relativeScoring = forms.BooleanField(
        label="relativeScoring",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "inp-cbx",
                "style": "display: none;",
                "id": "cbx1",
            }
        ),
    )

    class Meta:
        model = Profile
        fields = ("viewPitResubmit", "relativeScoring")


class TeamSettingsForm(forms.ModelForm):

    canEditStats = forms.BooleanField(
        label="canEditStats",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "inp-cbx",
                "style": "display: none;",
                "id": "cbx",
            }
        ),
    )

    is_team_admin = forms.BooleanField(
        label="canEditStats",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "inp-cbx",
                "style": "display: none;",
                "id": "cbx1",
            }
        ),
    )

    class Meta:
        model = Profile
        fields = ("canEditStats",)
