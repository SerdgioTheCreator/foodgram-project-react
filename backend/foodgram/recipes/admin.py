from django.contrib import admin
from django.utils.safestring import mark_safe

from api.constants import MIN_VALUE
from .models import Cart, Favorite, Ingredient, Recipe, Tag


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    min_num = MIN_VALUE


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name', )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author', 'name', 'show_ingredients',
        'show_image', 'count_favorites'
    )
    list_filter = ('id', 'author', 'name', 'tags', )
    inlines = (IngredientInline, )

    @admin.display(description='В избранном')
    def count_favorites(self, obj):
        return obj.favorite.count()

    @admin.display(description='Картинка')
    def show_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="80" height="60">')

    @admin.display(description='Ингредиенты')
    def show_ingredients(self, obj):
        return ', '.join(
            [str(ingredient) for ingredient in obj.ingredients.all()]
        )


admin.site.register(Cart)
admin.site.register(Favorite)
