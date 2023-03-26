#!/usr/bin/env python
import functools
import logging
import re

import fitz

from heropy.models import Book, BookChapter, ChapterLink, ChapterBattle, Player

_logger = logging.getLogger(__name__)


class BookManager:
    UPLOAD_PATH = 'heropy/static/uploads/'
    SINGLE_BATTLE_PATTERN = r'\s?([A-Z\s]+)\s?HABIL[E|I]TÉ\s?:\s?(\d+)\s?ENDURANCE\s?:\s?(\d+)'
    MULTI_BATTLE_PATTERN = r'\s?HABIL[E|I]TÉ\s?ENDURANCE\s?(?:([a-zA-Z\s]+)\s?(\d+)\s+(\d+))'

    def __init__(self):
        pass

    def _load_battles(self, chapter):
        return True

    def _load_links(self, chapter):
        return True

    def _load_book(self, book):
        book_document = fitz.open(book.path)

        # parsing indexes
        chapter_index = -1

        chapter_dict = {}

        # iterate over all pages of the document
        for index in range(0, book_document.page_count):
            page = book_document.load_page(index)
            text = page.get_text()

            if index < 3:
                print("TODO : check if we find a line with the authors name "
                      "so we can retrieve the next line as the title of the book")

            # split text between chapter keys and content
            for text_line in text.splitlines(True):
                if (stripped_chapter_num := text_line.strip()).isdigit():
                    stripped_chapter_num = int(stripped_chapter_num)

                    if (stripped_chapter_num - chapter_index <= 2
                            and stripped_chapter_num not in chapter_dict):
                        chapter_dict[stripped_chapter_num] = ''
                        chapter_index = stripped_chapter_num
                        continue

                if chapter_index > 0:
                    # indexing content of the current chapter
                    chapter_dict[chapter_index] += text_line
                else:
                    # if no chapter is found there, we are parsing the rules
                    print('TODO : Check for spells (vol 2)')

                    print('TODO : Check for potions and equipment (vol 1 + 3)')

        chapter_bulk = []
        link_bulk = []
        battle_bulk = []

        regex_links = {}

        for number, content in chapter_dict.items():
            regex_battles = re.findall(self.SINGLE_BATTLE_PATTERN, content)

            if not regex_battles:
                print("TODO : regex_battles = re.findall(r'MULTI_BATTLE_PATTERN', content)")

            book_chapter = BookChapter(
                chapter_number=number,
                content=content.replace('\n', '<br/>'),
                book=book,
            )

            for battle in regex_battles:
                battle_bulk.append(ChapterBattle(
                    name=battle[0],
                    dexterity=int(battle[1]),
                    endurance=int(battle[2]),
                    chapter=book_chapter,
                ))

            chapter_bulk.append(book_chapter)

            regex_links[book_chapter.chapter_number] = set(r for r in re.findall(r'\bau\s+(\d+)', content))

        for chapter, links in regex_links.items():
            chapter_src = list(filter(lambda x: x.chapter_number == chapter, chapter_bulk)).pop()

            for link in links:
                chapter_dest = list(filter(lambda x: x.chapter_number == int(link), chapter_bulk)).pop()
                link_bulk.append(ChapterLink(
                    chapter_dest_number=link,
                    chapter_src=chapter_src,
                    chapter_dest=chapter_dest,
                ))

        BookChapter.objects.bulk_create(chapter_bulk)
        ChapterLink.objects.bulk_create(link_bulk)
        ChapterBattle.objects.bulk_create(battle_bulk)

        book.loaded = True

        book.save()

        return book

    def add_book(self, file):
        if file.name.endswith('.pdf') and not Book.objects.filter(title__contains=file.name):
            with open(self.UPLOAD_PATH + file.name, 'wb+') as dest:
                for c in file.chunks():
                    dest.write(c)

                book = Book(title=file, path=self.UPLOAD_PATH + file.name, loaded=False)
                book.save()

                self._load_book(book)

        return Book.objects.all()

    def delete_book(self, book_id):
        Player.objects.filter(book=book_id).delete()
        Book.objects.get(pk=book_id).delete()
        return True

    def update_book(self):
        return False

    def reload_book(self, book_id):
        # get current book
        current_book = Book.objects.get(pk=book_id)

        # prepare update for players
        player_update = {}
        for player in Player.objects.filter(book=current_book):
            player_update[player] = player.chapter.chapter_number

        # delete chapters of the book
        BookChapter.objects.filter(book=current_book).delete()

        # reload book
        self._load_book(current_book)

        # update linked players to the correct chapter
        for player, chapter_number in player_update.items():
            player.chapter = current_book.chapters.get(chapter_number=chapter_number)
            player.save()

        return True

    def get_book(self, book_id):
        return Book.objects.get(pk=book_id)

    def show_book_list(self):
        return Book.objects.all()


class HeropyV2:
    def __init__(self):
        _logger.info('__init__ call')
        self.current_player = False

    def reset(self):
        _logger.info('reset call')
        self.current_player = False

    def show_player_list(self):
        return Player.objects.all()

    def create_player(self, name='', dexterity=-1, endurance=-1, luck=-1, magic=-1, book_id=-1):
        current_book = Book.objects.get(pk=book_id)

        player = Player(
            name=name,
            dexterity=dexterity,
            endurance=endurance,
            luck=luck,
            magic=magic,
            gold=0,
            book=current_book)

        player.save()

        self.current_player = player

        return self.current_player

    def load_player(self, player_id):
        self.current_player = Player.objects.get(pk=player_id)

        return self.current_player
