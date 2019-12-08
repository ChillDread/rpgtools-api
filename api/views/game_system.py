# -*- coding: utf-8 -*-
"""
Defines the GameSystem views
"""
from django.utils.text import slugify
from rest_framework import generics
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from api.models.game_system import GameSystem
from api.models.game_system import Serializer
from api.models.game_system import HyperLinkedSerializer
from api.models.game_system import GameSystemHistorySerializer
from api.permissions.admin import IsAdminOrReadOnly


class ItemView(generics.RetrieveAPIView): # pylint: disable=too-many-ancestors
    '''
    Provides access to the DELETE, GET, PATCH and PUT requests for a given ID.
    '''    
    queryset = GameSystem.objects.all()
    serializer_class = HyperLinkedSerializer
    lookup_field = "id"

class ItemEditView(generics.UpdateAPIView): # pylint: disable=too-many-ancestors
    '''
    Provides access to the PATCH and PUT requests for a given ID.
    '''
    permission_classes = (IsAdminUser,)
    queryset = GameSystem.objects.all()
    serializer_class = Serializer
    lookup_field = "id"

class ItemDeleteView(generics.DestroyAPIView): # pylint: disable=too-many-ancestors
    '''
    Provides access to the DELETE requests for a given ID.
    '''
    permission_classes = (IsAdminUser,)
    queryset = GameSystem.objects.all()
    serializer_class = Serializer
    lookup_field = "id"

class ListView(generics.ListAPIView):
    '''
    Provides access to the GET request for a list of all game objects.
    '''
    queryset = GameSystem.objects.all()
    serializer_class = Serializer

class CreateView(generics.CreateAPIView):
    '''
     Provides access to the POST request for creating game objects.
    '''
    permission_classes = (IsAdminUser,)
    queryset = GameSystem.objects.all()
    serializer_class = Serializer

    def create(self, request, *args, **kwargs):
        name = request.data['name']
        id = slugify(name) # pylint: disable=redefined-builtin, invalid-name

        queryset = GameSystem.objects.filter(id=id)

        if queryset.count() != 0:
            detail = 'A Game System entry already exists with the id '+id
            raise serializers.ValidationError(detail)

        return super(CreateView, self).create(request, *args, **kwargs)

class GameSystemHistoryView(generics.RetrieveAPIView):
    """Get game system history by name"""
    serializer_class = GameSystemHistorySerializer
    queryset = GameSystem.objects.all()
    lookup_field = "id"
