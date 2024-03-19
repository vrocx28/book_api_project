from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Author(models.Model):
    name = models.CharField(max_length=128)
    birth_year = models.SmallIntegerField(null=True, blank=True)
    death_year = models.SmallIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Subject(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.name}"


class Language(models.Model):
    code = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return f"{self.code}"


class BookShelf(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.name}"


class Book(models.Model):
    title = models.CharField(max_length=1024)
    download_count = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    gutenberg_id = models.IntegerField(unique=True, validators=[MinValueValidator(0)])
    media_type = models.CharField(max_length=16)
    subjects = models.ManyToManyField(
        Subject, through="BookSubjects", related_name="books"
    )
    book_languages = models.ManyToManyField(
        Language, through="BookLanguages", related_name="books"
    )
    bookshelves = models.ManyToManyField(
        BookShelf, through="BookBookShelves", related_name="books"
    )
    author = models.ManyToManyField(Author, through="BookAuthors", related_name="books")

    def __str__(self):
        return f"{self.title}"


class BookAuthors(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


class BookBookShelves(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    bookshelf = models.ForeignKey(BookShelf, on_delete=models.CASCADE)


class BookLanguages(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)


class BookSubjects(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


class Format(models.Model):
    mime_type = models.CharField(max_length=32)
    url = models.URLField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.mime_type}", f"{self.url}"
