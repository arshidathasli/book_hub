from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

    isbn = models.CharField(max_length=13, unique=True, default="0000000000000")  # ISBN-13 has 13 characters

    def __str__(self):
        return f"{self.title} by {self.author}, ISBN: {self.isbn}"