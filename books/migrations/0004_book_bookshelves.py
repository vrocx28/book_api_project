# Generated by Django 4.2.11 on 2024-03-19 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_book_book_languages'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='bookshelves',
            field=models.ManyToManyField(related_name='books', to='books.bookshelf'),
        ),
    ]