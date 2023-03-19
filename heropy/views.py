from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect

from . import hero
from .forms import FileForm

heropy = hero.HeropyV2()
book_manager = hero.BookManager()


### -- INDEX
def index(request):
    heropy.reset()
    return render(request, 'index.html', {})


### -- SETTINGS
def settings(request):
    # TODO : add settings to manage options and also show list of books
    return render(request, 'settings/settings.html', {})


### -- BOOK MANAGEMENT
def booklist(request):
    if request.method == 'POST':
        # TODO : check if a form is best suited for this kind of operations
        #  would be better to use an API call and reload the content I guess
        #  but this exercise shows that a form can be suited for the player creation
        form = FileForm(request.POST, request.FILES)

        if form.is_valid() and (new_book := request.FILES['newfile']):
            book_manager.add_book(new_book)

        elif view_book_id := request.POST.get('view_book_id'):
            return redirect('/heropy/book/%s' % view_book_id)

        elif reload_book_id := request.POST.get('reload_book_id'):
            book_manager.reload_book(reload_book_id)

        elif delete_book_id := request.POST.get('delete_book_id'):
            book_manager.delete_book(delete_book_id)

    return render(request, 'books/book_list.html', {
        'books': book_manager.show_book_list(),
    })


def start(request):
    if request.method == 'POST':
        current_player = heropy.create_player(
            name=request.POST["player_name"],
            dexterity=int(request.POST["player_dex"]),
            endurance=int(request.POST["player_end"]),
            luck=int(request.POST["player_luck"]),
            magic=int(request.POST["player_magic"]),
            book_id=int(request.POST["player_book"]),
        )

        return redirect('/heropy/book/%s' % current_player.book.id)

    return render(request, 'start/start.html', {
        'titles': book_manager.show_book_list(),
    })


def load(request):
    if request.method == 'POST':
        if player_id := request.POST.get('player_id'):
            current_player = heropy.load_player(player_id)
            return redirect('/heropy/book/chapter/%s/%s' % (
                current_player.book.id, current_player.chapter.chapter_number if current_player.chapter else 1))

    return render(request, 'load/load.html', {
        'players': heropy.show_player_list(),
    })


def book(request, book_id):
    current_player = heropy.current_player
    current_book = book_manager.get_book(book_id)

    try:
        context = {
            'id': current_book.id,
            'title': current_book.title,
            'chapters': current_book.chapters.all,
            'player': current_player,
        }
    except Exception as e:
        raise Http404(e)

    return render(request, 'books/book.html', context)


def chapter(request, book_id, chapter_id):
    try:
        player = heropy.current_player
        player.book = book_manager.get_book(book_id)
        player.chapter = player.book.chapters.get(chapter_number=chapter_id)
        player.save()

        context = {
            'name': player.name,
            'dexterity': player.dexterity,
            'endurance': player.endurance,
            'luck': player.luck,
            'magic': player.magic,
            'gold': player.gold,
            'book_id': player.book.id,
            'chapter': player.chapter,
        }

    except Exception as e:
        raise Http404(e)

    return render(request, 'chapters/chapter.html', context)


def stat(request, stat_name, value):
    try:
        player = heropy.current_player

        value = int(value)

        if stat_name == 'endurance':
            player.endurance += value
        elif stat_name == 'dexterity':
            player.dexterity += value
        elif stat_name == 'luck':
            player.luck += value
        elif stat_name == 'magic':
            player.magic += value

        player.save()

        context = {
            'name': player.name,
            'dexterity': player.dexterity,
            'endurance': player.endurance,
            'luck': player.luck,
            'magic': player.magic,
            'gold': player.gold,
        }
    except Exception as e:
        raise Http404(e)

    return JsonResponse(context)
