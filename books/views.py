import json

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db.models import Q
from django.utils.text import wrap
from django.db.models.functions import Lower

from account.models import Account

from .forms import AddBook
from .models import Book, BookShelf, Downloads, Genre, Language, Rating, Reply, Comment, Barcode

import requests,barcode
from django.core.files import File

# def trial(request):
#     return render(request, 'books/trial2.html')

@login_required
def pdfviewer(request):
    context = {}
    if request.method == 'GET':
        if request.GET['isbn'] :
            context['isbn'] = request.GET['isbn']
            context['book'] = Book.objects.get(isbn = request.GET['isbn'])
            try:
                context['page'] = BookShelf.objects.get(user=request.user, book=context['book']).currentpage
            except BookShelf.DoesNotExist:
                context['page'] = 1
    return render(request, 'books/pdfviewer.html',context)


def home(request):
    context = {}
    context['search'] = True
    if request.user.is_authenticated:
        context['auth'] = True
    allBooks = Book.objects.select_related('user').all()
    context['mostviewed'] = allBooks.order_by('-views')[:12]
    context['new'] = allBooks.order_by('-created_at')[:12]
    return render(request, 'books/index.html', context)

@login_required
def addbook(request):
    context = {}
    context['addbookActive'] = True
    context['auth'] = True
    form = AddBook(initial = {'user':request.user})
    if request.method == 'POST':
        form = AddBook(request.POST, request.FILES, initial = {'user':request.user})
        if form.is_valid():
            book = form.save()
            response = HttpResponse(status=302)
            response['Location'] = '/book?isbn='+str(book.isbn)
            return response
            form = AddBook(initial = {'user':request.user})
    context['form'] = form;
    context['genres'] = Genre.objects.all()
    context['languages'] = Language.objects.all()
    return render(request, 'books/addbook2.html', context)


def bookview(request,isbn=None):
    context = {}
    context['search'] = True
    if request.user.is_authenticated:
        context['auth'] = True
    if request.method=='GET':
        if request.GET.get('isbn'):
            isbn = request.GET.get('isbn')
    if isbn == None:
        return redirect('books:home')
    book = Book.objects.get(isbn=isbn)
    context['book'] = book
    bookrating = Rating.objects.filter(book=book).count()
    if bookrating == 0:
        context['ratingnumber'] = 0
    else:
        context['ratingnumber'] = bookrating
    if request.user.is_authenticated:
        if Rating.objects.filter(book=book, user=request.user).count() == 0:
            context['userRated'] = False
        else:
            context['userRated'] = True
            context['userrating'] = Rating.objects.get(book=book,user=request.user).userrating
    else:
        context['userRated'] = False
    context['comments'] = Comment.objects.filter(book=book).order_by('-created_at')
    context['morefromauthor'] = Book.objects.filter(author=book.author).exclude(isbn=book.isbn)[:6]

    #get or generate barcode
    barcode = gen_or_get_barcode(request)
    context['barcode'] = barcode

    return render(request, 'books/bookview.html', context)



def catview(request):
    context = {}
    context['search'] = True
    context['languages'] = Language.objects.all()
    context['genres'] = Genre.objects.all()
    if request.user.is_authenticated:
        context['auth'] = True
    if request.method == 'POST':
        sort = request.POST.get('sort','az')
        lang = request.POST.get('language','all')
        gen = request.POST.get('category','all')
        print('lang print next')
        print(request.POST.get('category'))
        books = Book.objects.select_related('language').all()
        if lang != 'all':
            language = Language.objects.get(lang=lang)
            books = books.filter(language = language)
        if gen != 'all':
            genre = Genre.objects.get(name=gen)
            books = books.filter(genre=genre)
        if sort == 'az':
            books = books.order_by(Lower('title'))
        elif sort == 'za':
            books = books.order_by(Lower('title')).reverse()
        elif sort == 'no':
            books = books.order_by('-created_at')
        else:
            books = books.order_by('created_at')
        context['cat'] = books
        context['selectedsort'] = sort
        context['selectedlang'] = lang
        context['selectedgen'] = gen
        return render(request, 'books/catview1.html', context)
    if request.method == 'GET':
        cat = request.GET.get('cat')
        context['title'] = cat
        context['cat'] = Book.objects.filter(genre = Genre.objects.get(name = cat))
    return render(request, 'books/catview1.html', context)

@login_required
def search(request):
    context ={}
    context['search'] = True
    if request.user.is_authenticated:
        context['auth'] = True
    context['title'] = 'Search Results'
    if request.method == 'GET':
        q = request.GET.get('search')
        context['cat'] = Book.objects.filter(Q(title__icontains=q) | Q(author__icontains=q) | Q(description__icontains=q))
    return render(request, 'books/searchview.html', context)

