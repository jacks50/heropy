from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect

from . import book_manager, forms, hero

heropy = hero.HeropyV2()
book_manager = book_manager.BookManager()


### -- INDEX
def index(request):
    heropy.reset()
    return render(request, 'index.html', {})


### -- SETTINGS
def settings(request):
    # TODO : add settings to manage options and also show list of books
    return render(request, 'settings/settings.html', {})


### -- BOOK MANAGEMENT
def book_list(request):
    if request.method == 'POST':
        # TODO : check if a form is best suited for this kind of operations
        #  would be better to use an API call and reload the content I guess
        #  but this exercise shows that a form can be suited for the player creation
        if new_book := request.FILES.get('newfile', False):
            new_book_id = book_manager.add_book(new_book)
            return redirect(f'/heropy/book_config/{new_book_id}')

        elif view_book_id := request.POST.get('view_book_id'):
            return redirect(f'/heropy/book/{view_book_id}')

        elif reload_book_id := request.POST.get('reload_book_id'):
            return redirect(f'/heropy/book_config/{reload_book_id}')

        elif delete_book_id := request.POST.get('delete_book_id'):
            book_manager.delete_book(delete_book_id)

    return render(request, 'books/book_list.html', {
        'books': book_manager.show_book_list(),
    })


def book_config(request, book_id):
    current_book = book_manager.get_book(book_id)

    if request.method == 'POST':
        form = forms.BookForm(request.POST)

        if not form.is_valid():
            return render(request, 'books/book_config.html', {
                'loaded_book': current_book,
                'form': form,
            })

        result = book_manager.load_book(
            book_id,
            book_title=form.cleaned_data['book_name'],
            nb_chapters=form.cleaned_data['nb_chapters'],
            page_intro=form.cleaned_data['intro_pages'],
            page_items=form.cleaned_data['item_pages'],
            page_spells=form.cleaned_data['spell_pages']
        )

        return render(request, 'books/book_config.html', {
            'loaded_book': current_book,
            'form': form,
            'result': result,
        })

    return render(request, 'books/book_config.html', {
        'loaded_book': current_book,
        'form': forms.BookForm(initial={
            'book_name': current_book.title.replace('.pdf', ''),
            'nb_chapters': 400,
        }),
    })


def start(request):
    if request.method == 'POST':
        form = forms.PlayerForm(request.POST)

        if form.is_valid():
            current_player = heropy.create_player(
                name=form.cleaned_data["player_name"],
                dexterity=form.cleaned_data["player_dexterity"],
                endurance=form.cleaned_data["player_endurance"],
                luck=form.cleaned_data["player_luck"],
                magic=form.cleaned_data["player_magic"],
                book_id=form.cleaned_data["player_book"],
            )

            return redirect('/heropy/book/%s' % current_player.book.id)

    return render(request, 'start/start.html', {
        'titles': book_manager.show_book_list(),
        'form': forms.PlayerForm(),
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


def _get_player_data(player, stat_only=False):
    player_data = {
        'name': player.name,
        'gold': player.gold,
        'stats': {
            'endurance': player.endurance,
            'dexterity': player.dexterity,
            'magic': player.magic,
            'luck': player.luck,
        }
    }

    if not stat_only:
        player_data.update({
            'book_id': player.book.id,
            'chapter': player.chapter,
        })

    return player_data


def chapter(request, book_id, chapter_id):
    try:
        player = heropy.current_player
        player.book = book_manager.get_book(book_id)
        player.chapter = player.book.chapters.get(chapter_number=chapter_id)
        player.save()

        context = _get_player_data(player)

    except Exception as e:
        raise Http404(e)

    return render(request, 'chapters/chapter.html', context)


def partial_chapter_battle(request):
    context = {}
    return render(request, '', context)


# -- PARTIAL VIEWS
def partial_player_board(request, stat_name, value):
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
        elif stat_name == 'gold':
            player.gold += value

        player.save()

        context = _get_player_data(player)
    except Exception as e:
        raise Http404(e)

    return render(request, 'chapters/chapter_player_board.html', context)


def partial_dialog_items(request):
    context = {}
    return render(request, '', context)


def partial_dialog_spells(request):
    context = {}
    return render(request, '', context)


# -- API
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
        elif stat_name == 'gold':
            player.gold += value

        player.save()

        context = _get_player_data(player, stat_only=True)
    except Exception as e:
        raise Http404(e)

    return JsonResponse(context)
