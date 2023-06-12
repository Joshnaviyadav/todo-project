from django.shortcuts import HttpResponse 
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
import jwt
from django.conf import settings
from .models import ToDo
# Create your views here.
def index(request):
    return HttpResponse("index")

def todo(request):
    if request.response == "GET":
        data = ToDo.objects.all()
        title = []
        details = []
        date = []
        for item in data:
            ToDo.append(item['title'])
            ToDo.append(item['details'])
            ToDo.append(item['date'])
            
        response_data = {
            "title" : title,
            "details" : details,
            "date" : date,  
        }
        
        return JsonResponse(response_data)

        
    
    
class DataView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            token = request.META['HTTP_AUTHORIZATION'].split()[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            data = {"Userid":user_id}
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=401)