from enum import Enum, auto
from typing import Any

from django.conf import settings

from bot.models import TgUser
from bot.tg.dc import Message
from goals.models import Goal, GoalCategory


class MsgManager:
    def __init__(self) -> None:
        self.storage_for_create: dict[str, Any] = {}
        self.response: dict[str, str] = {}
        self.state = self.State.idle

    class State(Enum):
        idle = auto(), 'бездействие'
        category_input = auto(), 'ввод названия категории для создания цели'
        title_goal_input = auto(), 'ввод названия цели'

    def check_commands(self, msg: Message, tg_user: TgUser) -> dict[str, str]:
        """ Проверяет вводимые команды пользователя """
        match msg.text:
            case '/goals':
                self.goals(msg, tg_user)
            case '/create':
                self.start_create_goal(msg, tg_user)
            case '/cancel':
                self.cancel()
            case '/site':
                self.response['message'] = f'ссылка на сайт: {settings.HOST_NAME}'
            case _:
                self.response['message'] = 'неизвестная команда'
        return self.response

    def check_state(self, msg: Message, tg_user: TgUser) -> dict[str, str]:
        """ Проверяет состояние: бездействие, создание цели"""
        match self.state:
            case self.State.idle:
                self.response['message'] = 'введите команду'
            case self.State.category_input:
                self.category_input(msg, tg_user)
            case self.State.title_goal_input:
                self.title_goal_input(msg, tg_user)
        return self.response

    def goals(self, msg: Message, tg_user: TgUser) -> dict[str, str]:
        """ Проверяет наличие целей и выводит в тг чате их наличие """
        goals = (
            Goal.objects.filter(category__board__participants__user=tg_user.user).
            exclude(status=Goal.Status.archived)
        )
        if goals.count() > 0:
            goals_for_message = [f"# {item.id} [{item.title}]" for item in goals]
            self.response['message'] = 'ваши цели:\n' + '\n'.join(goals_for_message)
        else:
            self.response['message'] = 'список целей пуст'
        return self.response

    def category_input(self, msg: Message, tg_user: TgUser) -> dict[str, str]:
        """ Находит категорию для создания цели """
        category = GoalCategory.objects.filter(
            title__exact=msg.text,
            board__participants__user=tg_user.user,
            is_deleted=False
        ).first()
        if category:
            self.state = self.State.title_goal_input
            self.storage_for_create['category'] = category
            self.response['message'] = (f'вы выбрали {category.title} категорию\n'
                                        f'введите название цели')
        else:
            self.response['message'] = 'такой категории нет, выберите из имеющихся'
            self.response['message'] += self.category(msg, tg_user)['message']
        return self.response

    def start_create_goal(self, msg: Message, tg_user: TgUser) -> dict[str, str]:
        """ Выводит список категорий для создания цели и переключает статус на ввод категории """
        self.response['message'] = (f'выберите в какой категории создать цель:'
                                    f'\n{self.category(msg, tg_user).get("message")}')
        self.state = self.State.category_input
        return self.response

    def category(self, msg: Message, tg_user: TgUser) -> dict[str, str]:
        """ Проверяет наличие и название категорий и выводит список категорий в тг чате """
        category = GoalCategory.objects.filter(
            board__participants__user=tg_user.user,
            is_deleted=False
        )
        if category.count() > 0:
            cat_for_msg = [f"# {item.id} [{item.title}]" for item in category]
            self.response['message'] = 'ваши категории:\n' + '\n'.join(cat_for_msg)
        else:
            self.response['message'] = 'список категорий пуст'
        return self.response

    def cancel(self) -> dict[str, str]:
        """ Отмена создания цели(устанавливает статус бездействия) """
        self.storage_for_create = {}
        self.response['message'] = 'операция отменена'
        self.state = self.State.idle
        return self.response

    def title_goal_input(self, msg: Message, tg_user: TgUser) -> dict[str, str]:
        """ Получает название цели и создаёт её """
        category = self.storage_for_create['category']
        goal = Goal.objects.create(
            user=tg_user.user,
            title=msg.text,
            category=category
        )
        if goal:
            self.response['message'] = 'цель создана'
            self.state = self.State.idle
        return self.response
