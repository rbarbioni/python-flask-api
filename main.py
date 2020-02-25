from sentry_sdk import init as sentry_init
from app.dao.schema import Base
from app.dao.context import engine
from app import app as api
from app.utils.logger import get_logger
from app.utils.config import get_config


SENTRY_DSN = get_config('SENTRY_DSN')
log = get_logger(__name__)


if __name__ == '__main__':
    log.info('Starting py-api')

    if SENTRY_DSN:
        sentry_init(SENTRY_DSN)

    if get_config('DATABASE_MIGRATION', False, cast='@bool'):
        Base.metadata.create_all(engine)

    api.run(host='0.0.0.0', port=5000, debug=get_config('DEBUG', default=False))
