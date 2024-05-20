#!/usr/bin/env python
import logging

from heropy.models import Book, Player

_logger = logging.getLogger(__name__)


class HeropyException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


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
