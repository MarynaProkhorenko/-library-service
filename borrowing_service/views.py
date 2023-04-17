from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from borrowing_service.models import Borrowing
from borrowing_service.serializers import BorrowingSerializer, BorrowingListSerializer, BorrowingDetailSerializer
from rest_framework import serializers


class BorrowingPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    pagination_class = BorrowingPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Borrowing.objects.filter(user=self.request.user)

    def get_serializer_class(self) -> type[serializers.Serializer]:
        if self.action == "list":
            return BorrowingListSerializer

        if self.action == "retrieve":
            return BorrowingDetailSerializer

        return BorrowingSerializer

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)
