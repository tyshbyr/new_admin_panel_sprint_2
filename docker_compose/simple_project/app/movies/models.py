import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('Name'), max_length=255)
    description = models.TextField(_('Description'), default='', blank=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self) -> str:
        return self.name


class Person(UUIDMixin, TimeStampedMixin):

    class Gender(models.TextChoices):
        MALE = 'male', _('male')
        FEMALE = 'female', _('female')

    full_name = models.CharField(_('Name'), max_length=255)
    gender = models.TextField(_('gender'), choices=Gender.choices, default='')

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
        indexes = [
            models.Index(
                fields=['full_name',], 
                name='full_name_idx'),\
        ]

    def __str__(self) -> str:
        return self.full_name


class Filmwork(UUIDMixin, TimeStampedMixin):

    class Type(models.TextChoices):
        MOVIE = 'movie', _('Movie')
        TV_SHOW = 'tv_show', _('TV Show')

    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'),  default='', blank=True)
    creation_date = models.DateField(_('Creation date'), blank=True)
    rating = models.FloatField(_('Rating'), blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])
    type = models.CharField(_('Type'), max_length=7, choices=Type.choices)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')
    certificate = models.CharField(
        _('certificate'),
        max_length=512,
        default='', blank=True)
    file_path = models.FileField(
        _('file'),
        default='',
        upload_to='movies/', blank=True)

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')
        indexes = [
            models.Index(
                fields=['title',], 
                name='title_idx'),
            models.Index(
                fields=['creation_date',], 
                name='creation_date_idx'),
            models.Index(
                fields=['rating',], 
                name='rating_idx'),
        ]

    def __str__(self) -> str:
        return self.title




class PersonFilmwork(UUIDMixin):
    
    class Role(models.TextChoices):
        ACTOR = 'actor', _('actor')
        DIRECTOR = 'director', _('director')
        WRITER = 'writer', _('writer')
    
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    person = models.ForeignKey(
        Person,
        verbose_name=_('Person'),
        on_delete=models.CASCADE)
    role = models.TextField(_('Role'), choices=Role.choices, default='')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('Actor/creator')
        verbose_name_plural = _('Actors/creators')
        constraints = [
            models.UniqueConstraint(
                fields=['film_work_id', 'person_id', 'role'],
                name='film_work_person_role_idx'),
        ]

    def __str__(self) -> str:
        return self.person.full_name


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre,
        verbose_name=_('Genre'),
        on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('Genre of film')
        verbose_name_plural = _('Genres of film')
        constraints = [
            models.UniqueConstraint(
                fields=['genre_id', 'film_work_id'],
                name='genre_film_work_idx'),
        ]

    def __str__(self) -> str:
        return self.genre.name
