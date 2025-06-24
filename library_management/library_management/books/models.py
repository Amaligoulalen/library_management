from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Book(models.Model):
    title = models.CharField( max_length=200)
    author = models.CharField( max_length=200)
    description = models.TextField( blank=True)
    published_date = models.DateField( null=True, blank=True)
    
    cover_image = models.ImageField( blank=True, null=True)
    isbn = models.CharField( max_length=13, unique=True, blank=True, null=True)
    publisher = models.CharField( max_length=200, blank=True)
    pages = models.PositiveIntegerField( blank=True, null=True)
    language = models.CharField( max_length=100, default="Français")
    genre = models.CharField( max_length=100, blank=True)
    available = models.BooleanField( default=True)
    copies = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField( auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.author}"

class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=timezone.now() + timedelta(days=15))

    def is_overdue(self):
        return timezone.now() > self.due_date

    def __str__(self):
        return f"{self.user.username} a emprunté {self.book.title}"

    