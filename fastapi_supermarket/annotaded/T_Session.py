from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from fastapi_supermarket.core.database import get_session

T_Session = Annotated[Session, Depends(get_session)]
