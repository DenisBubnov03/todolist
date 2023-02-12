import random
import string

from django.db import models

class TgUser(models.Model):
    tg_id = models.BigIntegerField(verbose_name='telegram id', unique=True)
    tg_chat_id = models.BigIntegerField(verbose_name='telegram chat id')
    username = models.CharField(verbose_name='имя пользователя telegram',
                                max_length=520,
                                null=True,
                                blank=True,
                                default=None)
    user = models.ForeignKey('core.User',
                             models.PROTECT,
                             null=True,
                             blank=True,
                             verbose_name='связанный пользователь',
                             default=None)
    verification_code = models.CharField(verbose_name='код подтверждения', max_length=12)

    class Meta:
        verbose_name = 'пользователь telegram'
        verbose_name_plural = 'пользователи telegram'

    def __str__(self):
        return self.username

    def set_verification_code(self) -> None:
        self.verification_code = ''.join(
            random.choice(string.digits + string.ascii_letters) for _ in range(12)
        )


