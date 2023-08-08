from django.contrib import admin

from .models import Cart, Favorite, Ingredient, Recipe, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name', )


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'count_favorites')
    list_filter = ('id', 'author', 'name', 'tags', )

    def count_favorites(self, obj):
        return obj.favorites.count()
    count_favorites.short_description = 'Количество добавлений в избранное'


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Cart)
admin.site.register(Favorite)
