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

        if form.is_valid():
            book_manager.add_book(request.FILES['newfile'])

        elif reload_book_id := request.POST.get('reload_book_id'):
            book_manager.reload_book(reload_book_id)

        elif delete_book_id := request.POST.get('delete_book_id'):
            book_manager.delete_book(delete_book_id)

    return render(request, 'books/book_list.html', {
        'titles': book_manager.show_book_list(),
    })


def start(request):
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


def book(request):
    if request.method == 'POST':
        current_player = heropy.create_player(
            name=request.POST["player_name"],
            dexterity=int(request.POST["player_dex"]),
            endurance=int(request.POST["player_end"]),
            luck=int(request.POST["player_luck"]),
            magic=int(request.POST["player_magic"]),
            book_id=int(request.POST["player_book"]),
        )
    else:
        current_player = heropy.current_player

    try:
        context = {
            'id': current_player.book.id,
            'title': current_player.book.title,
            'chapters': current_player.book.chapters.all
        }
    except Exception as e:
        raise Http404(e)

    return render(request, 'books/book.html', context)


def chapter(request, book_id, chapter_id):
    page_dest = 'chapters/chapter.html'

    try:
        player = heropy.current_player
        player.book = book_manager.get_book(book_id)
        player.chapter = player.book.chapters.get(chapter_number=chapter_id)
        player.save()

        context = {
            'name': player.name,
            'dexterity': range(player.dexterity),
            'endurance': range(player.endurance),
            'luck': range(player.luck),
            'magic': range(player.magic),
            'gold': player.gold,
            'book_id': player.book.id,
            'chapter': player.chapter,
        }

        if player.chapter.has_battle:
            page_dest = 'chapters/chapter_battle.html'

    except Exception as e:
        raise Http404(e)

    return render(request, page_dest, context)


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
