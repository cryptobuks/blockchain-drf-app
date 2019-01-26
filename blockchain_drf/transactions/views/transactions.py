from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from transactions.models.transaction import Transaction
from transactions.serializers.transactions import TransactionsSerializer


class TransactionsViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin,
                          mixins.CreateModelMixin):
    """Manage transactions on Db"""
    queryset = Transaction.objects.all()
    serializer_class = TransactionsSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Returns objects for the current authenticated user only"""
        return self.queryset.filter(
            sender=self.request.user
        ).order_by('-created_at')
