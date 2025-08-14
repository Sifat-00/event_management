from django import forms
import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Permission,Group
from .models import Category
from .models import Event
from .models import Participant
from django.contrib.auth.models import Group
from .models import Profile


class StyleMixin:
    def apply_common_style(self):

        common_class = (
            'w-full mb-5 px-4 py-3 rounded-xl border border-gray-310 '
            'placeholder-gray-400 text-sm '
        )


        for field_name, field in self.fields.items():
            if not field.widget.attrs.get('placeholder'):


                field.widget.attrs['placeholder'] = field.label


            field.widget.attrs['class']= common_class


class CategoryForm(StyleMixin,forms.ModelForm):
    class Meta:

        model = Category

        fields = ['name','description']


    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.apply_common_style()


class EventForm(StyleMixin,forms.ModelForm):
    class Meta:

        model = Event

        fields = ['title', 'category', 'location', 'date', 'time', 'description', 'image']





    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)


        self.apply_common_style()

        self.fields['date'].widget.input_type = 'date'
        self.fields['time'].widget.input_type = 'time'






class ParticipantForm(StyleMixin, forms.ModelForm):
    class Meta:
        model = Participant

        fields = ['name', 'email','events']

        widgets = {
            'events': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, event_instance=None, **kwargs):
        super(ParticipantForm, self).__init__(*args, **kwargs)
        self.apply_common_style()

        if event_instance:

            self.fields['events'].queryset = Event.objects.filter(pk=event_instance.pk)
            self.fields['events'].initial =event_instance







class RegisterForm(forms.ModelForm, StyleMixin):

    password1 = forms.CharField(

        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter Password'
        })
    )

    confirm_password = forms.CharField(

        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password'
        })
    )


    class Meta:
        model = User

        fields = ['username', 'first_name', 'last_name',
                  'password1', 'confirm_password', 'email']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.apply_common_style()

    def clean(self):

        cleaned_data = super().clean()

        password1 = cleaned_data.get('password1')

        confirm_password = cleaned_data.get('confirm_password')

        if password1 != confirm_password:

            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data




class AssignRoleForm(forms.Form):

    role = forms.ModelChoiceField(

        queryset=Group.objects.all(),


        empty_label="Select a Role",

        widget=forms.Select(
            attrs={
                "class": "w-full px-4 py-2 border rounded-lg shadow-sm focus:border-blue-500"
            }
        ),
        label="Choose Role"
    )


class CreateGroupForm(forms.ModelForm):

    permissions = forms.ModelMultipleChoiceField(

        queryset=Permission.objects.all(),



        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'space-y-5'
            
        }),
        required=False,
        label='Assign permission',
    )

    class Meta:
        model = Group

        fields = ['name','permissions']
        widgets = {

            'name': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border border-gray-300 py-2 px-3 shadow-sm ',
                'placeholder': 'Enter group name',
            }),
        }



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile


        fields = ['profile_pic', 'phone_num']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']