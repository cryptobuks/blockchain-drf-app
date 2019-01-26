from django.urls import path, include
from rest_framework.routers import DefaultRouter
from transactions.views.transactions import (
    TransactionsViewSet
)


router = DefaultRouter()
router.register('manage', TransactionsViewSet)

app_name = 'transactions'

urlpatterns = [
    path('', include(router.urls)),
]
