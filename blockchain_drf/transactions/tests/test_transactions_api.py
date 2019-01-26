from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from transactions.models import Transaction
from transactions.serializers.transactions import TransactionsSerializer


TRANSACTIONS_URL = '/api/transactions/manage/'


def create_sample_user(email='test@webapps.agency', password='password123'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


def create_sample_transaction(sender, amount, recipient):
    """Create a sample transaction"""
    return Transaction.objects.create(
        sender=sender, amount=amount,
        recipient=recipient
    )


class TransactionsModelTest(TestCase):
    """Test Transaction model"""
    def test_transaction_str(self):
        """Test the transaction string representation"""
        transaction = Transaction.objects.create(
            sender=create_sample_user(),
            recipient=create_sample_user('user@webapps.agency', 'password467'),
            amount=45.8
        )
        self.assertEqual(str(transaction), str(transaction.signature))


class PublicTransactionsApiTest(TestCase):
    """Test publicly available transactions API access"""
    def setUp(self):
        self.client = APIClient()

    def test_transactions_login_required(self):
        """Test the login is required for retrieving transactions"""
        res = self.client.get(TRANSACTIONS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTransactionsApiTest(TestCase):
    """Testing authorized transactions API access"""
    def setUp(self):
        self.client = APIClient()
        self.user = create_sample_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_transactions(self):
        """Test retrieve transactions"""
        recipient1 = create_sample_user('rec1@webapps.agency', 'pwd12346')
        recipient2 = create_sample_user('rec2@webapps.agency', 'pwd12346')
        create_sample_transaction(
            sender=self.user, amount=78.8,
            recipient=recipient1
        )
        create_sample_transaction(
            sender=self.user, amount=85.5,
            recipient=recipient2
        )
        res = self.client.get(TRANSACTIONS_URL)
        transactions = Transaction.objects.all().order_by('-created_at')
        serializer = TransactionsSerializer(transactions, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_transactions_to_logged_user(self):
        """Test that transactions returned are for the authenticated user"""
        user_sender = create_sample_user('usr3@webapps.agency', 'pwd12346')
        user_recipient = create_sample_user('rec3@webapps.agency', 'pwd12346')
        create_sample_transaction(user_sender, 978.54, user_recipient)
        transaction = create_sample_transaction(
            self.user, 345.87, user_recipient
        )
        res = self.client.get(TRANSACTIONS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['signature'], str(transaction.signature))

    def test_create_transaction_successfull(self):
        """Test create a new transaction"""
        rec_usr = create_sample_user('usr4@webapps.agency')
        payload = {
            'sender': self.user.pk,
            'recipient': rec_usr.pk,
            'amount': 78.9
        }
        self.client.post(TRANSACTIONS_URL, payload)
        exists = Transaction.objects.filter(
            sender=payload['sender'], recipient=payload['recipient'],
            amount=payload['amount']
        ).order_by('-created_at').exists()
        self.assertTrue(exists)
