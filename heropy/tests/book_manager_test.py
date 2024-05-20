from unittest.mock import MagicMock
from django.core.files.uploadedfile import SimpleUploadedFile

from heropy.book_manager import BookManager
# pytest -s to have stdout in case logging is set on tests
import pytest

from heropy.models import Book


@pytest.mark.parametrize(
    ("page_range", "max_page", "expected_results"),
    [
        ('1-5', 1, ([(1, 5)], [], 5)),
        ('1-5', 1, ([(1, 5)], [], 5)),
        ('1-5', 1, ([(1, 5)], [], 5)),
        ('1-5', 1, ([(1, 5)], [], 5)),
        ('1-5', 1, ([(1, 5)], [], 5)),
    ]
)
def test_get_page_ranges(page_range, max_page, expected_results):
    result = BookManager()._get_page_ranges(page_range, max_page)

    assert result == expected_results


@pytest.mark.django_db
def test_add_book():
    file = SimpleUploadedFile('test.pdf', '')

    # MagicMock() to mock an object and override attributes

    test_id = BookManager().add_book(file)

    assert Book.objects.count() == 1

    test = Book.objects.get(pk=test_id)

    assert test
    assert test.title == 'test.pdf'
    assert test.file == file
    assert not test.loaded
