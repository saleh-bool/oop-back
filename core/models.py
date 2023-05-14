import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import m2m_changed
from django.utils.crypto import get_random_string
import datetime



def get_random_string_me():
    c = get_random_string(length=9)
    return c


def upload_item_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{instance.name}.{ext}'
    return os.path.join('uploads/item', filename)






class User(AbstractUser):

    phone_number = models.CharField(max_length=20)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    def __str__(self) -> str:
        return self.username + ' ' + str(self.id)


class Category(models.Model):
    """tags for items in order to categorize them"""
    
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Shift(models.Model):

    RepeatType = [
        ('do not repeat', 'do not repeat'),
        ('every week', 'every week' ),
        ('every 2 weeks', 'every 2 weeks' ),
        ('every month', 'every month' ),
        ('every 2 months', 'every 2 months' ),
    ]

    item = models.ForeignKey('Item', on_delete=models.CASCADE, null=True)
    is_available = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    repeat = models.CharField(max_length=100, choices=RepeatType)
    shift = models.ForeignKey('Shift', on_delete= models.CASCADE, null=True, blank=True, related_name='repeatShifts')
    n_time_repeat = models.IntegerField(default=1)
    services = models.ManyToManyField('Service')
    is_archive = models.BooleanField(default=False)

    def __str__(self):
        return  str(self.start_date) + '-' + str(self.end_date) + str(self.id)


class Service(models.Model):
    name = models.CharField(max_length=100)
    duration = models.DurationField(default=datetime.timedelta(minutes=15))
    price = models.DecimalField(max_digits=10, decimal_places=2)


    subtitle = models.CharField(max_length=50, null=True)

    def __str__(self) -> str:
        return self.name +  "- " + str(self.subtitle) +  " - duration: " + str(self.duration) 


class Reservation(models.Model):

    STATUS_TYPES = (
        ('review','review'),
        ('accepted', 'accepted'),
        ('not accepted', 'not accepted')
    )

    reserver = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE, null=True)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, null=True)
    service = models.ForeignKey('Service', on_delete=models.CASCADE, null=True)
    time_date = models.DateTimeField()
    code = models.CharField(default=get_random_string_me, max_length=9)

    status = models.CharField(max_length=20, choices=STATUS_TYPES, default='review')
    is_archive = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.reserver.username + " " + str(self.service)


class ReservationArchive(Reservation):
    class Meta:
        proxy = True


class Item(models.Model):

    name = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_item_image_path, null=True, blank=True)
    experience = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class ShiftArchive(Shift):
    class Meta:
        proxy = True

# add n_time_repeat more shifts depending on the repeat
def update_item(sender, instance, action, **kwargs):
    if action == 'post_add':
        st = instance.start_date
        en = instance.end_date
        if instance.repeat != 'do not repeat':
            for i in range(instance.n_time_repeat):
                if instance.repeat == 'every week':
                    st = st + datetime.timedelta(days=7)
                    en = en + datetime.timedelta(days=7)
                elif instance.repeat == 'every 2 weeks':
                    st = st + datetime.timedelta(days=14)
                    en = en + datetime.timedelta(days=14)
                elif instance.repeat == 'every month':
                    st = st + datetime.timedelta(days=30)
                    en = en + datetime.timedelta(days=30)
                elif instance.repeat == 'every 2 months':
                    st = st+ datetime.timedelta(days=60)
                    en = en + datetime.timedelta(days=60)
                s = Shift.objects.create(
                    item=instance.item,
                    start_date=st,
                    end_date=en,
                    repeat= 'do not repeat',
                    n_time_repeat = 0,
                    shift = instance,
                )

                for t in instance.services.all():
                    s.services.add(t)

m2m_changed.connect(update_item, sender=Shift.services.through)