# Data-class (model) for conference
from uuid import UUID
from pydantic import BaseModel

class ConferenceRequest(BaseModel):
    name: str
    created_by: UUID

class ConferenceResponse(BaseModel):
    name: str
    room_id: str
    link: str
    active: bool
    users: int
    created_by: str
    # Добавить хэш room_id (SHA256)

    # мне нада код, который получает данные с камеры и микрофона (Python Today)
    # данные разбиваем по фрагментам и передаем на сервер. Потом с сервера передаем в команту конференции, из команты остальным юзерам. придумать как собирать и передавать данные