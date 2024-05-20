# TODO : add validators as regex for fields containing pages
from django import forms
from django.core.validators import RegexValidator, ValidationError

import re


def validate_page_range(value):
    for v in value.split(','):
        if not re.match(r'\d+-\d+|\d+', v):
            raise ValidationError('Not matching regex')

    return True


class PlayerForm(forms.Form):
    player_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'nes-input is-dark'}),
        label="Your name",
        required=True)
    player_endurance = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'nes-input is-dark', 'id': 'endurance_field'}),
        label="Endurance",
        required=True)
    player_dexterity = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'nes-input is-dark', 'id': 'dexterity_field'}),
        label="Dexterity",
        required=True)
    player_luck = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'nes-input is-dark', 'id': 'luck_field'}),
        label="Luck",
        required=True)
    player_magic = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'nes-input is-dark', 'id': 'magic_field'}),
        label="Magic",
        required=True)
    player_book = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'nes-input is-dark'}),
        label="Book",
        required=True)
    # player_avatar = forms.CharField(label="Avatar", required=True)


class BookForm(forms.Form):
    book_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'nes-input is-dark'}),
        label="Book title",
        required=True)
    nb_chapters = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'nes-input is-dark'}),
        label="Number of chapters",
        required=True)
    intro_pages = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'nes-input is-dark', 'placeholder': 'ex. : 0-10,11,12'}),
        label="Pages for introduction",
        validators=[validate_page_range],
        required=True)
    item_pages = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'nes-input is-dark', 'placeholder': 'ex. : 0-10,11,12'}),
        label="Pages for items",
        validators=[validate_page_range],
        required=True)
    spell_pages = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'nes-input is-dark', 'placeholder': 'ex. : 0-10,11,12'}),
        label="Pages for spells",
        validators=[validate_page_range],
        required=True)
