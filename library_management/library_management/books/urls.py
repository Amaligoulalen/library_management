from django.urls import path
from .views import Home, BookCreate, AllBooksView
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.Home.as_view(), name='home'), 
    path('add-book/', views.BookCreate.as_view(), name='add_book'),
    path('livres/', views.AllBooksView.as_view(), name='all_books'),
    path('livres/<int:idlivre>/',views.LivreDetail.as_view(),name='livredetail'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('livres/modifier/<int:id>',views.BookUpdate.as_view(),name='update_book'),
    path('livres/supprimer/<int:id>',views.BookDelete.as_view(),name='delete_book'),
    path('livres/emprunter/<int:book_id>/', views.BorrowBookView.as_view(), name='borrow_book'),
    path('gestion/emprunts/', views.admin_borrow_list, name='admin_borrow_list'),
    path('my-borrows/', views.UserBorrowListView.as_view(), name='user_borrows'),
    path('return/<int:borrow_id>/', views.ReturnBookView.as_view(), name='return_book'),
]
