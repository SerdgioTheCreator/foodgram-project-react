from rest_framework import viewsets

from api.filters import IngredientSearchFilter
from api.permissions import IsAdminOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet
from api.models import Tag, Ingredient, Recipe
from api.serializers import TagSerializer, IngredientSerializer


class TagsViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAdminOrReadOnly, )
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAdminOrReadOnly, )
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter, )
    search_fields = ('^name', )


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
