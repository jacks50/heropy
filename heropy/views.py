from django.shortcuts import render
from django.http import Http404, JsonResponse
from . import hero

heropy = hero.HeropyV2()

def index(request):
    heropy.reset()
    return render(request, 'index.html', {})

def start(request):
    try:
        context = {
            'titles': heropy.load_books(),
        }
    except Exception as e:
        raise Http404(e)

    return render(request, 'start/start.html', context)

def load(request):
    return render(request, 'load/load.html', {})

def book(request):
    current_player = heropy.save_player(
        name=request.POST["player_name"], 
        dexterity=int(request.POST["player_dex"]),
        endurance=int(request.POST["player_end"]),
        luck=int(request.POST["player_luck"]),
        magic=int(request.POST["player_magic"]),
        book_id=int(request.POST["player_book"]),      
    )

    try:
        context = {
            'id': current_player.book.id,
            'title': current_player.book.title,
            'chapters': current_player.book.bookchapter_set.all
        }
    except Exception as e:
        raise Http404(e)

    return render(request, 'books/book.html', context)

def chapter(request, book_id, chapter_id):
    try:
        player = heropy.current_player

        # TODO : check that book ids match

        selected_chapter = player.book.bookchapter_set.get(chapter_number=chapter_id)

        chapter = selected_chapter

        context = {
            'name': player.name,
            'dexterity': range(player.dexterity),
            'endurance': range(player.endurance),
            'luck': range(player.luck),
            'book_id': book_id,
            'chapter': chapter,
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

        context = {
            'name': player.name,
            'dexterity': player.dexterity,
            'endurance': player.endurance,
            'luck': player.luck,
        }
    except Exception as e:
        raise Http404(e)

    return JsonResponse(context)