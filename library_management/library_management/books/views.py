from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.views import View
from .models import Book, Borrow
from .forms import BookForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import ListView
from datetime import timedelta
from django.utils import timezone

class AllBooksView(View):
    def get(self, request):
        books = Book.objects.all()
        is_admin = request.user.is_superuser
        return render(request, 'all_books.html', {'books': books})

class Home(View):
    def get(self, request):
        books = Book.objects.all()
        return render(request, 'home.html', {'books': books})


class LivreDetail(View):
    def get(self, request, idlivre):
        livre = Book.objects.get(id=idlivre)  
        return render(request, 'detail_livre.html', {'livre': livre})
    
class BookCreate(View):
    def get(self,request):
        form=BookForm()
        return render(request,'add_book.html',{'form':form})
    
    def post(self,request):
        form=BookForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('all_books')
        return render(request,'add_book.html',{'form':form})
    
@login_required
def profil_utilisateur(request):
    livre = Book.objects.filter(auteur=request.user).order_by('-title')
    return render(request, 'home.html', {'livre': livre})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connexion automatique après inscription
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

class BookUpdate(View):
    def get(self,request,id):
        livre=Book.objects.get(id=id)
        form=BookForm(instance=livre)
        return render(request, 'add_book.html', {'form':form})
    
    def post(self, request,id):
        livre=Book.objects.get(id=id)
        form=BookForm(request.POST,request.FILES,instance=livre)
        if form.is_valid():
            form.save()
            return redirect('all_books')
        return render(request, 'add_book.html', {'form':form})
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("Vous n'avez pas la permission.")
        return super().dispatch(request, *args, **kwargs)
    
class BookDelete(View):
    def get(self,request,id):
        livre=Book.objects.get(id=id)
        livre.delete()
        return redirect('all_books')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("Vous n'avez pas la permission.")
        return super().dispatch(request, *args, **kwargs)
        
        
class BorrowBookView(LoginRequiredMixin, View):
    def get(self, request, book_id):
        book = Book.objects.get(id=book_id)
        user = request.user

        # Vérif : limite de 6 livres
        if Borrow.objects.filter(user=user).count() >= 6:
            return HttpResponse("Limite de 6 livres atteinte.")

        # Vérif : copies disponibles
        if book.copies <= 0:
            return HttpResponse("Aucun exemplaire disponible.")

        # Emprunt
        Borrow.objects.create(user=user, book=book)
        book.copies -= 1
        book.save()

        return redirect('all_books')
    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        user = request.user

        # Vérifier limite de 6 livres
        if Borrow.objects.filter(user=user).count() >= 6:
            return HttpResponse("Limite de 6 livres atteinte.")

        # Vérifier disponibilité
        if book.copies <= 0:
            return HttpResponse("Aucun exemplaire disponible.")

        # Créer l'emprunt
        Borrow.objects.create(
            user=user,
            book=book,
            due_date=timezone.now() + timedelta(days=15)
        )
        book.copies -= 1
        book.save()

        return redirect('all_books')
    
    
class ReturnBookView(LoginRequiredMixin, View):
    def post(self, request, borrow_id):
        borrow = get_object_or_404(Borrow, id=borrow_id, user=request.user)
        borrow.book.copies += 1
        borrow.book.save()
        borrow.delete()
        return redirect('user_borrows')  # ou autre nom d'URL
    
    
@staff_member_required
def admin_borrow_list(request):
        borrows = Borrow.objects.all().order_by('-borrowed_at')
        return render(request, 'admin_borrow_list.html', {'borrows': borrows})
   
   
class UserBorrowListView(LoginRequiredMixin, ListView):
    model = Borrow
    template_name = 'my_borrows.html'
    context_object_name = 'borrows'

    def get_queryset(self):
        return Borrow.objects.filter(user=self.request.user).order_by('-borrowed_at')     