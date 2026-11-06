from django.contrib.auth.models import AbstractUser

from django.db import models

class User(AbstractUser):
    fio = models.CharField('ФИО', max_length=150)
    consent = models.BooleanField('Согласие на обработку данных', default=False)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_work', 'Принято в работу'),
        ('done', 'Выполнено'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')#как по тз, - категория => - заявки
    image = models.ImageField('Фото/план помещения', upload_to='applications/')
    status = models.CharField('Статус', max_length=10, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)# ставится сама, оно умное:)
    comment = models.TextField('Комментарий', blank=True)# для "Принято в работу"
    design_image = models.ImageField('Изображение дизайна', upload_to='designs/',
                                     blank=True, null=True)# для "Выполнено"

    class Meta:
        ordering = ['-created_at']# новые заявки сверху(перевернутая сортировка)
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return self.title