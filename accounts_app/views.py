from rest_framework import permissions
from rest_framework import generics
from django.contrib.auth import get_user_model
from django.db.models import Count

from .serializers import UserSerializer, UserCountPostSerializer


class CreateUserAPIView(generics.CreateAPIView):
    """
    Registers a user by fields username and password.
    """
    model = get_user_model()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer


class ListUsersAPIView(generics.ListAPIView):
    """
    Get all users and added field "count_post".
    Filter by url parameter, example - /?count_post=1
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserCountPostSerializer

    def get_queryset(self):
        count_post = self.request.query_params.get('count_post')

        if count_post is None:
            return get_user_model().objects.annotate(
                count_post=Count('post')
            )
        else:
            return get_user_model().objects.annotate(
                count_post=Count('post')
            ).filter(count_post=count_post)
