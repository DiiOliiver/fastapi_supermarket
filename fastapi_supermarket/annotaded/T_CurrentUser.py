from typing import Annotated

from fastapi import Depends

from fastapi_supermarket.core.security import get_current_user
from fastapi_supermarket.models import User

T_CurrentUser = Annotated[User, Depends(get_current_user())]
