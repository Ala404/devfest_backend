# Generated by Django 5.1.2 on 2024-10-25 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssetsLiabilities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_name', models.CharField(max_length=50)),
                ('asset_value', models.DecimalField(decimal_places=2, max_digits=15)),
                ('liability_name', models.CharField(blank=True, max_length=50, null=True)),
                ('liability_value', models.DecimalField(decimal_places=2, max_digits=15)),
                ('date', models.DateField()),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fiscal_year', models.CharField(max_length=50)),
                ('department', models.CharField(max_length=50)),
                ('allocated_budget', models.DecimalField(decimal_places=2, max_digits=15)),
                ('spent_budget', models.DecimalField(decimal_places=2, max_digits=15)),
                ('remaining_budget', models.DecimalField(decimal_places=2, max_digits=15)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CashFlow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('cash_inflow', models.DecimalField(decimal_places=2, max_digits=15)),
                ('cash_outflow', models.DecimalField(decimal_places=2, max_digits=15)),
                ('net_cash_flow', models.DecimalField(decimal_places=2, max_digits=15)),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Debt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debt_type', models.CharField(max_length=50)),
                ('principal', models.DecimalField(decimal_places=2, max_digits=15)),
                ('interest_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('maturity_date', models.DateField(blank=True, null=True)),
                ('payment_due_date', models.DateField(blank=True, null=True)),
                ('amount_paid', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('outstanding_balance', models.DecimalField(decimal_places=2, max_digits=15)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('expense_category', models.CharField(blank=True, max_length=50, null=True)),
                ('department', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FinancialReports',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_type', models.CharField(max_length=50)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Funding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('funding_round', models.CharField(max_length=50)),
                ('amount_raised', models.DecimalField(decimal_places=2, max_digits=15)),
                ('date', models.DateField()),
                ('investor_name', models.CharField(blank=True, max_length=50, null=True)),
                ('valuation', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Investments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('investment_type', models.CharField(max_length=50)),
                ('investment_amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('investment_date', models.DateField()),
                ('returns', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('risk_level', models.CharField(blank=True, max_length=50, null=True)),
                ('current_value', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('revenue', models.DecimalField(decimal_places=2, max_digits=15)),
                ('expenses', models.DecimalField(decimal_places=2, max_digits=15)),
                ('net_profit', models.DecimalField(decimal_places=2, max_digits=15)),
                ('profit_margin', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Revenue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('product_line', models.CharField(blank=True, max_length=50, null=True)),
                ('customer_type', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
