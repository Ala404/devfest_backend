from datetime import date
from pathlib import Path
from django.http import JsonResponse
from rest_framework.views import Response, APIView
import pandas as pd
from users.models import Organization
from .models import Bill, BillType
from .serializers import BillSerializer, BillTypeSerializer
from .tools import  financial_date
import plotly.express as px
from fpdf import FPDF
import google.generativeai as genai
GOOGLE_API_KEY = 'AIzaSyCl1UpKx-JDl09jv20NrzpnR1yJBXE3nco'
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")
import google.generativeai as genai

# from users.authentication import JSONWebTokenAuthentication
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.parsers import MultiPartParser, FormParser
# from users.custom_renderers import ImageRenderer
# from django.http import HttpResponse
# from rest_framework import generics
# from .models import RecordMessage


# class SessionViews(APIView):
#     authentication_classes = [JSONWebTokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         request.data['patient'] = request.user.id
#         serializer = SessionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save() 
#             print(serializer.data)
#             return Response(serializer.data)
#         return Response({'error': "Can't add session", 'message': serializer.errors}, status=400)

#     def get(self, request):
#         print(request.user)
#         sessions = Session.objects.filter(patient=request.user)
#         serializer = SessionSerializer(sessions, many=True)
#         return Response(serializer.data)

# class DeleteSessionViews(APIView):
#     def delete(self, request, id):
#         instance = Session.objects.filter(id=id).first()
#         if not instance:
#             return Response({'error': 'there are no element with such id'})
#         if (instance.patient.id == request.user.id):
#             instance.delete()
#             return Response({'id': id})
#         else:
#             return Response({'error': 'non authorized'})


# class PatientSessionViews(APIView):
#     authentication_classes = [JSONWebTokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, id):
#         sessions = Session.objects.filter(patient=id)
#         serializer = SessionSerializer(sessions, many=True)
#         return Response(serializer.data)

# class CreateMessageViews(APIView):
#     authentication_classes = [JSONWebTokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         request.data['sender'] = request.user.id
#         serializer = MessageSerializer(data=request.data)
#         print(request.data)
#         if serializer.is_valid(): 
#             serializer.save()
#             if request.data.get('offline', False):
#                 answer = 'nigga'
#             else:
#                 try:
#                     response = client.chat.completions.create(
#                         messages=[
#                                     {
#                                         "role": "user",
#                                         "content": request.data['content']
#                                     }
#                                 ],
#                         model="gpt-3.5-turbo",
#                         temperature=0,
#                         max_tokens=1024,
#                         n=1,
#                         stop=None
#                     )
#                     answer = response.choices[0].message.content
#                 except Exception as e:
#                     answer = 'Sorry you Quota is limited'
#             serializer2 = MessageSerializer(data={'session': request.data['session'],'content': answer})
#             if serializer2.is_valid():
#                 serializer2.save()
#             return Response({'sender': 'bot', 'content': answer})
#         return Response({'sender': 'error', 'content': 'Error !!!'}, status=400)

# class ListMessageViews(APIView):
#     def get(self, request, id):
#         sessions = Message.objects.filter(session=id)
#         serializer = MessageSerializer(sessions, many=True)
#         temp = serializer.data.copy()
#         for message in temp:
#             print(message)
#             message['sender'] = 'patient' if message['sender'] else 'bot'
#         return Response(temp)


# class CreateRecordView(APIView):
#     permission_classes = [IsAuthenticated]
#     parser_classes = [FormParser, MultiPartParser]
    
#     def post(self, request):
#         data = dict(request.data)
#         data['session'] = data['session'][0]
#         data['image'] = data['image'][0]
#         data['sender'] = request.user.id
#         print(data)
#         serializer = RecordMessageSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data, status=200)
#         print(serializer.errors)
#         return Response(data=serializer.errors, status=500)

# class RecordImageView(generics.RetrieveAPIView):
#     renderers_classes = [ImageRenderer]
#     def get(self, request, id):
#         queryset = RecordMessage.objects.get(id=id).image
#         data = queryset
#         return HttpResponse(data, content_type='image/' + data.path.split(".")[-1])

