import re
import datetime as dt

from rest_framework import serializers
from reviews.models import Title, Category, Genre, Review, Comment
from django.shortcuts import get_object_or_404
from django.core.validators import EmailValidator

from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class ReadTitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category', 'rating')

    def get_rating(self, obj):
        sum = 0
        reviews = obj.reviews.all()
        for review in reviews:
            sum += review.score
        if sum == 0:
            return None
        return sum / len(reviews)


class WriteTitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug', queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def validate_year(self, value):
        if value > dt.date.today().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!'
            )
        return value

    def create(self, validated_data):
        category_slug = validated_data.pop('category')
        genre_slugs = validated_data.pop('genre')
        category = get_object_or_404(Category, slug=category_slug)
        title = Title.objects.create(**validated_data, category=category)
        genres = Genre.objects.filter(slug__in=genre_slugs)
        for genre in genres:
            title.genre.add(genre)
            title.save()
        return title


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True)
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')
        extra_kwargs = {
            'email': {
                'validators': [
                    EmailValidator()
                ]
            }
        }

    def validate_username(self, value):
        regex = re.compile(r'^[\w.@+-]+\Z')
        if not regex.match(value):
            raise serializers.ValidationError('Incorrect username')
        if value == 'me':
            raise serializers.ValidationError(
                'Restricted to use "me" as username'
            )
        return value

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if user and user.username != username:
            raise serializers.ValidationError(
                {'email': 'This email is already taken.'}
            )
        return data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author',)

    def validate(self, data):
        if self.context.get('request').method != 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                {'unique_error': 'You can only have one review on title.'}
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('author',)


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'role', 'bio',)

    def validate_username(self, value):
        regex = re.compile(r'^[\w.@+-]+\Z')
        if not regex.match(value):
            raise serializers.ValidationError('Incorrect username')
        return value
