from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from PIL import Image
import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import reverse


class User(AbstractUser):
    GENDER_CHOICES = (('Male', 'Male'),
                      ('Female', 'Female'))
    bio = models.CharField(max_length=500, blank=True)
    male = models.CharField(max_length=10, choices=GENDER_CHOICES)
    photo = models.ImageField(default='ProfilePicture/default.jpg', upload_to='ProfilePicture/')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()

        img = Image.open(self.photo.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)

    def __str__(self):
        return self.username

    @property
    def group(self):
        groups = self.groups.all()
        return groups[0].name if groups else None


class Car(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='new_car', null=True)
    car_model = models.ForeignKey('core.Model', on_delete=models.CASCADE, related_name='new_car')
    car_type = models.ForeignKey('core.Type', on_delete=models.CASCADE, related_name='new_car')
    car_number = models.ForeignKey('core.CarNumber', on_delete=models.CASCADE, related_name='new_car')

    def __str__(self):
        return f'{self.car_number}:{self.car_model}({self.car_type})'


class Model(models.Model):
    car_brand = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.car_brand}:{self.car_model}'


class Type(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type


class CarNumber(models.Model):
    number = models.CharField(max_length=4)
    series = models.CharField(max_length=2)
    region = models.ForeignKey('address.State', on_delete=models.CASCADE, related_name='cars_numbers')

    def save(self, *args, **kwargs):
        self.series = self.series.upper()
        return super(CarNumber, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.number}{self.series}-{self.region.code}'


class Trip(models.Model):
    REQUESTED = 'REQUESTED'
    STARTED = 'STARTED'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    STATUSES = (
        (REQUESTED, REQUESTED),
        (STARTED, STARTED),
        (IN_PROGRESS, IN_PROGRESS),
        (COMPLETED, COMPLETED),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    pick_up_address = models.CharField(max_length=255)
    drop_off_address = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUSES, default=REQUESTED)
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='trips_as_driver'
    )
    rider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='trips_as_rider'
    )

    def __str__(self):
        return f'{self.id}'

    def get_absolute_url(self):
        return reverse('trip:trip_detail', kwargs={'trip_id': self.id})
