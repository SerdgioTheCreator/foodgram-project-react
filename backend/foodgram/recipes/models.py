from colorfield.fields import ColorField
from django.core import validators
from django.db import models

from api.constants import (BLUE, GREEN, MAX_INGREDIENTS_VALUE,
                           MAX_LENGTH, MAX_LENGTH_COLOR, MAX_VALUE,
                           MIN_VALUE, ORANGE, PURPLE, YELLOW)
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Единица измерения'
    )

    class Meta:
        ordering = ('name', 'measurement_unit', )
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(fields=['name', 'measurement_unit'],
                                    name='unique_ingredient')
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):

    COLOR_CHOICES = [
        (BLUE, 'Синий'),
        (ORANGE, 'Оранжевый'),
        (GREEN, 'Зеленый'),
        (PURPLE, 'Фиолетовый'),
        (YELLOW, 'Желтый'),
    ]
    name = models.CharField(
        max_length=MAX_LENGTH,
        unique=True,
        verbose_name='Название'
    )
    color = ColorField(
        format="hex",
        samples=COLOR_CHOICES,
        max_length=MAX_LENGTH_COLOR,
        unique=True,
        verbose_name='Цвет'
    )
    slug = models.SlugField(
        unique=True,
        max_length=MAX_LENGTH,
        verbose_name='Слаг'
    )

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Название'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Изображение'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        related_name='recipes',
        verbose_name='Список ингредиентов'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(
            validators.MinValueValidator(
                MIN_VALUE,
                message='Минимальное время приготовления: 1 минута'
            ),
            validators.MaxValueValidator(
                MAX_VALUE,
                message='Максимальное время приготовления: 180 минут'
            ),
        ),
        verbose_name='Время приготовления')

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipeingredient',
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        validators=(
            validators.MinValueValidator(
                MIN_VALUE,
                message='Минимальное количество ингридиентов: 1'
            ),
            validators.MaxValueValidator(
                MAX_INGREDIENTS_VALUE,
                message='Максимальное количество ингридиентов: 100'
            ),
        ),
        verbose_name='Количество',
    )

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(fields=['ingredient', 'recipe'],
                                    name='unique_ingredients_recipe')
        ]


class AbstractFavoriteCartModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        abstract = True
        ordering = ('-id', )
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='%(app_label)s_%(class)s_unique'
            )
        ]


class Favorite(AbstractFavoriteCartModel):

    class Meta(AbstractFavoriteCartModel.Meta):
        default_related_name = 'favorite'
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


class Cart(AbstractFavoriteCartModel):

    class Meta(AbstractFavoriteCartModel.Meta):
        default_related_name = 'cart'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
