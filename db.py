from sqlalchemy import create_engine, Integer, String, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('sqlite:///warefly.db')
db_session = scoped_session(sessionmaker(bind=engine,
                                         autocommit=False,
                                         autoflush=False))
Base = declarative_base()
Base.query = db_session.query_property()


def validate_int(value, name=''):
    try:
        return int(value)
    except:
        raise ValueError('{} should be int'.format(name))


def validate_string(value):
    if not isinstance(value, str):
        raise ValueError('value is not a str instance')
    return value


validators = {
    Integer: validate_int,
    String: validate_string
}


@event.listens_for(Base, 'attribute_instrument')
def configure_listener(class_, key, inst):
    if not hasattr(inst.property, 'columns'):
        return

    # this event is called whenever a "set"
    # occurs on that instrumented attribute
    @event.listens_for(inst, "set", retval=True)
    def set_(instance, value, oldvalue, initiator):
        validator = validators.get(inst.property.columns[0].type.__class__)
        if validator:
            return validator(value)
        else:
            return value
