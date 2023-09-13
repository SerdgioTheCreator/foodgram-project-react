import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Tag

DATA_ROOT = os.path.join(settings.BASE_DIR, 'data')


class Command(BaseCommand):
    help = 'Загрузка ингредиентов и тегов из папки data в формате json'

    def add_arguments(self, parser):
        parser.add_argument('ingredients', default='ingredients.json', nargs='?',
                            type=str)
        parser.add_argument('tags', default='tags.json', nargs='?',
                            type=str)

    def handle(self, *args, **options):
        with open(os.path.join(DATA_ROOT, options['ingredients']), 'r',
                  encoding='utf-8') as f:
            data = json.load(f)
            print('Загрузка ингредиентов и тегов началась')
            counter = 0
            for ingredient in data:
                Ingredient.objects.get_or_create(
                    name=ingredient['name'],
                    measurement_unit=ingredient['measurement_unit']
                )
                if True:
                    counter += 1
            if counter == 0:
                print('Список ингредиентов пуст')
            print(f'{counter} ингредиентов было загружено')
        with open(os.path.join(DATA_ROOT, options['tags']), 'r',
                  encoding='utf-8') as f:
            data = json.load(f)
            counter = 0
            for tag in data:
                Tag.objects.get_or_create(
                    name=tag['name'],
                    color=tag['color'],
                    slug=tag['slug']
                )
                if True:
                    counter += 1
            if counter == 0:
                print('Список тегов пуст')
            print(f'{counter} тегов было загружено')
        print('Загрузка ингредиентов и тегов завершена')
