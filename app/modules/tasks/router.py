from fastapi import (
    APIRouter,
    Depends,
    status
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.models.user import User

from app.core.dependencies import (
    get_current_user
)

from app.modules.tasks.schema import (
    TaskCreateSchema,
    TaskResponseSchema,
    TaskUpdateSchema
)

from app.modules.tasks.service import (
    TaskService
)

from uuid import UUID

from fastapi import Query

from app.modules.tasks.query_schema import (
    TaskQueryParams
)

from app.models.task import (
    TaskStatus,
    TaskPriority
)

from app.modules.tasks.response_schema import (
    PaginatedTaskResponse
)

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post(
    "",
    response_model=TaskResponseSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_task(
    task_data: TaskCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    return await TaskService.create_task(
        task_data=task_data,
        current_user=current_user,
        db=db
    )
    
    
@router.get(
    "",
    response_model=PaginatedTaskResponse
)
async def get_tasks(
    page: int = Query(
        1,
        ge=1
    ),
    size: int = Query(
        10,
        ge=1,
        le=100
    ),
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    search: str | None = None,
    sort_by: str = "created_at",
    order: str = "desc",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    params = TaskQueryParams(
        page=page,
        size=size,
        status=status,
        priority=priority,
        search=search,
        sort_by=sort_by,
        order=order
    )

    return await TaskService.get_tasks(
        current_user=current_user,
        db=db,
        params=params
    )
    
    
@router.get(
    "/{task_id}",
    response_model=TaskResponseSchema
)
async def get_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    return await TaskService.get_task(
        task_id=task_id,
        current_user=current_user,
        db=db
    )
    
    
@router.put(
    "/{task_id}",
    response_model=TaskResponseSchema
)
async def update_task(
    task_id: UUID,
    task_data: TaskUpdateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    return await TaskService.update_task(
        task_id=task_id,
        task_data=task_data,
        current_user=current_user,
        db=db
    )
    
    
@router.delete("/{task_id}")
async def delete_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    return await TaskService.delete_task(
        task_id=task_id,
        current_user=current_user,
        db=db
    )