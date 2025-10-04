from django.urls import path
from .views import RegisterView, LoginView, LogoutView, UserListView, UserDetailView, ProfileView, api_root

urlpatterns = [
    path('', api_root, name='api-root'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
