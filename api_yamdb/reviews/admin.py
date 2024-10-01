from django.contrib import admin


from .models import Category, Genre, Title, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
        'bio',
    )
    search_fields = ('username', 'role')
    list_filter = ('username',),
    empty_value_display = '-empty-'


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)