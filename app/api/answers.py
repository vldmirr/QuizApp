from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
#from typing import List

from app.db_connect import get_db
from app.models.schemas import AnswerCreate, AnswerResponse
from app.service import answers as crud_answers
from app.service import questions as crud_questions

router = APIRouter()

@router.post("/questions/{question_id}/answers/", response_model=AnswerResponse, status_code=status.HTTP_201_CREATED)
def create_answer(question_id: int = Path(..., gt=0), answer: AnswerCreate = ...,db: Session = Depends(get_db)):
    """Добавить ответ к вопросу"""
    # Проверяем существование вопроса
    question = crud_questions.get_question(db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Question not found")
    
    return crud_answers.create_answer(db=db, answer=answer, question_id=question_id)

@router.get("/answers/{answer_id}", response_model=AnswerResponse)
def get_answer(answer_id: int, db: Session = Depends(get_db)):
    """Получить конкретный ответ"""
    db_answer = crud_answers.get_answer(db, answer_id=answer_id)
    if db_answer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found"
        )
    return db_answer

@router.delete("/answers/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_answer(answer_id: int, db: Session = Depends(get_db)):
    """Удалить ответ"""
    success = crud_answers.delete_answer(db, answer_id=answer_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found"
        )
    return None