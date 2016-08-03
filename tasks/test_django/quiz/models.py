from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Question(models.Model):
    author = models.ForeignKey(verbose_name=_('Автор'), to=User)
    title = models.CharField(verbose_name=_('Название'), max_length=200)
    text = models.TextField(verbose_name=_('Текст'))
    is_active = models.BooleanField(verbose_name=_('Отображать?'), default=True)

    class Meta:
        verbose_name = _('Вопрос')
        verbose_name_plural = _('Вопросы')

    def __str__(self):
        return self.title


class Choice(models.Model):
    question = models.ForeignKey(verbose_name=_('Вопрос'), to=Question, on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_('Название'), max_length=200)
    text = models.TextField(verbose_name=_('Текст'))
    position = models.IntegerField(verbose_name=_('Сортировка'), default=0)
    is_active = models.BooleanField(verbose_name=_('Отображать?'), default=True)

    class Meta:
        verbose_name = _('Ответ')
        verbose_name_plural = _('Ответы')

    def __str__(self):
        return self.title
