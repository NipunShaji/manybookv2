from django.urls import path

from .views import (
    registration_view,
    logout_view,
    login_view,
    update_view,
)

app_name = 'account'

urlpatterns = [
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('update/', update_view, name='update'),
]
