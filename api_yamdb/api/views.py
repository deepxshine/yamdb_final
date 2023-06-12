from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from .filters import TitleFilter
from .permissions import AdminOrReadOnly, AdminUser, IsAdminOrModeratorOrOwner
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, GetTokenSerializer,
                          ReadTitleSerializer, ReviewSerializer,
                          SignUpSerializer, UsersSerializer,
                          WriteTitleSerializer)
from .viewsets import CreateListDestroyViewSet


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = [AdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return WriteTitleSerializer
        return ReadTitleSerializer


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['name']


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['name']


class GetToken(APIView):

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(User, username=data['username'])
        if default_token_generator.check_token(
                user, data.get('confirmation_code')
        ):
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Вы ввели некорректный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)


class SignUp(APIView):

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        user = User.objects.filter(username=username, email=email).first()
        if not user:
            serializer = SignUpSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            serializer = SignUpSerializer(user)
        confirmation_code = default_token_generator.make_token(user)
        email_body = (
            f'Добрый день, {user.username}.\n'
            f'Ваш код подтверждения: {confirmation_code}'
        )
        send_mail(
            'Код подтверждения для доступа к API!',
            message=email_body,
            from_email='admin@example.com',
            recipient_list=[user.email],
            fail_silently=False
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class PatchDelAdminModeratorOwnerViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action in ["partial_update", "destroy"]:
            return [
                permissions.IsAuthenticated(),
                IsAdminOrModeratorOrOwner()
            ]
        return [permissions.IsAuthenticatedOrReadOnly()]


class ReviewViewSet(PatchDelAdminModeratorOwnerViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(PatchDelAdminModeratorOwnerViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (permissions.IsAuthenticated, AdminUser)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
        url_path='me')
    def user_info(self, request):
        data = request.data.copy()
        if 'role' in data:
            data.pop('role')
        serializer = UsersSerializer(
            request.user,
            data=data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
