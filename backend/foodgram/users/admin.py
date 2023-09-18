from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import Follow, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'id', 'email', 'username', 'first_name',
        'last_name', 'count_recipes', 'count_followers'
    )
    list_filter = ('email', 'username', 'first_name', )

    @admin.display(description='Рецепты')
    def count_recipes(self, obj):
        return obj.recipes.count()

    @admin.display(description='Подписчики')
    def count_followers(self, obj):
        return obj.following.count()


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'author'
    )
    list_filter = ('id', )


admin.site.unregister(Group)
