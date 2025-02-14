from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from django.contrib.auth import authenticate, login, logout
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .models import CustomUser
from drf_spectacular.utils import extend_schema
from django.middleware.csrf import get_token
from oauth2_provider.models import AccessToken
from datetime import timedelta
from django.utils import timezone
from django.middleware.csrf import get_token


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

@extend_schema(
    request=RegisterSerializer,
    responses={201: 'User created successfully', 400: 'Invalid data'},
)
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=LoginSerializer,
    responses={200: 'Login successful', 400: 'Invalid credentials'},
)
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        csrf_token = get_token(request)
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                
                # Buscar o crear el token de acceso
                token, created = AccessToken.objects.get_or_create(user=user)
                
                # Si el token es nuevo, asignar el valor de expiración
                if created:
                    token.expires = timezone.now() + timedelta(seconds=3600)  # Expiración en 1 hora
                    token.save()
                else:
                    # Si el token ya existe, actualiza la expiración
                    token.expires = timezone.now() + timedelta(seconds=3600)
                    token.save()

                response_data = {
                    'message': 'Login successful',
                    'access_token': token.token,
                    'csrfToken': csrf_token,
                }
                return Response(response_data, status=status.HTTP_200_OK)

            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@extend_schema(
    request=LoginSerializer,
    responses={200: 'Logout successful', 400: 'Invalid credentials'},
)
def logout_view(request):
    # Código de logout
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        # Autenticación del usuario
        user = authenticate(username=email, password=password)
        if user is not None:
            # Desconectar al usuario
            logout(request)
            
            # Invalida el token de acceso
            try:
                # Eliminar el token del usuario (revocar acceso)
                access_token = AccessToken.objects.get(user=user)
                access_token.delete()  # Elimina el token de acceso
            except AccessToken.DoesNotExist:
                pass  # Si no existe un token, no hacemos nada
            
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