@login_required
def addtoshelf(request):
    context = {'status':'err'}
    if request.method == "GET":
        isbn = request.GET.get('isbn')
        book = Book.objects.get(isbn=isbn)
        user = request.user
        try:
            bookadded = BookShelf.objects.filter(book=book).filter(user= Account.objects.get(username=request.user))
            context['status'] = 'pre'
        except BookShelf.DoesNotExist:
            text = Book.objects.get(isbn = isbn)
            text.views+=1
            text.save()
            newbook=BookShelf(user=Account.objects.get(username=request.user), book=text)
            newbook.save()
            context['status'] = 'ok'
        if not bookadded:
            text = Book.objects.get(isbn = isbn)
            text.views+=1
            text.save()
            newbook=BookShelf(user=Account.objects.get(username=request.user), book=text)
            newbook.save()
            context['status'] = 'ok'
    return JsonResponse(context)

def bookshelf(request):
    context = {}
    context['auth'] = False
    context['bookshelfActive'] = True
    context['search'] = True
    if request.user.is_authenticated:
        context['auth'] = True
        context['books'] = BookShelf.objects.filter(user=request.user)
        try:
            context['currentbook'] = context['books'].get(iscurrentbook=True)
            if context['currentbook'].totalpage == 0:
                context['percent'] = 0;
            else:
                context['percent'] = context['currentbook'].currentpage / context['currentbook'].totalpage * 100
        except BookShelf.DoesNotExist:
            pass
    return render(request, 'books/bookshelf1.html', context)

@login_required
def deletebook(request):
    context = {'status':'err'}
    if request.method == 'GET':
        isbn = request.GET.get('isbn')
        try:
            book = Book.objects.get(isbn=isbn)
        except Book.DoesNotExist:
            return JsonResponse(context)
        bookinshelf = BookShelf.objects.filter(book=book).filter(user=request.user)
        bookinshelf.delete()
        context['status'] = 'ok'
    return JsonResponse(context)

@login_required
def setcurrentbook(request):
    if request.method == 'GET':
        try:
            previousbook = BookShelf.objects.get(user=request.user, iscurrentbook=True)
            previousbook.iscurrentbook = False
            previousbook.save()
        except BookShelf.DoesNotExist:
            pass
        isbn = request.GET.get('isbn')
        try:
            book = Book.objects.get(isbn=isbn)
        except Book.DoesNotExist:
            print('Error in getting book')
            return
        item = BookShelf.objects.get(book=book, user=request.user)
        item.iscurrentbook = True
        item.save()
    return

@login_required
def setcurrentpage(request):
    print('got request')
    if request.method == 'GET':
        currentbook = BookShelf.objects.get(user=request.user, iscurrentbook=True)
        pageno = request.GET.get('page')
        totalpage = request.GET.get('total')
        print('in if ')
        if int(pageno) > currentbook.currentpage:
            currentbook.currentpage = pageno
            currentbook.totalpage = int(totalpage)
            currentbook.save()
            print('saved')
    return JsonResponse({'result':'done'})

@login_required
def uploadslist(request):
    context = {}
    context['uploadActive'] = True
    context['search'] = True
    if request.user.is_authenticated:
        context['auth'] = True
    if request.method == 'GET':
        booklist = Book.objects.filter(user=request.user)
        page = request.GET.get('page',1)
        paginator = Paginator(booklist.order_by('-created_at'),10)
        context['books'] = paginator.get_page(page)
        context['length'] = booklist.count()
        context['cat'] = 'Uploads'
        context['upload'] = True
    return render(request, 'books/uploads.html', context)

@login_required
def downloadlist(request):
    context = {}
    context['downloadActive'] = True
    context['search'] = True
    if request.user.is_authenticated:
        context['auth'] = True
    if request.method == 'GET':
        booklist = Downloads.objects.filter(user = request.user)
        page = request.GET.get('page',1)
        paginator = Paginator(booklist.order_by('-created_at'),10)
        context['booksdown'] = paginator.get_page(page)
        context['cat'] = 'Downloads'
        context['download'] = True
    return render(request, 'books/uploads.html', context)

@login_required
def downloaded(request):
    if request.method == 'GET':
        if request.GET.get('isbn'):
            book = Book.objects.get(isbn = request.GET.get('isbn'))
            user = request.user
            try:
                downloadedBook = Downloads.objects.get(user=request.user, book=book)
            except Downloads.DoesNotExist:
                item = Downloads(user = user, book = book);
                item.save()
                return
            downloadedBook.created_at = timezone.now()
            downloadedBook.save()
            return
    return

@login_required
def checkisbn(request):
    if request.method == 'GET':
        isbn = request.GET.get('isbn')
        try:
            book = Book.objects.get(isbn=isbn)
            return JsonResponse({'status':'err'})
        except Book.DoesNotExist:
            return JsonResponse({'status':'ok'})
        return JsonResponse({'status':'ok'})


