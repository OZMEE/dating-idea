class AppError(Exception):
    """Базовая бизнес-ошибка приложения"""


class NotFoundError(AppError):
    """Сущность не найдена (404)"""


class ForbiddenError(AppError):
    """Недостаточно прав / нет доступа к ресурсу (403)"""


class BadRequestError(AppError):
    """Некорректное действие или нарушение бизнес-правил (400)"""


class RoomNotFoundError(NotFoundError):
    pass


class RoomAccessDeniedError(ForbiddenError):
    pass


class RoomClosedError(BadRequestError):
    pass


class RoomFullError(BadRequestError):
    pass


class AlreadyRoomMemberError(BadRequestError):
    pass


class ParticipantNotFoundError(NotFoundError):
    pass


class OwnerRemovalError(BadRequestError):
    pass


class OptionNotFoundError(NotFoundError):
    pass


class OptionAccessDeniedError(ForbiddenError):
    pass
