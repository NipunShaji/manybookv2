from django.contrib import admin

from .models import Book,BookShelf,Downloads, Genre, Language, Rating, Reply, Comment, Barcode

admin.site.register(Book)
admin.site.register(BookShelf)
admin.site.register(Downloads)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Rating)
admin.site.register(Reply)
admin.site.register(Comment)
admin.site.register(Barcode)