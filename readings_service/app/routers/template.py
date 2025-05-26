from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db_vitals import get_async_session
from app.db.crud.template import get_all_templates_by_category, get_template_by_id
from app.schemas.template import TemplateCategory, TemplateShort, TemplateDetailResponse, CardQuestionResponse

router = APIRouter(tags=["Templates"])

@router.get("/get_templates", response_model=List[TemplateCategory])
async def get_templates(db: AsyncSession = Depends(get_async_session)):
    """Получение всех шаблонов, сгруппированных по категориям"""
    templates_by_category = await get_all_templates_by_category(db)
    
    return [
        TemplateCategory(
            category_name=category,
            templates=[
                TemplateShort(
                    template_id=template.id,
                    template_name=template.name
                ) for template in templates
            ]
        ) for category, templates in templates_by_category.items()
    ]

@router.get("/get_template_by_id/{template_id}", response_model=TemplateDetailResponse)
async def get_template(template_id: int, db: AsyncSession = Depends(get_async_session)):
    """Получение шаблона по ID со списком вопросов"""
    template = await get_template_by_id(db, template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    return TemplateDetailResponse(
        id=template.id,
        name=template.name,
        category=template.category,
        card_questions=[
            CardQuestionResponse(
                id=q.id,
                num=q.num,
                question=q.question
            ) for q in sorted(template.questions, key=lambda x: x.num)
        ]
    ) 