from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import *
import datetime

User = get_user_model()


class ModelTestCase(TestCase):
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

    def test_category_creation(self):
        self.assertEqual(Category.objects.count(), 1)

    def test_shift_creation(self):
        self.assertEqual(Shift.objects.count(), 1)

    def test_service_creation(self):
        self.assertEqual(Service.objects.count(), 1)

    def test_reservation_creation(self):
        self.assertEqual(Reservation.objects.count(), 1)

    def test_item_creation(self):
        self.assertEqual(Item.objects.count(), 1)

    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 1)

    def test_category_name_max_length(self):
        max_length = self.category._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_shift_string_representation(self):
        shift_str = f'{self.shift.start_date}-{self.shift.end_date} {self.shift.id}'
        self.assertEqual(str(self.shift), shift_str)

    def test_service_string_representation(self):
        service_str = f'{self.service.name} - {self.service.subtitle} - duration: {self.service.duration}'
        self.assertEqual(str(self.service), service_str)

    def test_reservation_string_representation(self):
        reservation_str = f'{self.reservation.reserver.username} {self.reservation.service}'
        self.assertEqual(str(self.reservation), reservation_str)

    def test_item_string_representation(self):
        self.assertEqual(str(self.item), 'Test Item')

    def test_user_string_representation(self):
        user_str = f'{self.user.username} {self.user.id}'
        self.assertEqual(str(self.user), user_str)



#------------------------ admin page ------------------------------



from django.test import TestCase, Client
from django.contrib.admin.sites import AdminSite
from django.urls import reverse
from django.contrib.auth import get_user_model
from .admin import ItemAdmin, ShiftAdmin, ShiftArchiveAdmin, ServiceAdmin, ReservationArchiveAdmin, ReservationAdmin, UserAdminCustom
from .models import Item, Shift, Service, Reservation, Category

User = get_user_model()


class AdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.site = AdminSite()

        # Create a superuser for authentication
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass'
        )

        self.client.force_login(self.admin_user)

    def test_item_admin_list_display(self):
        item = Item.objects.create(
            name='Test Item',
            category=Category.objects.create(name='Test Category')
        )

        model_admin = ItemAdmin(Item, self.site)
        list_display = model_admin.get_list_display(request=None)

        self.assertEqual(list_display, (
            'first_name',
            'last_name',
            'category'
        ))

    def test_shift_admin_list_display(self):
        shift = Shift.objects.create(
            start_date='2022-01-01 08:00:00',
            end_date='2022-01-01 10:00:00',
            item=Item.objects.create(name='Test Item')
        )

        model_admin = ShiftAdmin(Shift, self.site)
        list_display = model_admin.get_list_display(request=None)

        self.assertEqual(list_display, (
            'start_date',
            'end_date',
            'item',
            'get_category'
        ))


    def test_admin_page_accessible(self):
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)



    def test_service_admin_list_display(self):
        service = Service.objects.create(
            name='Test Service',
            subtitle='Test Subtitle',
            price=10.99
        )

        model_admin = ServiceAdmin(Service, self.site)
        list_display = model_admin.get_list_display(request=None)

        self.assertEqual(list_display, (
            'name',
            'subtitle',
            'price'
        ))

    def test_reservation_archive_admin_list_display(self):
        reservation = Reservation.objects.create(
            item=Item.objects.create(name='Test Item'),
            reserver=User.objects.create(username='testuser'),
            time_date='2022-01-01 09:00:00',
            code='ABC123',
            is_archive=True
        )

        model_admin = ReservationArchiveAdmin(Reservation, self.site)
        list_display = model_admin.get_list_display(request=None)

        self.assertEqual(list_display, (
            'item',
            'reserver',
            'time_date',
            'code'
        ))

    def test_reservation_admin_list_display(self):
        reservation = Reservation.objects.create(
            item=Item.objects.create(name='Test Item'),
            reserver=User.objects.create(username='testuser'),
            time_date='2022-01-01 09:00:00',
            code='ABC123',
            is_archive=False,
            status='accepted'
        )

        model_admin = ReservationAdmin(Reservation, self.site)
        list_display = model_admin.get_list_display(request=None)

        self.assertEqual(list_display, (
            'item',
            'reserver',
            'time_date',
            'code'
        ))

    def test_user_admin_list_display(self):
        user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            phone_number='1234567890'
        )

        model_admin = UserAdminCustom(User, self.site)
        list_display = model_admin.get_list_display(request=None)

        self.assertEqual(list_display, (
            'username',
            'email',
            'phone_number'
        ))
