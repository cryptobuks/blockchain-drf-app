import uuid
from django.db import models
from django.conf import settings


class Transaction(models.Model):
    """The transaction which will be add to a block in the blockchain"""
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='sender_transaction'
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='recipient_transaction'
    )
    amount = models.FloatField(
        null=False,
        blank=False,
        default=0.00
    )
    signature = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        null=False,
        blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.signature)

    class Meta:
        ordering = ['-created_at']
