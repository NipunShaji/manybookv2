from django.urls import path
from books.views import (
        home,
        addbook,\
        # me,
        bookview,\
        catview,
        search,
        addtoshelf,
        bookshelf,
        pdfviewer,
        deletebook,
        setcurrentbook,
        setcurrentpage,
        downloaded,
        uploadslist,
        downloadlist,
        checkisbn,
        setrating,
        newcomment,
        newreply,
        deletecomment,
        deletereply,
)

app_name = 'books'

urlpatterns = [
        path('', home, name='home'),
        path('addbook/', addbook, name='addbook'),
        path('book/', bookview, name='bookview'),
        path('cat/', catview, name='catview'),
        path('search/', search, name='search'),
        path('addtoshelf/', addtoshelf, name='addtoshelf'),
        path('bookshelf/', bookshelf, name='bookshelf'),
        path('bookview/', pdfviewer, name='pdfviewer'),
        path('deleteshelf/', deletebook, name='deleteshelf'),
        path('setcurrentbook/', setcurrentbook, name='setcurrentbook'),
        path('setcurrentpage', setcurrentpage, name='setcurrentpage'),
        path('download/', downloaded, name='downloaded'),
        path('uploadlist', uploadslist, name='uploadslist'),
        path('downloadlist/', downloadlist, name='downloadlist'),
        path('checkisbn/', checkisbn, name='checkisbn'),
        path('setrating/', setrating, name='setrating'),
        path('newcomment/', newcomment, name='newcomment'),
        path('newreply/', newreply, name='newreply'),
        path('deletecomment/', deletecomment, name='deletecomment'),
        path('deletereply/', deletereply, name='deletereply'),
]
