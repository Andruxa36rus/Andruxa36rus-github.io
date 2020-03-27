from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    return 'uploads/{0}/{1}'.format(instance.username, filename)

class Post(models.Model):
    username = models.CharField('Имя пользователя', max_length=30)
    title = models.CharField('Название поста', max_length=100)
    text = models.TextField('Содержание поста')
    datetime = models.DateTimeField('Дата публикации')
    image = models.ImageField(upload_to=user_directory_path, default='', blank=True)

    changed = models.BooleanField('Изменена', default=False)
    changed_datetime = models.DateTimeField('Дата изменения', null=True, blank=True)

    # Модель Post связана с дефолтной моделью User м2м
    # таблица связей для лайков
    likedone = models.ManyToManyField(User, related_name='users_post_like', blank=True)
    thumbnumber = models.IntegerField(default=0, verbose_name='Число лайков', blank=True)

    # таблица связей для просмотров
    viewdone = models.ManyToManyField(User, related_name='users_post_view')
    viewcount = models.IntegerField(default=0, verbose_name='Количество просмотров')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.username
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    username = models.CharField('Имя пользователя', max_length=30)
    text = models.TextField('Содержание комментария')
    datetime = models.DateTimeField('Дата публикации')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.username
