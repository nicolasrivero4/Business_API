from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.users import User
from app.core.security import verify_password, create_access_token
from app.core.logger import logger

class LoginService:
    def login(self, db: Session, user):

        statement = select(User).where(User.email == user.email)

        result = db.execute(statement)

        user_db = result.scalar_one_or_none()

        if not user_db:
            raise HTTPException(
                status_code=401,
                detail="Credenciales invalidas"
            )

        if not verify_password(user.password, user_db.password_hash):
            raise HTTPException(
                status_code=401,
                detail="Credenciales invalidas"
            )

        logger.info("Inicio de sesion. Email: %s", user.email)
        
        access_token = create_access_token(
            user_id=user_db.id,
            role=user_db.role.value
        )

        return {
            "Token": access_token,
            "Token_type": "bearer"
        }