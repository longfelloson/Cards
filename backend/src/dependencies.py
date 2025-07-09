from typing import Annotated

from fastapi import Depends
from unit_of_work import IUnitOfWork, UnitOfWork

UOWDependency = Annotated[IUnitOfWork, Depends(UnitOfWork)]
