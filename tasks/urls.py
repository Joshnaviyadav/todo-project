from django.urls import path
from .views import index,Todo, DataView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("",index),
    path("todo/",Todo.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('data/', DataView.as_view(), name='data'),
    # path('',)
]