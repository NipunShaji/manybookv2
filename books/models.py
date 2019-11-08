from django.db import models
from account.models import Account
from multiselectfield import MultiSelectField
from django.utils import timezone

class Genre(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return self.name

class Language(models.Model):
    lang        = models.CharField(max_length=30,primary_key=True)

    def __str__(self):
        return self.lang

class Book(models.Model):

    title           = models.CharField(max_length=120, null=False, blank=False)
    author          = models.CharField(max_length=40, null=False, blank=False)
    series          = models.CharField(max_length=20)
    genre           = models.ManyToManyField(Genre)
    language        = models.ForeignKey(Language, on_delete=models.CASCADE)
    description     = models.CharField(max_length=1536, null=False, blank=False)
    isbn            = models.CharField(max_length=13, unique=True, null=False)
    file            = models.FileField(upload_to='pdf/')
    cover           = models.ImageField(upload_to='covers/', null=True, blank=True)
    views           = models.IntegerField(default=0)
    user            = models.ForeignKey(Account, on_delete=models.CASCADE)
    totalrating     = models.PositiveSmallIntegerField(default=0)
    ratingcount     = models.PositiveIntegerField(default=0)
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class BookShelf(models.Model):
    user                = models.ForeignKey(Account, on_delete=models.CASCADE)
    book                = models.ForeignKey(Book, on_delete=models.CASCADE)
    iscurrentbook       = models.BooleanField(default=False)
    currentpage         = models.PositiveIntegerField(default=1)
    totalpage           = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username

class Downloads(models.Model):
    user                = models.ForeignKey(Account, on_delete=models.CASCADE)
    book                = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at          = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.book.title

class Comment(models.Model):
    book        = models.ForeignKey(Book, on_delete=models.CASCADE)
    user        = models.ForeignKey(Account, on_delete=models.CASCADE)
    text        = models.CharField(max_length=512, null=False)
    likes       = models.PositiveIntegerField(default=0)
    dislikes    = models.PositiveIntegerField(default=0)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class Reply(models.Model):
    class Meta:
        ordering = ['-created_at']
        
    comment     = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user        = models.ForeignKey(Account, on_delete=models.CASCADE)
    text        = models.CharField(max_length=512, null=False)
    likes       = models.PositiveIntegerField(default=0)
    dislikes    = models.PositiveIntegerField(default=0)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

class Rating(models.Model):
    book        = models.ForeignKey(Book, on_delete=models.CASCADE)
    user        = models.ForeignKey(Account, on_delete=models.CASCADE)
    userrating  = models.PositiveSmallIntegerField(default=0, null=False)

    def __str__(self):
        return str(self.userrating)


class Barcode(models.Model):

    long_url     = models.URLField(primary_key=True)
    short_url    = models.URLField(default="")
    image        = models.FileField(upload_to='images/barcodes/')

    def __str__(self):
        return str(self.long_url)