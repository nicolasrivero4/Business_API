from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.users import User
from app.core.logger import logger

class UserService:

    def user_create(self, db:Session, user):
        try:
            new_user = User(
                name = user.name,
                email = user.email,
                password_hash = user.password_hash,
                role = user.role
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            logger.info("Usuario creado correctamente. Email: %s", new_user.email)

            return new_user

        except IntegrityError:
            db.rollback()

            logger.warning("Se intento crear un Usuario con Email invalido o repetido. Email: %s", user.email)

            raise HTTPException(
                status_code=400,
                detail="Usuario o Email invalidos"
            )

    def user_get(self, db: Session, user_id):

        statement = select(User).where(User.id == user_id)
        result = db.execute(statement)
    
        users = result.scalar_one_or_none()

        if not users:

            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )
                
        return users
    