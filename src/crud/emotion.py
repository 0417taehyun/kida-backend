from src.model import Emotion
from src.crud.base import CRUDBase
from src.schema import CreateEmotion, UpdaetEmotion


class CRUDEmotion(CRUDBase[CreateEmotion, UpdaetEmotion]):
    pass


crud_emotion = CRUDEmotion(model=Emotion)
