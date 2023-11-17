from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from .constants import MAX_COOKING_TIME, MAX_INGREDIENTS_VALUE, MIN_VALUE
from recipes.models import (Cart, Favorite, Ingredient, IngredientAmount,
                            Recipe, Tag)
from users.models import Follow, User


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return (request
                and request.user.is_authenticated
                and request.user.follower.filter(author=obj.id).exists())


class GetFollowSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + (
            'recipes',
            'recipes_count'
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        try:
            recipes = recipes[:int(limit)]
        except TypeError:
            pass
        return SmallRecipeSerializer(recipes, many=True, read_only=True).data

    @staticmethod
    def get_recipes_count(obj):
        return obj.recipes.count()


class PostFollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = (
            'user',
            'author'
        )

    def validate(self, data):
        if Follow.objects.filter(
                author=data['author'], user=data['user']
        ).exists():
            raise ValidationError(
                detail='Вы уже подписаны на этого пользователя',
                code=status.HTTP_400_BAD_REQUEST
            )
        if data['user'] == data['author']:
            raise ValidationError(
                detail='Вы не можете подписаться на самого себя',
                code=status.HTTP_400_BAD_REQUEST
            )
        return data

    def to_representation(self, instance):
        return GetFollowSerializer(
            instance.author, context={
                'request': self.context.get('request')
            }).data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class GetIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class GetRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = GetIngredientSerializer(
        source='recipeingredient',
        many=True,
        read_only=True,
    )
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return (request
                and request.user.is_authenticated
                and obj.favorite.filter(user=request.user).exists())

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return (request
                and request.user.is_authenticated
                and obj.cart.filter(user=request.user).exists())


class PostIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(
        min_value=MIN_VALUE, max_value=MAX_INGREDIENTS_VALUE,
        error_messages={
            'min_value': 'Минимальное количество ингредиента: 1',
            'max_value': 'Максимальное количество ингредиента: 10000'
        }
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')


class PostRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = PostIngredientSerializer(many=True)
    cooking_time = serializers.IntegerField(
        min_value=MIN_VALUE, max_value=MAX_COOKING_TIME,
        error_messages={
            'min_value': 'Минимальное время приготовления блюда: 1 минута',
            'max_value': 'Максимальное время приготовления блюда: 10000 минут'
        }
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def validate(self, data):
        ingredients = data['ingredients']
        if not ingredients:
            raise serializers.ValidationError({
                'ingredients': 'В рецепте должен быть как '
                               'минимум 1 ингредиент'
            })
        ingredients_ids = [ingredient['id'] for ingredient in ingredients]
        if len(ingredients_ids) != len(set(ingredients_ids)):
            raise serializers.ValidationError(
                'Ингридиенты должны быть уникальными'
            )
        return data

    def validate_tags(self, data):
        tags = self.initial_data.get('tags')
        if not tags:
            raise serializers.ValidationError({
                'tags': 'Нужно выбрать хотя бы один тег'
            })
        if len(tags) != len(set(tags)):
            raise serializers.ValidationError({
                'tags': 'Теги должны быть уникальными'
            })
        return data

    @staticmethod
    def validate_image(data):
        if not data:
            raise serializers.ValidationError({
                'image': 'Нужно добавить изображение'
            })
        return data

    @staticmethod
    def create_ingredients(ingredients, recipe):
        IngredientAmount.objects.bulk_create(
            [IngredientAmount(
                ingredient=ingredient['id'],
                recipe=recipe,
                amount=ingredient['amount']
            ) for ingredient in ingredients]
        )

    def create(self, validated_data):
        request = self.context.get('request')
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.create_ingredients(recipe=instance, ingredients=ingredients)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return GetRecipeSerializer(instance, context=self.context).data


class SmallRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
        read_only_fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = (
            'user',
            'recipe'
        )

    def validate(self, data):
        user = data['user']
        if user.favorite.filter(recipe=data['recipe']).exists():
            raise serializers.ValidationError(
                'Рецепт уже добавлен в избранное.'
            )
        return data


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = (
            'user',
            'recipe'
        )

    def validate(self, data):
        user = data['user']
        if user.cart.filter(recipe=data['recipe']).exists():
            raise serializers.ValidationError(
                'Рецепт уже добавлен в корзину'
            )
        return data
