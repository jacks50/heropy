from django.db import models


# TODO : see if items / spells must be linked to a book
class Book(models.Model):
    title = models.CharField(max_length=64)
    file = models.FileField(null=True)
    introduction = models.TextField(null=True)
    loaded = models.BooleanField()


class BookItem(models.Model):
    TYPE_CHOICE = [
        ('consumable', 'Consumable'),
        ('equipment', 'Equipment'),
    ]

    name = models.CharField(max_length=24)
    description = models.TextField()
    type = models.CharField(max_length=24, choices=TYPE_CHOICE, default='consumable')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, related_name='book_items')


class BookSpell(models.Model):
    name = models.CharField(max_length=24)
    description = models.TextField()
    effect = models.CharField(max_length=24)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, related_name='book_spells')


class BookChapter(models.Model):
    chapter_number = models.IntegerField(default=0)
    content = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, related_name='chapters')

    def has_battle(self):
        return self.enemies.all()


class ChapterLink(models.Model):
    chapter_dest_number = models.IntegerField(default=0)
    chapter_src = models.ForeignKey(BookChapter, on_delete=models.CASCADE, null=True, related_name='links')
    chapter_dest = models.ForeignKey(BookChapter, on_delete=models.CASCADE, null=True)


class ChapterBattle(models.Model):
    name = models.CharField(max_length=64)
    dexterity = models.IntegerField(default=1)
    endurance = models.IntegerField(default=1)
    chapter = models.ForeignKey(BookChapter, on_delete=models.CASCADE, null=True, related_name='enemies')


class Player(models.Model):
    name = models.CharField(max_length=24)
    dexterity = models.IntegerField(default=1)
    endurance = models.IntegerField(default=1)
    luck = models.IntegerField(default=1)
    magic = models.IntegerField(default=1)
    gold = models.IntegerField(default=0)

    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True)
    chapter = models.ForeignKey('BookChapter', on_delete=models.SET_NULL, null=True)


class PlayerItem(models.Model):
    TYPE_CHOICE = [
        ('consumable', 'Consumable'),
        ('equipment', 'Equipment'),
    ]

    name = models.CharField(max_length=24)
    description = models.TextField()
    type = models.CharField(max_length=24, choices=TYPE_CHOICE, default='consumable')
    nb_usages = models.IntegerField(default=1)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, related_name='items')


class PlayerSpell(models.Model):
    name = models.CharField(max_length=24)
    description = models.TextField()
    effect = models.CharField(max_length=24)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, related_name='spells')
