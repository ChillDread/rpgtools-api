# -*- coding: utf-8 -*-
"""
Defines the user and group views
"""
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from api.serializers.user_group import UserSerializer
from api.serializers.user_group import GroupSerializer
from api.permissions.admin import IsAdminOrReadOnly


class UserViewSet(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = (IsAdminOrReadOnly,)
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
