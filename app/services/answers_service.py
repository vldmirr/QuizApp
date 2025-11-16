from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional

from app.models.models import Answer
from app.models.schemas import AnswerCreate

def get_answers_by_question(db: Session, question_id: int, skip: int = 0, limit: int = 100) -> List[Answer]:
    return db.query(Answer).filter(Answer.question_id == question_id).order_by(desc(Answer.created_at)).offset(skip).limit(limit).all()

def get_answer(db: Session, answer_id: int) -> Optional[Answer]:
    return db.query(Answer).filter(Answer.id == answer_id).first()

def create_answer(db: Session, answer: AnswerCreate, question_id: int) -> Answer:
    db_answer = Answer(
        text=answer.text,
        user_id=answer.user_id,
        question_id=question_id
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer

def delete_answer(db: Session, answer_id: int) -> bool:
    answer = db.query(Answer).filter(Answer.id == answer_id).first()
    if answer:
        db.delete(answer)
        db.commit()
        return True
    return False