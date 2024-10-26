import pandas as pd
from django_pandas.io import read_frame
from django.apps import apps  # Import to access Django models
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from statsmodels.tsa.statespace.sarimax import SARIMAX

import google.generativeai as genai
GOOGLE_API_KEY = 'AIzaSyCl1UpKx-JDl09jv20NrzpnR1yJBXE3nco'
genai.configure(api_key=GOOGLE_API_KEY)

model_generation = genai.GenerativeModel("gemini-1.5-flash")
import google.generativeai as genai


def load_cashflow_data(model_name, feature):
    # Dynamically get the model class using the model name
    try:
        CashFlowModel = apps.get_model('finance', model_name)  # Ensure the correct app name is provided
    except LookupError:
        raise ValueError(f"Model '{model_name}' not found.")

    # Load CashFlow data from the specified model
    queryset = CashFlowModel.objects.all()
    df = read_frame(queryset)
    
    # Convert 'date' column to datetime and set it as index
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df.set_index("date", inplace=True)
    df.sort_index(inplace=True)

    # Check if the feature exists
    if feature not in df.columns:
        raise ValueError(f"The feature '{feature}' is not available in {model_name} data.")
    
    # Select the specified feature and ensure it's a numeric series
    series = pd.to_numeric(df[feature], errors='coerce').dropna()
    
    return series



class SarimaForecastView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        # Retrieve the model name and feature from the request parameters
        model_name = request.query_params.get("model", "CashFlow")  # Default model name
        feature = request.query_params.get("feature")  # Feature must be provided
        
        if not feature:
            return Response({"error": "Feature parameter is required."}, status=400)

        # Load the cash flow time series data using the specified model and feature
        try:
            series = load_cashflow_data(model_name=model_name, feature=feature)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        # Train the SARIMA model
        order = (1, 1, 1)  # You can make these configurable if needed
        seasonal_order = (1, 1, 1, 12)
        model = SARIMAX(series, order=order, seasonal_order=seasonal_order)
        sarima_model = model.fit(disp=False)

        # Forecast future values
        steps = 12  # You can also make this configurable if needed
        forecast = sarima_model.forecast(steps=steps)
        
        # Return the forecast as a JSON response
        return Response(forecast.to_dict())
    



# class GeminiForecastIntrpretationView(RetrieveAPIView):
#     def get(self, request, *args, **kwargs):
#         # Retrieve the model name and feature from the request parameters
#         model_name = request.query_params.get("model")  # Default model name
#         feature = request.query_params.get("feature")  # Feature must be provided
        
#         if not feature:
#             return Response({"error": "Feature parameter is required."}, status=400)

#         # Load the cash flow time series data using the specified model and feature
#         try:
#             series = load_cashflow_data(model_name=model_name, feature=feature)
#         except ValueError as e:
#             return Response({"error": str(e)}, status=400)

#         # Train the SARIMA model
#         order = (1, 1, 1)  # You can make these configurable if needed
#         seasonal_order = (1, 1, 1, 12)
#         model = SARIMAX(series, order=order, seasonal_order=seasonal_order)
#         sarima_model = model.fit(disp=False)

#         # Forecast future values
#         steps = 12  # You can also make this configurable if needed
#         forecast = sarima_model.forecast(steps=steps)
#         result_inter = model_generation.generate_content([str(forecast.to_dict()), "\n\n", "Can you interpret this forcasting values?"])


        
#         # Return the forecast as a JSON response
#         return Response(str(result_inter))




class GeminiForecastInterpretationView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        # Retrieve the model name and feature from the request parameters
        model_name = request.query_params.get("model")  # Model name must be provided
        feature = request.query_params.get("feature")    # Feature must be provided

        if not model_name:
            return Response({"error": "Model parameter is required."}, status=400)
        if not feature:
            return Response({"error": "Feature parameter is required."}, status=400)

        # Dynamically get the model class and initialize a list with its column names
        try:
            ModelClass = apps.get_model('finance', model_name)  # Replace 'finance' with your actual app name
        except LookupError:
            return Response({"error": f"Model '{model_name}' not found."}, status=400)

        # Extract column names of the specified model
        model_columns = [field.name for field in ModelClass._meta.get_fields()]
        feature_data = list(ModelClass.objects.values_list(feature, flat=True))


        # Load the cash flow time series data using the specified model and feature
        try:
            series = load_cashflow_data(model_name=model_name, feature=feature)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        # Train the SARIMA model
        order = (1, 1, 1)  # Configurable if needed
        seasonal_order = (1, 1, 1, 12)
        model = SARIMAX(series, order=order, seasonal_order=seasonal_order)
        sarima_model = model.fit(disp=False)

        # Forecast future values
        steps = 12  # Configurable if needed
        forecast = sarima_model.forecast(steps=steps)

        # Generate interpretation for the forecasted values
        result_inter = model_generation.generate_content([
            f"Model Columns: {str(model_columns)}",
            f"Historical Data: {str(feature_data)}",
            f"Forecast Interpretation: {str(forecast.to_dict())}",
            "\n\n",
            f"Provide a medium comprehensive analysis of both the historical data and the forecasted values for the specified table and feature. Focus on identifying key patterns, trends, and potential implications of the forecast to guide strategic decision-making. Highlight any insights that could support planning and performance evaluation based on this data and don't talk about the period of time, make short and summrize."
        ])

        result_interr= result_inter.candidates[0].content.parts[0].text

        # Return the model columns and the forecast interpretation as a JSON response
        return Response({
            # "model_columns": model_columns,
            # "feature_data": feature_data,
            # "Historical Data": feature_data,
            "forecast_interpretation": result_interr
        })
