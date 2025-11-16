from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.schemas import QuestionCreate, QuestionResponse, QuestionWithAnswers
from app.service import questions as serviceQ


router = APIRouter(prefix="/questions")

@router.get("/", response_model=List[QuestionResponse])
def get_questions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список всех вопросов"""
    return serviceQ.get_questions(db, skip=skip, limit=limit)

@router.post("/", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    """Создать новый вопрос"""
    return serviceQ.create_question(db=db, question=question)

@router.get("/{question_id}", response_model=QuestionWithAnswers)
def get_question(question_id: int, db: Session = Depends(get_db)):
    """Получить вопрос и все ответы на него"""
    db_question = serviceQ.get_question_with_answers(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    return db_question

@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(question_id: int, db: Session = Depends(get_db)):
    """Удалить вопрос (вместе с ответами)"""
    success = serviceQ.delete_question(db, question_id=question_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    return None