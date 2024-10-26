from rest_framework import serializers
from .models import *

class CashFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlow
        fields = '__all__'

class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = '__all__'

class RevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revenue
        fields = '__all__'

class ProfitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profit
        fields = '__all__'

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'

class DebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debt
        fields = '__all__'

class InvestmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investments
        fields = '__all__'

class FundingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funding
        fields = '__all__'

class FinancialReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialReports
        fields = '__all__'

class AssetsLiabilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetsLiabilities
        fields = '__all__'

class TextInputSerializer(serializers.Serializer):
    text = serializers.CharField(required=True)