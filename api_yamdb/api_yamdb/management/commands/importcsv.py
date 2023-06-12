from django.core.management.base import BaseCommand
from reviews import models
from api_yamdb.settings import CSV_PATH
import os
import csv


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Read categories
        file = os.path.join(CSV_PATH, 'category.csv')
        with open(file, encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                models.Category.objects.update_or_create(
                    id=row[0],
                    defaults={
                        'name': row[1],
                        'slug': row[2]
                    }
                )

        # Read genres
        file = os.path.join(CSV_PATH, 'genre.csv')
        with open(file, encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                models.Genre.objects.update_or_create(
                    id=row[0],
                    defaults={
                        'name': row[1],
                        'slug': row[2]
                    }
                )

        # Read titles
        file = os.path.join(CSV_PATH, 'titles.csv')
        with open(file, encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                category_id = row[3]
                models.Title.objects.update_or_create(
                    id=row[0],
                    defaults={
                        'name': row[1],
                        'year': row[2],
                        'category': models.Category.objects.get(pk=category_id)
                    }
                )

        # Read genre_title
        file = os.path.join(CSV_PATH, 'genre_title.csv')
        with open(file, encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                title_id = row[1]
                title = models.Title.objects.get(pk=title_id)
                genre_id = row[2]
                genre = models.Genre.objects.get(pk=genre_id)
                title.genre.add(genre)

        # Read users
        file = os.path.join(CSV_PATH, 'users.csv')
        with open(file, encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                models.User.objects.get_or_create(
                    id=row[0],
                    username=row[1],
                    email=row[2],
                    role=row[3],
                    bio=row[4],
                    first_name=row[5],
                    last_name=row[6]
                )

        # Read review
        file = os.path.join(CSV_PATH, 'review.csv')
        with open(file, encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                title_id = row[1]
                author_id = row[3]
                models.Review.objects.update_or_create(
                    id=row[0],
                    defaults={
                        'title': models.Title.objects.get(pk=title_id),
                        'text': row[2],
                        'author': models.User.objects.get(pk=author_id),
                        'score': row[4],
                        'pub_date': row[5]
                    }
                )

        # Read comments
        file = os.path.join(CSV_PATH, 'comments.csv')
        with open(file, encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                review_id = row[1]
                author_id = row[3]
                models.Comment.objects.update_or_create(
                    id=row[0],
                    defaults={
                        'author': models.User.objects.get(pk=author_id),
                        'review': models.Review.objects.get(pk=review_id),
                        'text': row[2],
                        'pub_date': row[4]
                    }
                )
