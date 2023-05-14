from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import *

class ItemViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_items(self):
        url = reverse('item-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_item(self):
        item = Item.objects.create(name='Test Item')
        url = reverse('item-detail', args=[item.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_item(self):
        url = reverse('item-list')
        data = {'name': 'New Item'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_item(self):
        item = Item.objects.create(name='Old Name')
        url = reverse('item-detail', args=[item.pk])
        data = {'name': 'New Name'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'New Name')

    def test_delete_item(self):
        item = Item.objects.create(name='Test Item')
        url = reverse('item-detail', args=[item.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Item.objects.filter(pk=item.pk).exists())

    # Add more tests as needed


class ShiftViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_shifts(self):
        url = reverse('shift-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_shift(self):
        shift = Shift.objects.create()
        url = reverse('shift-detail', args=[shift.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_shift(self):
        url = reverse('shift-list')
        data = {}  # Add the required data for creating a shift
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_shift(self):
        shift = Shift.objects.create()
        url = reverse('shift-detail', args=[shift.pk])
        data = {}  # Add the data to update the shift
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add assertions for updated data

    def test_delete_shift(self):
        shift = Shift.objects.create()
        url = reverse('shift-detail', args=[shift.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Shift.objects.filter(pk=shift.pk).exists())

    # Add more tests as needed


class ReservationViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_reservations(self):
        url = reverse('reservation-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_reservation(self):
        reservation = Reservation.objects.create()
        url = reverse('reservation-detail', args=[reservation.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_reservation(self):
        url = reverse('reservation-list')
        data = {}  # Add the required data for creating a reservation
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_reservation(self):
        reservation = Reservation.objects.create()
        url = reverse('reservation-detail', args=[reservation.pk])
        data = {}  # Add the data to update the reservation
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add assertions for updated data

    def test_delete_reservation(self):
        reservation = Reservation.objects.create()
        url = reverse('reservation-detail', args=[reservation.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Reservation.objects.filter(pk=reservation.pk).exists())

    # Add more tests as needed




#--------------------------------serializers-----------------------------------------



from django.test import TestCase
from core.models import Item, Shift, Reservation, Service, Category
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .serializers import *

User = get_user_model()


class SerializerTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.service = Service.objects.create(
            name='Test Service', duration=datetime.timedelta(minutes=15), price=10.0
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            phone_number='1234567890',
        )
        self.item = Item.objects.create(
            name='Test Item',
            category=self.category,
            description='Test Description',
        )
        self.shift = Shift.objects.create(
            item=self.item,
            is_available=True,
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now() + datetime.timedelta(hours=1),
            repeat='do not repeat',
            n_time_repeat=1,
        )
        self.reservation = Reservation.objects.create(
            reserver=self.user,
            item=self.item,
            shift=self.shift,
            service=self.service,
            time_date=datetime.datetime.now(),
            code='ABC123',
        )

    def test_item_serializer(self):
        serializer = ItemSerializer(instance=self.item)
        expected_fields = ['id', 'name', 'category', 'description', 'image', 'experience', 'phone_number', 'last_name', 'first_name']
        self.assertEqual(set(serializer.data.keys()), set(expected_fields))

    def test_category_serializer(self):
        serializer = CategorySerializer(instance=self.category)
        expected_fields = ['id', 'name']
        self.assertEqual(set(serializer.data.keys()), set(expected_fields))

    def test_shift_serializer(self):
        serializer = ShiftSerializer(instance=self.shift)
        expected_fields = ['id', 'start_date', 'end_date', 'repeat', 'shift', 'services', 'item', 'is_available']
        self.assertEqual(set(serializer.data.keys()), set(expected_fields))

    def test_reservation_serializer(self):
        serializer = ReservationSerializer(instance=self.reservation)
        expected_fields = ['id', 'reserver', 'time_date', 'service', 'shift', 'item', 'code', 'status']
        self.assertEqual(set(serializer.data.keys()), set(expected_fields))

    def test_service_serializer(self):
        serializer = ServiceSerializer(instance=self.service)
        expected_fields = ['id', 'name', 'duration', 'price', 'subtitle']
        self.assertEqual(set(serializer.data.keys()), set(expected_fields))

    def test_custom_user_serializer(self):
        serializer = CustomUserSerializer(instance=self.user)
        expected_fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number']
        self.assertEqual(set(serializer.data.keys()), set(expected_fields))

    def test_custom_user_create_serializer(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'phone_number': '0987654321',
        }
        serializer = CustomUserCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        validated_data = serializer.validated_data
        self.assertEqual(validated_data['username'], 'newuser')
        self.assertEqual(validated_data['email'], 'newuser@example.com')
        self.assertEqual(validated_data['phone_number'], '0987654321')

    def test_time_serializer(self):
        data = {'time': datetime.time(hour=9, minute=30)}
        serializer = TimeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        validated_data = serializer.validated_data
        self.assertEqual(validated_data['time'], datetime.time(hour=9, minute=30))


        self.assertEqual(validated_data['time'], datetime.time(hour=9, minute=30))


# Add the following tests to the SerializerTestCase class

    def test_custom_user_serializer(self):
        serializer = CustomUserSerializer(instance=self.user)
        expected_fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number']
        self.assertEqual(set(serializer.data.keys()), set(expected_fields))

    def test_custom_user_create_serializer(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'phone_number': '0987654321',
        }
        serializer = CustomUserCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        validated_data = serializer.validated_data
        self.assertEqual(validated_data['username'], 'newuser')
        self.assertEqual(validated_data['email'], 'newuser@example.com')
        self.assertEqual(validated_data['phone_number'], '0987654321')

    def test_time_serializer(self):
        data = {'time': datetime.time(hour=9, minute=30)}
        serializer = TimeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        validated_data = serializer.validated_data
        self.assertEqual(validated_data['time'], datetime.time(hour=9, minute=30))



#----------------------sending email -------------------------------

from django.test import TestCase
from unittest.mock import patch
from . import send_mail

class EmailSendingTestCase(TestCase):
    @patch('smtplib.SMTP')
    def test_send_mail(self, mock_smtp):
        from_email = 'sender@example.com'
        to_emails = ['recipient@example.com']
        subject = 'Test Email'
        html = 'ABC123'

        send_mail(html, subject=subject, from_email=from_email, to_emails=to_emails)

        # Assert that the SMTP instance was called with the correct arguments
        mock_smtp.assert_called_once_with(host='smtp.gmail.com', port=587)
        smtp_instance = mock_smtp.return_value
        smtp_instance.ehlo.assert_called_once()
        smtp_instance.starttls.assert_called_once()
        smtp_instance.login.assert_called_once_with(username=globals.USERNAME, password=globals.PASSWORD)
        smtp_instance.sendmail.assert_called_once_with(from_email, to_emails, mock_smtp.return_value.sendmail.return_value)
        smtp_instance.quit.assert_called_once()
