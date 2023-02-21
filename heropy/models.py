from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=64)


class BookChapter(models.Model):
    chapter_number = models.IntegerField(default=0)
    content = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)


class ChapterLink(models.Model):
    chapter_dest_number = models.IntegerField(default=0)
    link = models.ForeignKey(BookChapter, on_delete=models.CASCADE, null=True, related_name='links')


class Player(models.Model):
    name = models.CharField(max_length=24)
    dexterity = models.IntegerField(default=1)
    endurance = models.IntegerField(default=1)
    luck = models.IntegerField(default=1)
    magic = models.IntegerField(default=1)
    gold = models.IntegerField(default=0)


    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True)


class PlayerItems(models.Model):
    EFFECT_CHOICE = [
        ('add', 'Add'),
        ('remove', 'Remove'),
    ]

    name = models.CharField(max_length=24)
    description = models.TextField()
    effect = models.CharField(max_length=24, choices=EFFECT_CHOICE, default='add')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True)


class PlayerMagic(models.Model):
    name = models.CharField(max_length=24)
    description =  models.TextField()
    effect = models.CharField(max_length=24)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True)

