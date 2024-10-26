from django.shortcuts import render
from rest_framework.views import Response
from rest_framework import generics 
from .models import *
from .serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from .models import CashFlow
from .serializers import CashFlowSerializer

class CashFlowListAPIView(generics.ListCreateAPIView):
    serializer_class = CashFlowSerializer

    def get_queryset(self):
        try:
            return CashFlow.objects.all()
        except Exception:
            return CashFlow.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception:
            return Response(
                {"error": "An error occurred while retrieving data."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ExpensesListAPIView(generics.ListCreateAPIView):
    queryset = Expenses.objects.all()
    serializer_class = ExpensesSerializer

class RevenueListAPIView(generics.ListCreateAPIView):
    queryset = Revenue.objects.all()
    serializer_class = RevenueSerializer

class ProfitListAPIView(generics.ListCreateAPIView):
    queryset = Profit.objects.all()
    serializer_class = ProfitSerializer

class BudgetListAPIView(generics.ListCreateAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer

class DebtListAPIView(generics.ListCreateAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer
