from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=64)
    path = models.CharField(max_length=255)
    loaded = models.BooleanField()


class BookChapter(models.Model):
    chapter_number = models.IntegerField(default=0)
    content = models.TextField()
    has_battle = models.BooleanField(default=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, related_name='chapters')


class ChapterLink(models.Model):
    chapter_dest_number = models.IntegerField(default=0)
    link = models.ForeignKey(BookChapter, on_delete=models.CASCADE, null=True, related_name='links')


class ChapterBattle(models.Model):
    name = models.CharField(max_length=64)

    dexterity = models.IntegerField(default=1)
    endurance = models.IntegerField(default=1)

    chapter = models.ForeignKey(BookChapter, on_delete=models.CASCADE, null=True, related_name='ennemies')


class Player(models.Model):
    name = models.CharField(max_length=24)
    dexterity = models.IntegerField(default=1)
    endurance = models.IntegerField(default=1)
    luck = models.IntegerField(default=1)
    magic = models.IntegerField(default=1)
    gold = models.IntegerField(default=0)

    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True)
    chapter = models.ForeignKey('BookChapter', on_delete=models.DO_NOTHING, null=True)


class PlayerItem(models.Model):
    EFFECT_CHOICE = [
        ('add', 'Add'),
        ('remove', 'Remove'),
    ]

    name = models.CharField(max_length=24)
    description = models.TextField()
    effect = models.CharField(max_length=24, choices=EFFECT_CHOICE, default='add')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, related_name='items')


class PlayerSpell(models.Model):
    name = models.CharField(max_length=24)
    description = models.TextField()
    effect = models.CharField(max_length=24)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, related_name='spells')
