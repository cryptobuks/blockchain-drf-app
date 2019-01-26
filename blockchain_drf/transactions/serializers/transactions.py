from rest_framework.serializers import (
    ModelSerializer
)
from transactions.models.transaction import Transaction
# from core.models.user import User


class TransactionsSerializer(ModelSerializer):
    """Serializer for transaction objects"""
    # sender = PrimaryKeyRelatedField(
    #     many=False,
    #     queryset=User.objects.all()
    # )
    # recipient = PrimaryKeyRelatedField(
    #     many=False,
    #     queryset=User.objects.all()
    # )

    class Meta:
        model = Transaction
        fields = (
            'id', 'sender', 'recipient',
            'amount', 'signature', 'created_at'
        )
        ready_only_fields = ('id',)
