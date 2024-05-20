# Register your models here.
from django.contrib import admin
from .models import Book, BookSpell, BookItem, BookChapter, ChapterLink, ChapterBattle, Player, PlayerItem, PlayerSpell

admin.site.register(Book)
admin.site.register(BookChapter)
admin.site.register(BookSpell)
admin.site.register(BookItem)
admin.site.register(ChapterLink)
admin.site.register(ChapterBattle)
admin.site.register(Player)
admin.site.register(PlayerItem)
admin.site.register(PlayerSpell)
