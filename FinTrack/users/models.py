from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from decimal import Decimal
from django.core.validators import MinValueValidator
 
class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=254, verbose_name='email address')
    password = models.CharField(max_length=128, verbose_name='password')
    username = None
    last_name = models.CharField(max_length=128)
    first_name = models.CharField(max_length=128)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Organization(models.Model):
    title = models.CharField(max_length=128, verbose_name='name of the organization')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organizations')
    # employees = models.ManyToManyField(User, related_name='work_on')

    # Use DecimalField instead of FloatField to allow two decimal places
    capital = models.DecimalField(
        verbose_name='started with capital',
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]  # Optional: ensure non-zero, positive capital
    )

    debt = models.DecimalField(
        verbose_name='now debt',
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]  # Optional: ensure non-negative debt
    )

    def __str__(self):
        return self.title