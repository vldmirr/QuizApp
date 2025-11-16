from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional

from app.models.models import Question
from app.models.schemas import QuestionCreate

def get_questions(db: Session, skip: int = 0, limit: int = 100) -> List[Question]:
    return db.query(Question).order_by(desc(Question.created_at)).offset(skip).limit(limit).all()

def get_question(db: Session, question_id: int) -> Optional[Question]:
    return db.query(Question).filter(Question.id == question_id).first()

def create_question(db: Session, question: QuestionCreate) -> Question:
    db_question = Question(text=question.text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def delete_question(db: Session, question_id: int) -> bool:
    question = db.query(Question).filter(Question.id == question_id).first()
    if question:
        db.delete(question)
        db.commit()
        return True
    return False

def get_question_with_answers(db: Session, question_id: int) -> Optional[Question]:
    return db.query(Question).filter(Question.id == question_id).first()