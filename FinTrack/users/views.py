from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework import parsers, renderers, status
from .serializers import AuthTokenSerializer, OrganizationSerializer
from .serializers import UserCreationSerializer, UserSerializer
import jwt, datetime
from .models import Organization, User
 


class JSONWebTokenAuth(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = jwt.encode({
                'email': serializer.validated_data['email'],
                'iat': datetime.datetime.utcnow(),
                'nbf': datetime.datetime.utcnow() + datetime.timedelta(minutes=-5),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=5)
            }, settings.SECRET_KEY, algorithm='HS256')
            return Response({'token': token})
        user = User.objects.filter(email=request.data['email']).first()
        if user:
            if not user.is_active:
                return Response({'token': 'verification'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
class SignupView(APIView): 
    def post(self, request):
        serializer = UserCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'new users has been registered', 'email': serializer.data['email']})
        return Response(serializer.errors)

class ProfileView(APIView):
    def get(self, request):
        profile = User.objects.filter(id=request.user.id).first()
        serializer = UserSerializer(profile)
        print(serializer.data)
        return Response(serializer.data)
    
class OrganizationAPIView(APIView):

    def get(self, request):
        organizations = Organization.objects.filter(owner=request.user.id)
        serializer = OrganizationSerializer(organizations, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        request.data['owner'] = request.user.id
        serializer = OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