class BillTypeAPIView(APIView):
    def get(self, request):
        organization = request.data.get('organization')
        if organization is None:
            return Response({'error': 'Specify organization!'}, status=400)
        bill_types = BillType.objects.filter(organization=organization)
        serializer = BillTypeSerializer(bill_types, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = BillTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class BillAPIView(APIView):
    def get(self, request):
        organization = request.data.get('organization')
        if organization is None:
            return Response({'error': 'Specify organization!'}, status=400)
        bills = Bill.objects.filter(type__organization=organization)
        serializer = BillSerializer(bills, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = BillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class FinancialDateAPIView(APIView):
    def get(self, request):
        return Response(financial_date(request.data['organization']), status=200)
    
class FinancialDataReportingAPIView(APIView):
    # permission_classes = [IsAuthenticated]  # Require authentication

    def post(self, request):
        metrics = request.data.get('metrics')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        organization = request.data.get('organization')
        title = request.data.get('title', 'Financial Data Over Time')
        output_dir = 'output'

        
        data = financial_date(organization)
        df = pd.DataFrame(data)
        if start_date:
            df = df[df['day'] >= pd.to_datetime(start_date).date()]
        if end_date:
            df = df[df['day'] <= pd.to_datetime(end_date).date()]
        
        if metrics:
            fig = px.line(df, x='day', y=metrics,
                            labels={'value': 'Amount', 'day': 'Date'},
                            title=title,
                            markers=True)

            fig.for_each_trace(lambda t: t.update(name=t.name.capitalize()))
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)  # Create directory if it doesn't exist
            fig.write_image(output_path / f'{title}_report.png', width=1200, height=600, scale=2)  # Save the plot
            
            pdf_report = GenerateReportPDF()
            pdf_response = pdf_report.get(request)  # Call the PDF generation method

            return Response({
                "message": "Plot created successfully!",
                # "pdf_message": pdf_response.content.decode('utf-8')
            }, status=200)
        return Response({
        "error": "No metrics provided!"
    }, status=400)


class GenerateReportPDF(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        output_dir = Path("output")  # Define your output directory here
        try:
            self.generate_pdf_report(output_dir)
            return JsonResponse({"message": "PDF report generated successfully!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
    def generate_pdf_report(self, output_dir):
        # Convert output_dir to Path object if it's not already
        output_dir = Path(output_dir)

        # Define the font color as RGB values (dark gray)
        font_color = (64, 64, 64)

        # Find all PNG files in the output folder
        chart_filenames = list(output_dir.glob("*.png"))

        # Create a PDF document and set the page size
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 24)

        # Add the overall page title
        title = f"Financial Report of {date.today().strftime('%d/%m/%Y')}"
        pdf.set_text_color(*font_color)
        pdf.cell(0, 20, title, align='C', ln=1)
        pdf.ln(10)  # Add a space after the title

        # Add each chart to the PDF document
        pdf.set_font('Arial', '', 12)  # Set font for chart interpretation text
        for chart_filename in chart_filenames:
            pdf.ln(10)  # Add padding at the top of the next chart
            pdf.image(str(chart_filename), x=10, y=None, w=pdf.w - 20)  # Adjust margins
            
            myfile = genai.upload_file(chart_filename)
            result = model.generate_content([myfile, "\n\n", "Can you interpret this graph?"])
            # Add interpretation text for each chart
            try:
                # Adjusted access path to find the text field directly
                interpretation_text = result.candidates[0].content.parts[0].text
                print("Interpretation Text:", interpretation_text)
            except AttributeError as e:
                print("Error accessing 'text' field:", e)
            # interpretation_text = str(result.result.candidates[0].content.parts[0].text)
            # print(interpretation_text)
            pdf.ln(5)  # Add some space between the chart and the text
            pdf.multi_cell(0, 10, interpretation_text)  # Text wrapping

        # Save the PDF document to a file on disk
        pdf_output_path = output_dir / "report.pdf"
        pdf.output(str(pdf_output_path), "F")
        print(f"PDF report saved successfully at {pdf_output_path}")




