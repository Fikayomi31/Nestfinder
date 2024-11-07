from api import views as api_views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [

   

    # Authentication Endpoint
    
    path('user/token/', api_views.MyTokenObtainPairView.as_view()),
    path('user/token/refresh/', TokenRefreshView.as_view()),
    path('user/register/', api_views.RegisterView.as_view()),
    path('user/password-reset/<email>/', api_views.PasswordResetEmailVerifyAPIView.as_view()),
    path('user/password-change/', api_views.PasswordchangeAPIView.as_view()),
    
    # Core Endpoint
    path('core/category/', api_views.CategoryListAPIView.as_view()),
    path('core/property-list/', api_views.PropertyListAPIView.as_view()),

    #path('agent/', api_views.AgentListAPIView.as_view()),


]