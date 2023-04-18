from rest_framework import routers
from django.urls import path, include

from borrowing_service.views import BorrowingViewSet

router = routers.DefaultRouter()
router.register("borrowings", BorrowingViewSet, basename="borrowings")

urlpatterns = [path("", include(router.urls))]

app_name = "borrowing_service"
