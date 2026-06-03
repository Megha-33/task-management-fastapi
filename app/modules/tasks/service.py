from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.models.user import User

from app.modules.tasks.schema import (
    TaskCreateSchema,
    TaskUpdateSchema
)

from uuid import UUID

from sqlalchemy import select, func

from fastapi import (
    HTTPException,
    status
)

from sqlalchemy import (
    select,
    or_,
    asc,
    desc
)

from app.modules.tasks.query_schema import (
    TaskQueryParams
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
        db: AsyncSession,
        params: TaskQueryParams
    ):

        base_query = select(Task).where(
            Task.user_id == current_user.id
        )

        # ------------------
        # Filtering
        # ------------------

        if params.status:
            base_query = base_query.where(
                Task.status == params.status
            )

        if params.priority:
            base_query = base_query.where(
                Task.priority == params.priority
            )

        # ------------------
        # Search
        # ------------------

        if params.search:

            base_query = base_query.where(
                or_(
                    Task.title.ilike(
                        f"%{params.search}%"
                    ),
                    Task.description.ilike(
                        f"%{params.search}%"
                    )
                )
            )

        # ------------------
        # Count Query
        # ------------------

        count_query = select(
            func.count()
        ).select_from(
            base_query.subquery()
        )

        total = await db.scalar(
            count_query
        )

        # ------------------
        # Sorting
        # ------------------

        allowed_sort_fields = {
            "created_at": Task.created_at,
            "updated_at": Task.updated_at,
            "due_date": Task.due_date,
            "title": Task.title,
            "priority": Task.priority,
            "status": Task.status
        }

        sort_column = allowed_sort_fields.get(
            params.sort_by,
            Task.created_at
        )

        if params.order.lower() == "asc":
            base_query = base_query.order_by(
                asc(sort_column)
            )
        else:
            base_query = base_query.order_by(
                desc(sort_column)
            )

        # ------------------
        # Pagination
        # ------------------

        offset = (
            params.page - 1
        ) * params.size

        query = (
            base_query
            .offset(offset)
            .limit(params.size)
        )

        result = await db.execute(
            query
        )

        tasks = result.scalars().all()

        pages = (
            (total + params.size - 1)
            // params.size
        )

        return {
            "items": tasks,
            "total": total,
            "page": params.page,
            "size": params.size,
            "pages": pages
        }
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