from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.utils.config import get_config


engine = create_engine(get_config('DATABASE_URL'), echo=True)
Session = sessionmaker(bind=engine)


@contextmanager
def create_context(context=None):
    '''
    Create a new context to use database
    If 'context' arg are given, a sub transaction are create.
    useful for nested operations with transactions.
    '''
    try:
        if not context:
            session = Session()
        else:
            session = context['session']
            session.begin(subtransactions=True)

        yield {
            'session': session
        }

        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
