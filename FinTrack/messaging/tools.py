# from transformers import pipeline
# import pyjokes
# import pickle
# from random import randint

from messaging.models import Bill, BillType
import itertools



# def financial_data(organization):
#     bill_types = BillType.objects.filter(organization=organization)
#     bills = Bill.objects.filter(type__organization=organization)
#     assets = [bill_type.id for bill_type in bill_types if bill_type.type == 'assets']
#     liabilities = [bill_type.id for bill_type in bill_types if bill_type.type == 'liabilities']
#     assets_bills = [bill.id for bill in bills if bill.type.id in assets]
#     liabilities_bills = [bill.id for bill in bills if bill.type.id in liabilities]


#     return(liabilities_bills)

from django.db.models import Sum, F, Case, When, DecimalField
from django.db.models.functions import TruncDate

def financial_date(organization_id):
    # Filter bills related to the given organization and group by day
    assets_and_liabilities_per_day = (
        Bill.objects.filter(type__organization_id=organization_id)
        .annotate(day=TruncDate('timestamp'))  # Group by day
        .values('day')  # Keep the day in the results
        .annotate(
            revenue=Sum(
                Case(
                    When(type__type='assets', then=F('price') * F('quantity')),
                    default=0, output_field=DecimalField()  # Use DecimalField() directly
                )
            ),
            expenses=Sum(
                Case(
                    When(type__type='liabilities', then=F('price') * F('quantity')),
                    default=0, output_field=DecimalField()  # Use DecimalField() directly
                )
            ),
        )
        .annotate(profit=F('revenue') - F('expenses'))  # Calculate profit
        .order_by('day')  # Order by day
    )
    
    return list(assets_and_liabilities_per_day)

