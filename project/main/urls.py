from django.urls import path, re_path
from django.contrib.auth import views as authViews
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('get-balance/', get_balance),
    path('personal-admin/', personal_admin),
    path('personal-admin/case/<int:pk>/', CaseUpdate.as_view()),
    path('personal-admin/case/create/', case_create),
    path('personal-admin/weapons/', personal_admin_weapons),
    path('personal-admin/weapons/<int:pk>/', WeaponsUpdate.as_view()),
    path('personal-admin/weapons/create/', weapon_create),
    path('personal-admin/categories/', personal_admin_categories),
    path('personal-admin/categories/<int:pk>/', CategoriesUpdate.as_view()),
    path('personal-admin/categories/create/', categories_create),
    re_path(r'^auth/$', auth),
    path('exit/', authViews.LogoutView.as_view(next_page='/'), name='exit')
]