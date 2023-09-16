from datetime import date
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from authentication.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = '__all__'

    def clean_birthdate(self):
        today = date.today()
        value = self.cleaned_data['birthdate']
        if (
            today.year - value.year - (
                (today.month, today.day) < (value.month, value.day)
            )
        ) < 15:
            raise ValidationError(
                'You must have over 15 years old to create an account'
            )
        return self.cleaned_data['birthdate']


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = '__all__'


class CustomUserAdmin(UserAdmin):
    model = User
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = (
        'username', 'email', 'birthdate', 'can_be_contacted',
        'can_data_be_shared'
    )
    fieldsets = (
        (None, {'fields': (
            'password', 'username', 'email', 'birthdate',
            'can_be_contacted', 'can_data_be_shared'
        )}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2',
                       'birthdate', 'can_be_contacted', 'can_data_be_shared'),
        }),
    )


admin.site.register(User, CustomUserAdmin)
