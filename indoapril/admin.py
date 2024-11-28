from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserRole
from .forms import CustomUserCreationForm

class UserRoleInline(admin.StackedInline):
    model = UserRole
    can_delete = False
    verbose_name_plural = 'Role'

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    inlines = (UserRoleInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role')

    # Explicitly define fieldsets to avoid unknown field errors
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )

    def get_role(self, obj):
        try:
            return obj.user_role.role
        except UserRole.DoesNotExist:
            return "No Role"
    get_role.short_description = 'Role'

admin.site.register(CustomUser, CustomUserAdmin)