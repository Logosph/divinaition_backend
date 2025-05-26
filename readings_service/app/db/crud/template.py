from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List, Dict
from app.db.models.reading import ReadingTemplate, CardQuestion

async def get_all_templates_by_category(db: AsyncSession) -> Dict[str, List[ReadingTemplate]]:
    # Получаем все шаблоны с предзагрузкой вопросов
    result = await db.execute(
        select(ReadingTemplate).order_by(ReadingTemplate.category, ReadingTemplate.name)
    )
    templates = result.scalars().all()
    
    # Группируем шаблоны по категориям
    templates_by_category = {}
    for template in templates:
        if template.category not in templates_by_category:
            templates_by_category[template.category] = []
        templates_by_category[template.category].append(template)
    
    return templates_by_category

async def get_template_by_id(db: AsyncSession, template_id: int):
    # Получаем шаблон с предзагрузкой вопросов
    result = await db.execute(
        select(ReadingTemplate)
        .options(selectinload(ReadingTemplate.questions))
        .where(ReadingTemplate.id == template_id)
    )
    return result.scalar_one_or_none() 