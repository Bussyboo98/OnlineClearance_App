from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

@admin.action(description='Mark selected students as cleared')
def make_cleared(modeladmin, request, queryset):
    queryset.update(is_cleared=True)

class StudentAdmin(UserAdmin):
    list_display = ('username', 'matric_number', 'email', 'department', 'clearance_status', 'is_cleared')
    search_fields = ('username', 'matric_number')
    fieldsets = (
        (None, {'fields': ('username', 'matric_number', 'full_name', 'email', 'sex', 'date_of_birth', 'address', 'password', 'department', 'phone_number', 'clearance_status', 'is_cleared')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'matric_number', 'department')}
        ),
    )
    actions = [make_cleared]

    def mark_as_cleared(self, request, queryset):
        queryset.update(is_cleared=True)
    mark_as_cleared.short_description = "Mark selected students as cleared"

admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(ClearanceStatus)
admin.site.register(Student, StudentAdmin)
admin.site.register(Document)
