import fitz
import re
import logging

from heropy.models import Book, BookSpell, BookItem, BookChapter, ChapterLink, ChapterBattle, Player

from .hero import HeropyException

_logger = logging.getLogger(__name__)


class BookManager:
    SINGLE_BATTLE_PATTERN = r'\s?([A-zÀ-ú\s]+)\s?HABIL[E|I]TÉ\s?:\s?(\d+)\s?ENDURANCE\s?:\s?(\d+)'
    MULTI_BATTLE_PATTERN = r'(?:((?:[A-zÀ-ú]+\s+){1,3})\n\s*(\d+)\s+(\d+))+'
    SPELL_PATTERN = r'\n?([A-ZÀ-Ú]+\s?)\n'

    def __init__(self):
        self._loaded_book = False
        pass

    def _load_battles(self, chapter):
        return True

    def _load_links(self, chapter):
        return True

    def _get_page_ranges(self, page_range, max_page):
        single_pages = []
        page_ranges = []

        for prange in page_range.split(','):
            if prange.isdigit():
                single_pages.append(int(prange)-1)
            elif '-' in prange:
                page_from_str, page_to_str = prange.split('-', 2)
                page_ranges.append((int(page_from_str)-1, int(page_to_str)-1))

        flattened_pages = [p for r in page_ranges for p in r]
        flattened_pages.extend(single_pages)
        max_page_found = max(flattened_pages)

        return page_ranges, single_pages, max_page_found if max_page_found > max_page else max_page

    def _parse_introduction(self, book, book_document, page_intro, max_page):
        _logger.warning(f'Parsing introduction starting at page {page_intro}')

        page_ranges, single_pages, new_max = self._get_page_ranges(page_intro, max_page)

        introduction = ''

        for page_range in page_ranges:
            for index in range(page_range[0], page_range[1]):
                page = book_document.load_page(index)
                introduction += page.get_text()

        for single_page in single_pages:
            page = book_document.load_page(single_page)
            introduction += page.get_text()

        book.introduction = introduction

        return new_max

    def _parse_items(self, book, book_document, page_items, max_page):
        _logger.warning(f'Parsing items starting at page {page_items}')

        page_ranges, single_pages, new_max = self._get_page_ranges(page_items, max_page)

        # for page_range in page_ranges:
        #     for index in range(page_range[0], page_range[1]):
        #         page = book_document.load_page(index)
        #
        # for single_page in single_pages:
        #     page = book_document.load_page(single_page)

        # Default items

        BookItem.objects.bulk_create([
            BookItem(
                name="Repas", description="Un repas vous rend 4 points d'ENDURANCE (à utiliser hors combat)",
                type="consumable", book=book),
            BookItem(
                name="Potion d'Adresse", description="Rend tous vos points d'Habileté", type="consumable",
                book=book),
            BookItem(
                name="Potion de Vigueur", description="Rend tous vos points d'Endurance", type="consumable",
                book=book),
            BookItem(
                name="Potion de Fortune", description="Rend tous vos points de Chance + 1 point supplémentaire",
                type="consumable", book=book),
        ])

        return new_max

    def _parse_spells(self, book, book_document, page_spells, max_page):
        _logger.warning(f'Parsing spells starting at page {page_spells}')

        """
        TODO
        Need to iterate trough single and ranges consecutively to not mix pages incorrectly
        From the whole text content, need to split with each spell start => maybe "\n NAME UPPERCASE \n" ?
        Then retrieve text until next token that matches the pattern above
        """

        page_ranges, single_pages, new_max = self._get_page_ranges(page_spells, max_page)

        loaded_pages = []

        for page_range in page_ranges:
            for index in range(page_range[0], page_range[1]+1):
                loaded_pages.append(book_document.load_page(index))

        for single_page in single_pages:
            loaded_pages.append(book_document.load_page(single_page))

        loaded_pages.sort(key=lambda p: p.number)

        spell_dict = {}

        for loaded_page in loaded_pages:
            page_blocks = loaded_page.get_text('blocks')
            current_spell = ''

            for page_block in page_blocks:
                # 4 is content of text, previous indexes are x/y coordinates
                text_block = page_block[4]

                if current_spell:
                    spell_dict[current_spell] += text_block
                elif (current_spell := text_block.strip()).isupper():
                    spell_dict[current_spell] = ''

        for spell, desc in spell_dict.items():
            BookSpell(name=spell, description=desc, effect='-', book=book).save()

        return new_max

    def _parse_chapters(self, book, book_document, nb_chapters, page_start):
        _logger.warning(f'Parsing chapters starting at page {page_start}')

        chapter_index = -1

        chapter_dict = {}

        # TODO : Refactor using blocks as done in spells
        # if block[4] is only numbers -> chapter
        # need to check with previous chapter just to be sure that the block is not a link to another chapter
        # that jumped a page

        for index in range(page_start, book_document.page_count):
            page = book_document.load_page(index)
            text = page.get_text()

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

        regex_links = {}

        for number, content in chapter_dict.items():
            _logger.warning(f'Loading chapter number {number}')
            regex_battles = re.findall(self.SINGLE_BATTLE_PATTERN, content)

            if not regex_battles:
                regex_battles = re.findall(self.MULTI_BATTLE_PATTERN, content)

            # TODO : Highlight chance time
            re.sub('(tente[r,z] votre chance)', r'<i>\1</i>', content, flags=re.IGNORECASE)

            book_chapter = BookChapter(
                chapter_number=number,
                content=content.replace('\n', '<br/>'),
                book=book,
            )

            for battle in regex_battles:
                battle_bulk.append(ChapterBattle(
                    name=battle[0].replace('ENDURANCE', ''), # TODO : remove and correct this
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

        return True

    def add_book(self, file):
        if not file.name.endswith('.pdf'):
            raise HeropyException('File must be a PDF')

        book = Book(title=file.name, file=file, loaded=False)
        book.save()

        return book.id

    def load_book(self, book_id, book_title=False, nb_chapters=0, page_intro='', page_items='', page_spells=''):
        book = Book.objects.get(pk=book_id)

        book_document = fitz.open(book.file.path)

        chapter_page_start = self._parse_introduction(book, book_document, page_intro, -1)

        chapter_page_start = self._parse_items(book, book_document, page_items, chapter_page_start)

        chapter_page_start = self._parse_spells(book, book_document, page_spells, chapter_page_start)

        self._parse_chapters(book, book_document, nb_chapters, chapter_page_start)

        book.title = book_title
        book.loaded = True
        book.save()

        return True

    def delete_book(self, book_id):
        Player.objects.filter(book=book_id).delete()
        Book.objects.get(pk=book_id).delete()
        return True

    # def reload_book(self, book_id):
    #     # get current book
    #     current_book = Book.objects.get(pk=book_id)
    #
    #     # prepare update for players
    #     player_update = {}
    #     for player in Player.objects.filter(book=current_book, chapter__isnull=False):
    #         player_update[player] = player.chapter.chapter_number
    #
    #     # delete chapters of the book
    #     BookChapter.objects.filter(book=current_book).delete()
    #
    #     # reload book
    #     self.load_book(current_book)
    #
    #     # update linked players to the correct chapter
    #     for player, chapter_number in player_update.items():
    #         player.chapter = current_book.chapters.get(chapter_number=chapter_number)
    #         player.save()
    #
    #     return True

    def get_book(self, book_id):
        return Book.objects.get(pk=book_id)

    def show_book_list(self):
        return Book.objects.all()
