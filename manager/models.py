from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

ID_TYPES = [
    ('National ID', 'National ID'),
    ('Passport', 'Passport'),
    ('Drivers License', 'Drivers License'),
    ('Company Tax Clearance', 'Company Tax Clearance'),
]


class Country(models.Model):
    """All countries Data"""
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Organisation(models.Model):
    """Property Management Companies or Estate Agents"""
    company_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    phone = models.CharField(max_length=255)
    email = models.EmailField
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name


class UserManager(BaseUserManager):
    """Helps Django work with our custom user model"""

    def create_user(self, email, password=None):
        """Creates a new user """

        if not email:
            raise ValueError('User must have an email address.')

        email = self.normalize_email(email)
        user = self.model(email=email)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser with given details."""

        user = self.create_user(email, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
        Represents a "user" inside our system. Stores all user account related data
    """
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    # REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        """Django uses this when it needs to get the user's full name."""

        return self.first_name + self.last_name

    def get_short_name(self):
        """Django uses this when it needs to get the users abbreviated name."""

        return self.first_name

    def __str__(self):
        """Django uses this when it needs to convert the object to text."""

        return self.email


class PropertyManager(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organisation = models.ForeignKey('Organisation', on_delete=models.CASCADE)
    details = models.TextField(blank=True)

    def __str__(self):
        return self.user


class LandLord(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='country')
    identification_type = models.CharField(max_length=55, choices=ID_TYPES)
    identification = models.CharField(max_length=255)
    nationality = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='nationality')
    bank = models.CharField(max_length=255)
    bank_branch = models.CharField(max_length=255)
    bank_account_number = models.CharField(max_length=255)
    details = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Property(models.Model):
    PROPERTY_TYPES = [
        ('Residential', 'Residential'),
        ('Office', 'Office'),
        ('Industrial', 'Industrial'),
        ('Commercial', 'Commercial'),
        ('Agricultural', 'Agricultural'),

    ]
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    organisation_managing = models.ForeignKey('Organisation', on_delete=models.CASCADE)
    land_lord = models.ForeignKey('LandLord', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    property_value = models.DecimalField(blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    description = models.TextField()
    lot_size = models.DecimalField()
    building_size = models.DecimalField()
    date_added = models.DateTimeField(auto_now=True)
    last_updated = models.DateTimeField(blank=True)
    is_active = models.BooleanField(default=True)
    details = models.TextField(blank=True)

    def __str__(self):
        return self.title


class PropertyUnit(models.Model):
    property = models.ForeignKey('Property', on_delete=models.CASCADE)
    unit_name = models.CharField(max_length=255)
    is_vacant = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    max_number_of_tenants = models.IntegerField(default=1)
    rental_value = models.DecimalField()
    service_fees = models.DecimalField()
    date_added = models.DateTimeField(auto_now=True)
    last_updated = models.DateTimeField(blank=True)
    details = models.TextField(blank=True)

    def __str__(self):
        return self.unit_name


class Tenant(models.Model):
    name = models.CharField(max_length=255)
    property_unit = models.ForeignKey('PropertyUnit', on_delete=models.CASCADE)
    date_of_occupancy = models.DateField()
    identification_type = models.CharField(max_length=55, choices=ID_TYPES)
    identification = models.CharField(max_length=255)
    email = models.EmailField()
    contact_address = models.CharField(max_length=255)
    nationality = models.ForeignKey('Country', on_delete=models.CASCADE)
    tenant_representative = models.CharField(max_length=255, blank=True)
    details = models.TextField(blank=True)

    def __str__(self):
        return self.name


