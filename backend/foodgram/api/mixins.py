from re import L
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
)


class CreateListRetrieveViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    pass

