from django.db import models
from users.models import Organization
from django.core.validators import MinValueValidator
from decimal import Decimal





class BillType(models.Model):
    choices = [('assets', 'assets'), ('liabilities', 'liabilities')]
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=64, choices=choices)
    organization = models.ForeignKey(Organization,  on_delete=models.CASCADE)

class Bill(models.Model):
    type = models.ForeignKey(BillType,  on_delete=models.CASCADE, related_name='bills')
    timestamp = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(
        verbose_name='price of unit', 
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    quantity = models.IntegerField(verbose_name='quantity on the bill')
    


# Yousef Models:

class FinancialReport(models.Model):
    choices = [('csv', 'csv'), ('pdf', 'pdf'), ('excel', 'excel')]
    start_date = models.DateField()
    end_date = models.DateField()
    format_type = models.CharField(max_length=64)
    picture = models.ImageField(upload_to='media/reports/')
    description = models.TextField()
    organization = models.ForeignKey(Organization,  on_delete=models.CASCADE)

class FinancialInsight(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    recommandation = models.TextField()
    organization = models.ForeignKey(Organization,  on_delete=models.CASCADE)