@login_required
def setrating(request):
    if request.method == 'GET':
        rate = request.GET.get('rating',0)
        if rate == 0:
            return HttpResponse('Error!!!!  Not A valid rating.')
        isbn = request.GET.get('isbn',0)
        if isbn == 0:
            return HttpResponse('Error!!!!  Not A valid isbn.')
        try:
            book = Book.objects.get(isbn=isbn)
        except Book.DoesNotExist:
            return HttpResponse('Error!!!!  No such book.')
        if Rating.objects.filter(user=request.user, book=book).exists():
            response = HttpResponse(status=302)
            response['Location'] = '/book?isbn='+str(book.isbn)
            return response
        if book.ratingcount == 0:
            book.totalrating = rate;
            book.ratingcount += 1;
            book.save()
        else:
            book.ratingcount += 1
            book.totalrating = (book.totalrating + int(rate))/book.ratingcount
            book.save()
        newRating = Rating(user=request.user, book=book, userrating=rate).save()
        response = HttpResponse(status=302)
        response['Location'] = '/book?isbn='+str(book.isbn)
        return response
    return HttpResponse('error Occured')

@login_required
def newcomment(request):
    if request.method == 'GET':
        text = request.GET.get('text','')
        if text == '':
            return HttpResponse('No text for comment')
        print(text)
        isbn = request.GET.get('isbn',0)
        if isbn == 0:
            return HttpResponse('No id for book passed')
        try:
            book = Book.objects.get(isbn=isbn)
        except Book.DoesNotExist:
            return HttpResponse('No such book')
        new = Comment(text=text, user=request.user, book=book).save()
        response = HttpResponse(status=302)
        response['Location'] = '/book?isbn='+str(book.isbn)
        return response
    return HttpResponse('error Occured')

@login_required
def newreply(request):
    if request.method == 'GET':
        text = request.GET.get('text','')
        if text == '':
            return HttpResponse('No text for reply')
        print(text)
        id = request.GET.get('id',0)
        if id == 0:
            return HttpResponse('No id for comment passed')
        try:
            comment= Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            return HttpResponse('No such comment')
        new = Reply(text=text, user=request.user, comment=comment).save()
        response = HttpResponse(status=302)
        response['Location'] = '/book?isbn='+str(comment.book.isbn)
        return response
    return HttpResponse('error Occured')

def deletecomment(request):
    if request.method == 'GET':
        commentid = request.GET.get('commentid',0)
        if commentid == 0:
            return HttpResponse('No such comment id')
        try:
            comment= Comment.objects.get(id=commentid)
        except Comment.DoesNotExist:
            return HttpResponse('No such comment')
        comment.delete()
        response = HttpResponse(status=302)
        response['Location'] = '/book?isbn='+str(comment.book.isbn)
        return response
    return HttpResponse('error Occured')

def deletereply(request):
    if request.method == 'GET':
        replyid = request.GET.get('replyid',0)
        if replyid == 0:
            return HttpResponse('No such reply id')
        try:
            reply= Reply.objects.get(id=replyid)
        except Reply.DoesNotExist:
            return HttpResponse('No such reply')
        isbn = reply.comment.book.isbn
        reply.delete()
        response = HttpResponse(status=302)
        response['Location'] = '/book?isbn='+str(isbn)
        return response
    return HttpResponse('error Occured')



def gen_or_get_barcode(request):

    requesting_url = request.build_absolute_uri()
    code128 = barcode.get_barcode_class('code128')

    try:
        barcode_obj = Barcode.objects.get(long_url=requesting_url)
        if(not barcode_obj.short_url ):
            short_barcode_request = json.loads(shorten_url(requesting_url))
            if(short_barcode_request['status'] == 'ok'):
                barcode_obj.short_url = short_barcode_request['link']
                barcode_obj.save()
    except Barcode.DoesNotExist:

        barcode_obj = Barcode(long_url=requesting_url)

        short_barcode_request = json.loads(shorten_url(requesting_url))
        if(short_barcode_request['status'] == 'ok'):
            barcode_obj.short_url = short_barcode_request['link']

        barcode_obj.save()

    if not barcode_obj.image and barcode_obj.short_url :

        barcode_img = code128(barcode_obj.short_url)
        barcode_img.save('barcode')

        filename = 'barcode_'+barcode_obj.short_url.split('/')[1]+".svg"
        barcode_obj.image.save(filename,File(open('barcode.svg')))


    return barcode_obj

def shorten_url(url):

    # print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^",url)

    linkRequest = {
        "destination": url ,
        # "destination" : "https://barcodemoviedb.herokuapp.com/movie/baby/",
        "domain": { "fullName": "rebrand.ly" }
    }

    requestHeaders = {
    "Content-type": "application/json",
    "apikey": "2530603f8d76454fa2c3eaaa19d59f17",
    }
    try:
        response = requests.post("https://api.rebrandly.com/v1/links",
            data = json.dumps(linkRequest),
            headers=requestHeaders)
    except requests.exceptions.ConnectionError:
        response.status_code = "Connection Error"

    # print("**************",str(response.text))
    if (response.status_code == requests.codes.ok):
        link = response.json()
        return json.dumps({'status':'ok','link':link['shortUrl']})
    else:
        return json.dumps({'status':'fail'})
