from sqlmodel import SQLModel, Session, create_engine, select
from core.config import get_settings
from core.utils import hash, logger
from models import load_models
from models.user import Admin, User

engine = create_engine(get_settings().database_url, echo=get_settings().debug)


def create_default_admin(settings=None):
    if settings is None:
        settings = get_settings()
    admin_email = settings.admin_email
    hash_password = hash(settings.admin_password)
    with Session(engine) as s:
        user = s.exec(select(User).where(User.name == "Admin")).first()
        if not user:
            user_admin = User(
                name="Admin", email=admin_email, is_active=True, password=hash_password
            )
            s.add(user_admin)
            s.commit()
            s.refresh(user_admin)

            admin = Admin(user_id=user_admin.id)
            s.add(admin)
            s.commit()
            s.refresh(admin)
            logger.info("User Admin created")
        logger.info("User Admin existed")


def create_db_and_tables(db_engine=None):
    if db_engine is None:
        db_engine = engine
    load_models()
    SQLModel.metadata.create_all(db_engine)
    create_default_admin()


def get_session():
    with Session(engine) as s:
        yield s
