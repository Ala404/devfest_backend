from django.urls import path
from .views import *


urlpatterns = [
    path('bills/', BillAPIView.as_view()),
    path('bill_types/', BillTypeAPIView.as_view()),
    path('financial_data/', FinancialDateAPIView.as_view()),
    path('financial_data_report/', FinancialDataReportingAPIView.as_view()),

]



    # path('sessions/', views.SessionViews.as_view()),
    # path('patient_sessions/<int:id>/', views.PatientSessionViews.as_view()),
    # path('create_messages/', views.CreateMessageViews.as_view()),
    # path('list_messages/<int:id>/', views.ListMessageViews.as_view()),
    # path('delete_session/<int:id>/', views.DeleteSessionViews.as_view()),
    # path('create_record/', views.CreateRecordView.as_view()),
    # path('get_record/<int:id>/', views.RecordImageView.as_view()),
   
#]
 