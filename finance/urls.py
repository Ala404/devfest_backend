from django.urls import path
from .views import *
from .tools_prediction import *
from .query_set import *


urlpatterns = [
    path('cashflow/', CashFlowListAPIView.as_view(), name='cashflow-list'),
    path('expenses/', ExpensesListAPIView.as_view(), name='expenses-list'),
    path('revenue/', RevenueListAPIView.as_view(), name='revenue-list'),
    path('profit/', ProfitListAPIView.as_view(), name='profit-list'),
    path('budget/', BudgetListAPIView.as_view(), name='budget-list'),
    path('debt/', DebtListAPIView.as_view(), name='debt-list'),
    # predict_fututre values
    # http://127.0.0.1:8000/finance/forecast/?model=CashFlow&feature=net_cash_flow
    path("forecast/", SarimaForecastView.as_view(), name="sarima_forecast"),
    # interpretaction of historical and prediction values
    # http://127.0.0.1:8000/finance/interpretation/?model=CashFlow&feature=net_cash_flow
    path("interpretation/", GeminiForecastInterpretationView.as_view()),

    path('chat/', requestAnalyst.as_view(), name='coherence-analysis'),




]
