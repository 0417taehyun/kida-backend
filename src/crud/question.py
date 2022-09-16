from enum import Enum

from sqlalchemy.orm import Session

from src.crud.base import CRUDBase
from src.util import convert_datetime_to_string, get_current_datetime
from src.model import Question, QuestionCategory
from src.schema import (
    CreateQuestion,
    CreateQuestionCategory,
    UpdateQuestion,
    UpdateQuestionCategory
)


class CRUDQuestion(CRUDBase[CreateQuestion, UpdateQuestion]):
    def create_category(
        self, db: Session, insert_data: CreateQuestionCategory
    ) -> bool:                
        current_datetime = convert_datetime_to_string(get_current_datetime())
        query: str = f"""
        INSERT INTO question_category (name, created_at)
        VALUES ('{insert_data.name}', '{current_datetime}');
        """
        db.execute(statement=query)
        db.commit()
        return True
    
    
    def create_question(
        self, db: Session, insert_data: CreateQuestion
    ) -> bool:
        current_datetime = convert_datetime_to_string(get_current_datetime())
        query: str = f"""
        INSERT INTO {self.model.__tablename__}
        (question_category_id, content, created_at)
        VALUES (
            {insert_data.question_category_id},
            '{insert_data.content}',
            '{current_datetime}'
        );
        """
        db.execute(statement=query)
        db.commit()
        return True


crud_question = CRUDQuestion(model=Question)
