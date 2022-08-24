import csv

from django.core.management.base import BaseCommand
from django.db import models

from reviews.models import (Category, Comments, Genre, GenreTitle, Review,
                            Title, User)


def importcsv2db(model: models.Model, csv_file: str, field_list: list):
    """Импортирует из файла csv_file в базу модели model
    в field_list - список с именем полей.
    """

    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        row_number = 0
        for row in csvreader:
            if row[0] != 'id':
                try:
                    print(dict(zip(field_list, row)))
                    model.objects.create(**dict(zip(field_list, row)))
                except Exception as err1:
                    print(f'Ошибка импорта строки {row_number}')
                    print(err1)
            row_number += 1


class Command(BaseCommand):
    def handle(self, *args, **options):
        importcsv2db(
            Category,
            'static\\data\\category.csv',
            ['id', 'name', 'slug']
        )
        importcsv2db(
            Genre,
            'static\\data\\genre.csv',
            ['id', 'name', 'slug']
        )
        importcsv2db(
            User,
            'static\\data\\users.csv',
            ['id', 'username', 'email', 'role',
             'bio', 'first_name', 'last_name']
        )
        importcsv2db(
            Title,
            'static\\data\\titles.csv',
            ['id', 'name', 'year', 'category_id']
        )
        importcsv2db(
            GenreTitle,
            'static\\data\\titles.csv',
            ['id', 'title_id', 'genre_id']
        )
        importcsv2db(
            Review,
            'static\\data\\review.csv',
            ['id', 'title_id', 'text', 'author_id', 'score', 'pub_date']
        )
        importcsv2db(
            Comments,
            'static\\data\\comments.csv',
            ['id', 'review_id', 'text', 'author_id', 'pub_date']
        )
