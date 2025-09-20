from django.db import models

class Book(models.Model):
    GENRE_CHOICES = [
        ('FIC', 'Fiction'),
        ('NF', 'Non-Fiction'),
        ('FAN', 'Fantasy'),
        ('SCI', 'Science'),
        ('HIS', 'History'),
        ('BIO', 'Biography'),
        ('MYS', 'Mystery'),
        ('ROM', 'Romance'),
        ('HOR', 'Horror'),
        ('POE', 'Poetry'),
    ]

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField(null=True, blank=True)
    pages = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    # 👇 add genre using the choices
    genre = models.CharField(
        max_length=20,
        choices=GENRE_CHOICES,
        default='FIC',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} — {self.author} ({self.get_genre_display()})"
