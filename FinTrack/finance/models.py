from django.db import models

# # Create your models here.
# class CashFlow(models.Model):
#     date = models.DateField()
#     cash_inflow = models.DecimalField(max_digits=15, decimal_places=2)
#     cash_outflow = models.DecimalField(max_digits=15, decimal_places=2)
#     net_cash_flow = models.DecimalField(max_digits=15, decimal_places=2)
#     description = models.TextField(null=True, blank=True)
#     category = models.CharField(max_length=50, null=True, blank=True)

# class Expenses(models.Model):
#     date = models.DateField()
#     amount = models.DecimalField(max_digits=15, decimal_places=2)
#     expense_category = models.CharField(max_length=50, null=True, blank=True)
#     department = models.CharField(max_length=50, null=True, blank=True)
#     description = models.TextField(null=True, blank=True)

# class Revenue(models.Model):
#     date = models.DateField()
#     amount = models.DecimalField(max_digits=15, decimal_places=2)
#     product_line = models.CharField(max_length=50, null=True, blank=True)
#     customer_type = models.CharField(max_length=50, null=True, blank=True)
#     description = models.TextField(null=True, blank=True)

# class Profit(models.Model):
#     date = models.DateField()
#     revenue = models.DecimalField(max_digits=15, decimal_places=2)
#     expenses = models.DecimalField(max_digits=15, decimal_places=2)
#     net_profit = models.DecimalField(max_digits=15, decimal_places=2)
#     profit_margin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
#     description = models.TextField(null=True, blank=True)

# class Budget(models.Model):
#     fiscal_year = models.CharField(max_length=50)
#     department = models.CharField(max_length=50)
#     allocated_budget = models.DecimalField(max_digits=15, decimal_places=2)
#     spent_budget = models.DecimalField(max_digits=15, decimal_places=2)
#     remaining_budget = models.DecimalField(max_digits=15, decimal_places=2)
#     description = models.TextField(null=True, blank=True)

# class Debt(models.Model):
#     debt_type = models.CharField(max_length=50)
#     principal = models.DecimalField(max_digits=15, decimal_places=2)
#     interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
#     maturity_date = models.DateField(null=True, blank=True)
#     payment_due_date = models.DateField(null=True, blank=True)
#     amount_paid = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
#     outstanding_balance = models.DecimalField(max_digits=15, decimal_places=2)
#     description = models.TextField(null=True, blank=True)

# class Investments(models.Model):
#     investment_type = models.CharField(max_length=50)
#     investment_amount = models.DecimalField(max_digits=15, decimal_places=2)
#     investment_date = models.DateField()
#     returns = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
#     risk_level = models.CharField(max_length=50, null=True, blank=True)
#     current_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
#     description = models.TextField(null=True, blank=True)

# class Funding(models.Model):
#     funding_round = models.CharField(max_length=50)
#     amount_raised = models.DecimalField(max_digits=15, decimal_places=2)
#     date = models.DateField()
#     investor_name = models.CharField(max_length=50, null=True, blank=True)
#     valuation = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
#     description = models.TextField(null=True, blank=True)

# class FinancialReports(models.Model):
#     report_type = models.CharField(max_length=50)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

# class AssetsLiabilities(models.Model):
#     asset_name = models.CharField(max_length=50)
#     asset_value = models.DecimalField(max_digits=15, decimal_places=2)
#     liability_name = models.CharField(max_length=50, null=True, blank=True)
#     liability_value = models.DecimalField(max_digits=15, decimal_places=2)
#     date = models.DateField()
#     description = models.TextField(null=True, blank=True)




from django.db import models

# Create your models here.
class CashFlow(models.Model):
    date = models.DateField()
    cash_inflow = models.DecimalField(max_digits=15, decimal_places=2)
    cash_outflow = models.DecimalField(max_digits=15, decimal_places=2)
    net_cash_flow = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "CashFlow"

class Expenses(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    expense_category = models.CharField(max_length=50, null=True, blank=True)
    department = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "Expenses"

class Revenue(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    product_line = models.CharField(max_length=50, null=True, blank=True)
    customer_type = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "Revenue"

class Profit(models.Model):
    date = models.DateField()
    revenue = models.DecimalField(max_digits=15, decimal_places=2)
    expenses = models.DecimalField(max_digits=15, decimal_places=2)
    net_profit = models.DecimalField(max_digits=15, decimal_places=2)
    profit_margin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "Profit"

class Budget(models.Model):
    fiscal_year = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    allocated_budget = models.DecimalField(max_digits=15, decimal_places=2)
    spent_budget = models.DecimalField(max_digits=15, decimal_places=2)
    remaining_budget = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "Budget"

class Debt(models.Model):
    debt_type = models.CharField(max_length=50)
    principal = models.DecimalField(max_digits=15, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    maturity_date = models.DateField(null=True, blank=True)
    payment_due_date = models.DateField(null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    outstanding_balance = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "Debt"

class Investments(models.Model):
    investment_type = models.CharField(max_length=50)
    investment_amount = models.DecimalField(max_digits=15, decimal_places=2)
    investment_date = models.DateField()
    returns = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    risk_level = models.CharField(max_length=50, null=True, blank=True)
    current_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "Investments"

class Funding(models.Model):
    funding_round = models.CharField(max_length=50)
    amount_raised = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField()
    investor_name = models.CharField(max_length=50, null=True, blank=True)
    valuation = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "Funding"

class FinancialReports(models.Model):
    report_type = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "FinancialReports"

class AssetsLiabilities(models.Model):
    asset_name = models.CharField(max_length=50)
    asset_value = models.DecimalField(max_digits=15, decimal_places=2)
    liability_name = models.CharField(max_length=50, null=True, blank=True)
    liability_value = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField()
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "AssetsLiabilities"


 