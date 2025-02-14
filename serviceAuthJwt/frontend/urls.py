from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('documents/', views.document_list, name='document_list'),
    path('document/add/', views.add_document, name='add_document'),
    path('document/edit/<int:doc_id>/', views.edit_document, name='edit_document'),
    path('document/delete/<int:doc_id>/', views.delete_document, name='delete_document'),
]
