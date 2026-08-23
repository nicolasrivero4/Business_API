from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.users import User
from app.schemas.users import UserCreateAdmin
from app.core.security import hash_password
from app.core.logger import logger

class UserService:

    def user_create(self, db:Session, user):
        try:
            if isinstance(user, UserCreateAdmin):
                role = user.role

            else:
                role = "EMPLOYEE"

            new_user = User(
                name = user.name,
                email = user.email,
                password_hash = hash_password(user.password),
                role = role
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
    
        user = result.scalar_one_or_none()

        if not user:

            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )
                
        return user

    def users_get(self, db:Session):
        statement = select(User)
        result = db.execute(statement)

        users = result.scalars().all()

        if not users:

            raise HTTPException(
                status_code=404,
                detail="No hay usuarios"
            )

        return users

    def user_update(self, db: Session, user, user_id):
        statement = select(User).where(User.id == user_id)
        result = db.execute(statement)

        user_upd = result.scalar_one_or_none()

        if not user_upd:
        
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )
        
        try:
            user_upd.name = user.name
            user_upd.email = user.email

            db.commit()
            db.refresh(user_upd)

            logger.info("Se actualizaron los datos del usuario. ID: %s", user_upd.id)
            
            return user_upd

        except IntegrityError:
            db.rollback()

            logger.warning("Se intentó actualizar el usuario %s con un email repetido. Email: %s", user_id, user.email)

            raise HTTPException(
                status_code=400,
                detail="El email ya está registrado"
            )

    def user_delete(self, db: Session, user_id):
        statement = select(User).where(User.id == user_id)
        result = db.execute(statement)

        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        db.delete(user)
        db.commit()

        logger.info("Se elimino un usuario. ID: %s", user_id)
    