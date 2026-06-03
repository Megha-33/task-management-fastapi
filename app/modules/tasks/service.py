from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.models.user import User

from app.modules.tasks.schema import (
    TaskCreateSchema,
    TaskUpdateSchema
)

from uuid import UUID

from sqlalchemy import select

from fastapi import (
    HTTPException,
    status
)

class TaskService:

    @staticmethod
    async def create_task(
        task_data: TaskCreateSchema,
        current_user: User,
        db: AsyncSession
    ) -> Task:

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            due_date=task_data.due_date,
            user_id=current_user.id
        )

        db.add(task)

        await db.commit()

        await db.refresh(task)

        return task
    
    
    @staticmethod
    async def get_user_task(
        task_id: UUID,
        current_user: User,
        db: AsyncSession
    ) -> Task:

        result = await db.execute(
            select(Task).where(
                Task.id == task_id,
                Task.user_id == current_user.id
            )
        )

        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        return task
    
    
    @staticmethod
    async def get_tasks(
        current_user: User,
        db: AsyncSession
    ):

        result = await db.execute(
            select(Task).where(
                Task.user_id == current_user.id
            )
        )

        return result.scalars().all()
    
    
    @staticmethod
    async def get_task(
        task_id: UUID,
        current_user: User,
        db: AsyncSession
    ):

        return await TaskService.get_user_task(
            task_id=task_id,
            current_user=current_user,
            db=db
        )
        
        
    @staticmethod
    async def update_task(
        task_id: UUID,
        task_data: TaskUpdateSchema,
        current_user: User,
        db: AsyncSession
    ):

        task = await TaskService.get_user_task(
            task_id,
            current_user,
            db
        )

        update_data = task_data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(
                task,
                field,
                value
            )

        await db.commit()

        await db.refresh(task)

        return task
    
    
    @staticmethod
    async def delete_task(
        task_id: UUID,
        current_user: User,
        db: AsyncSession
    ):

        task = await TaskService.get_user_task(
            task_id,
            current_user,
            db
        )

        await db.delete(task)

        await db.commit()

        return {
            "message": "Task deleted successfully"
        }