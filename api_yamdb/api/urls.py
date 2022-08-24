from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, CommentsViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet)
from users.views import AccessTokenView, UserTokenViewSet, UserViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'auth/signup', UserTokenViewSet, basename='sign_up')
router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path(
        'v1/auth/token/',
        AccessTokenView.as_view(),
        name='token_obtain'
    )
]
