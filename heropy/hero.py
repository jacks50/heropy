#!/usr/bin/env python

import fitz
import os
import re

from heropy.models import Book, BookChapter, ChapterLink, Player

class HeropyV2():
    def __init__(self):
        self.reset()

    def reset(self):
        self.current_player = False

    def load_books(self):
        DEFAULT_PATH = f'{os.path.dirname(__file__)}/data'

        for file in os.listdir(DEFAULT_PATH):
            if file.endswith('.pdf'):
                if not Book.objects.filter(title__contains=file):
                    book = Book(title = file)
                    book.save()

                    self.load_book(book, f'{DEFAULT_PATH}/{file}')

        return Book.objects.all()

    def load_book(self, book: Book, book_path):
        book_document = fitz.open(book_path)

        # if required to bypass some chapters
        offset = 0

        # parsing indexes
        current_chapter = False
        chapter_index = -1

        # iterate over all pages of the document
        for index in range(0, book_document.page_count):
            if index < offset:
                continue

            page = book_document.load_page(index)
            text = page.get_text()

            # split text between chapter keys and content
            for text_line in text.splitlines(True):
                if (stripped_chapter_num := text_line.strip()).isdigit():
                    stripped_chapter_num = int(stripped_chapter_num)

                    if (chapter_index and 
                        stripped_chapter_num - chapter_index <= 2 and
                        not book.bookchapter_set.filter(chapter_number=stripped_chapter_num)):
                        # TODO : optmise calls here
                        # should be creating a new chapter and use regex, we are writing to the DB at each line
                        # wtf
                        chapter = BookChapter(
                            chapter_number=stripped_chapter_num, 
                            book=book
                        )

                        chapter.save()
 
                        current_chapter = chapter
                        chapter_index = stripped_chapter_num
                elif current_chapter:
                    chapter.content += text_line
                    chapter.save()

        for chapter in book.bookchapter_set.all():
            result = re.findall(r'\bau\s+(\d+)', chapter.content)
            for lid in set(r for r in result if result):
                link = ChapterLink(chapter_dest_number=lid, link=chapter)
                link.save()
            chapter.save()
            
        return True

    def save_player(self, name='',dexterity=-1, endurance=-1, luck=-1, magic=-1, book_id=-1):
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

        return player