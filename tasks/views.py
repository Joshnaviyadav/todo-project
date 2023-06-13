from django.shortcuts import HttpResponse 
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
import jwt
from django.conf import settings
from .models import ToDo
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
def index(request):
    return HttpResponse("index")

def update_task(request):
    pass


def delete_tasks(request):
    selected_tasks = request.data.get('tasks', [])
    
    # Delete the selected tasks from the database
    ToDo.objects.filter(task__in=selected_tasks).delete()
    
    return "deleted"
    
    
    
def create_task(request,userName,task,description,status):
    data = ToDo.objects.all()
    boolean = True
    for item in data:
        if item.task == task:
            boolean = False
    if boolean:
        ToDo.objects.create(
            user_name=userName,
            task=task,
            description=description,
            status=status
            )
        print("obj created successfully")

    
def read_task(request,userName):
    data = ToDo.objects.all()
    task = []
    description = []
    status = []
    for item in data:
        if item.user_name == userName:
            task.append(item.task)
        
    response_data = {
        "task" : task,
    }
        
    return response_data


        

class Todo(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self,request,*args,**kwargs):
        try:
            response ={"WOW":"wow - 1"}
            Type = self.request.GET.get('type')
            userName = self.request.GET.get('userName')
            task = self.request.GET.get('task')
            status = self.request.GET.get('status')
            discription = self.request.GET.get('discription')
             
            if Type == "update":
                response = update_task(request)
            elif Type == "delete":
                response = delete_tasks(request)
            elif Type == "create":
                response = create_task(request,userName,task,discription,status)
            elif Type == "read":
                response = read_task(request,userName)
            return JsonResponse(response)
            
        except Exception as e:
            return Response({'error': str(e)})

    def post(self,request,*args,**kwargs):
        try:
            response ={"WOW":"wow - 1"}
            Type = self.request.GET.get('type')
            userName = self.request.GET.get('userName')
            task = self.request.GET.get('task')
            status = self.request.GET.get('status')
            discription = self.request.GET.get('discription')
            
            if Type == "update":
                response = update_task(request)
            elif Type == "delete":
                response = delete_tasks(request)
            elif Type == "create":
                response = create_task(request,userName,task,discription,status)
            elif Type == "read":
                response = read_task(request,userName)
            return JsonResponse(response)
                
        except Exception as e:
            return Response({'error': str(e)})
            
    
    
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