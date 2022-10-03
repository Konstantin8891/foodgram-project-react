from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
)


class CreateListRetrieveViewSet(
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet
):
    pass


class CreateViewSet(CreateModelMixin, GenericViewSet):
    pass


class DestroyViewSet(DestroyModelMixin, GenericViewSet):
    pass


class CreateDestroyViewSet(
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    pass
