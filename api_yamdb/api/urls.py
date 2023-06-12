from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import (
    TitleViewSet, CategoryViewSet, GenreViewSet, SignUp, GetToken,
    ReviewViewSet, CommentViewSet, UsersViewSet
)


router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'titles', TitleViewSet, basename='title')
router.register(
    r'^titles/(?P<title_id>[0-9]+)/reviews',
    ReviewViewSet,
    basename='review'
)
router.register(
    r'^titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentViewSet, basename='comment'
)
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', SignUp.as_view(), name='signup'),
    path('v1/auth/token/', GetToken.as_view(), name='login'),
    path('v1/', include(router.urls)),
]
