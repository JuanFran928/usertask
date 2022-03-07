from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework import generics, status
import jwt, datetime
from .models import CustomUser


class LoginView(APIView):
    def post(self, request):
        print("entra")
        # Recuperamos las credenciales y autenticamos al usuario
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        print(email)
        print(password)
        user = authenticate(email=email, password=password)

        # Si es correcto añadimos a la request la información de sesión
        if user:
            #print(datetime.datetime.utcnow())
            login(request, user)
            """ JSON WEB TOKEN"""
            payload = {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 60),
                'iat': datetime.datetime.now(datetime.timezone.utc)
            }
            
            #token = jwt.encode(payload, 'secret', algorithm= 'HS256').decode('utf-8')
            token = jwt.encode(payload, 'secret', algorithm= 'HS256')
            '''
            oldresponse = Response(
                UserSerializer(user).data,
                status=status.HTTP_200_OK) #response antigua para devolver, funcionaba'''
            
            
            newresponse = Response()
            
            newresponse.set_cookie(key='jwt', value=token, httponly = True)
            newresponse.data = {
                'jwt': token
            }
            
            
            return newresponse

        # Si no es correcto devolvemos un error en la petición
        return Response(
            status=status.HTTP_404_NOT_FOUND)
        
#nuevo tutorial
class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms= ['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        user = CustomUser.objects.filter(id = payload['id']).first()
        
        response = Response(
                UserSerializer(user).data,
                status=status.HTTP_200_OK)
        
        return response

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        '''
        return Response(status=status.HTTP_200_OK)'''
        
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        response.status = status.HTTP_200_OK  
        return response      
        
        '''
        La de antes
        # Borramos de la request la información de sesión
        logout(request)

        # Devolvemos la respuesta al cliente
        return Response(status=status.HTTP_200_OK)
        '''
        


class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer