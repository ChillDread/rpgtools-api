# -*- coding: utf-8 -*-
"""
Defines the Schema model
"""
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify
from rest_framework import serializers
from .base import Base

SCHEMA_SPECIFICATION = (
    ('Draft-07', 'Draft-07'),
)

SCHEMA_TYPE = (
    ('Form', 'Form'),
    ('Object', 'Object')
)

class Schema(Base):
    """
    Definition for Schema Model
    """
    # Relationships

    # Attributes
    version = models.IntegerField(default=1,
                                  verbose_name='Version')
    document = JSONField(verbose_name='Document',
                         null=True,
                         blank=True)
    form_schema = JSONField(verbose_name='Form Schema',
                            null=True,
                            blank=True)
    specification = models.CharField(max_length=64,
                                     choices=SCHEMA_SPECIFICATION,
                                     default='Draft-07',
                                     verbose_name='Specification')

    # Manager

    # Functions

    # Meta
    class Meta: # pylint: disable=too-few-public-methods
        """
        Model meta data
        """
        db_table = 'schema'
        indexes = [models.Index(fields=['id', 'version'])]
        unique_together = ('id', 'version')
        verbose_name = 'Schema'
        verbose_name_plural = 'Schemas'
        ordering = ('name', )

@receiver(pre_save, sender=Schema)
def set_fields(sender, instance, **kwargs): # pylint: disable=unused-argument
    '''
    Set parameter values to html friendly format
    '''
    instance.id = slugify(instance.name)

class Serializer(serializers.ModelSerializer):
    '''
    Serializer class
    '''
    class Meta: #pylint: disable=too-few-public-methods
        """
        Class meta data
        """
        model = Schema
        fields = ('__all__')

class HrefSerializer(serializers.ModelSerializer):
    '''
    HrefSerializer class
    '''
    document = serializers.SerializerMethodField()
    class Meta: #pylint: disable=too-few-public-methods
        """
        Class meta data
        """
        model = Schema
        fields = ('__all__')

    def get_document(self, schema):
        '''
        return document
        '''
        request = self.context['request']
        # print(request)
        document = schema.document
        document["$id"] = request.build_absolute_uri(reverse(
            "schema_item_version_json", kwargs={'id': schema.id, 'version': schema.version}))
        return document

class DocumentSerializer(HrefSerializer):
    '''
    DocumentSerializer class
    '''
    def to_representation(self, schema): #pylint: disable=arguments-differ
        # print(schema)
        return self.get_document(schema)
