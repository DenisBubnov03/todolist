from django.conf import settings
from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from bot.tg.msg_manager import MsgManager


class Command(BaseCommand):
    help = 'run bot'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.TG_BOT_TOKEN)
        self.msg_manager = MsgManager()

    def handle(self, *args, **options):
        """ Обрабатывает чат """
        offset = 0
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)

    def handle_message(self, msg: Message | None) -> None:
        """ Проверяет верификацию пользователя """
        if not msg:
            return
        tg_user, created = TgUser.objects.get_or_create(
            tg_id=msg.from_.id,
            defaults={
                'tg_chat_id': msg.chat.id,
                'username': msg.from_.username
            }
        )
        if created:
            self.tg_client.send_message(msg.chat.id, 'Привет')
        if tg_user.user:
            self.handle_verified_user(msg, tg_user)
        else:
            self.handle_user_without_verification(msg, tg_user)

    def handle_verified_user(self, msg: Message, tg_user):
        """ Обрабатывает сообщения подтверждённого пользователя и отправляет ответ """
        if not msg.text:
            return
        if msg.text.startswith('/'):
            resp = self.msg_manager.check_commands(msg, tg_user)
        else:
            resp = self.msg_manager.check_state(msg, tg_user)

        self.tg_client.send_message(msg.chat.id, resp.get('message', None))

    def handle_user_without_verification(self, msg: Message, tg_user: TgUser) -> None:
        """ Обрабатывает сообщение неподтверждённого пользователя и выдает код верификации и ссылку на сайт """
        tg_user.set_verification_code()
        tg_user.save(update_fields=['verification_code'])
        self.tg_client.send_message(
            msg.chat.id,
            f"код подтверждения:\n{tg_user.verification_code}\n"
            f"ссылка на сайт:{settings.HOST_NAME}"
        )
