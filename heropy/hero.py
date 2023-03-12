#!/usr/bin/env python
import logging
import re

import fitz

from heropy.models import Book, BookChapter, ChapterLink, ChapterBattle, Player

_logger = logging.getLogger(__name__)


class BookManager:
    UPLOAD_PATH = 'heropy/static/uploads/'

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
            if index < 0:
                continue

            page = book_document.load_page(index)
            text = page.get_text()

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
                    chapter_dict[chapter_index] += text_line

        chapter_bulk = []
        link_bulk = []
        battle_bulk = []

        for number, content in chapter_dict.items():
            regex_battles = re.findall(r'(\w+)\s+HABIL[E|I]TÉ:\s+(\d+)\s+ENDURANCE:\s+(\d+)', content)

            book_chapter = BookChapter(
                chapter_number=number,
                content=content.replace('\n', '<br/>'),
                book=book,
                has_battle=True if regex_battles else False  # TODO : see if we want to create a new object
            )

            for battle in regex_battles:
                battle_bulk.append(ChapterBattle(
                    name=battle[0],
                    dexterity=int(battle[1]),
                    endurance=int(battle[2]),
                ))

            chapter_bulk.append(book_chapter)

            regex_links = re.findall(r'\bau\s+(\d+)', content)

            for lid in set(r for r in regex_links if regex_links):
                chapter_link = ChapterLink(
                    chapter_dest_number=lid,
                    link=book_chapter)
                link_bulk.append(chapter_link)

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
        Book.objects.get(pk=book_id).chapters
        self._load_book(Book.objects.get(pk=book_id))
        return

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
