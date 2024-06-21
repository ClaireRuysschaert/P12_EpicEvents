from sqlalchemy import create_engine, select

from epicevents.models import StaffUser, Department, EpicEvent
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from local_settings import postgresql as settings
from sqlalchemy.orm import Session


def get_engine(user, passwd, host, port, db):
    url = f"postgresql://{user}:{passwd}@{host}:{port}/{db}"
    if not database_exists(url):
        create_database(url)
    engine = create_engine(url, pool_size=50, echo=False)
    return engine


def get_engine_from_settings():
    keys = ["pguser", "pgpasswd", "pghost", "pgport", "pgdb"]
    if not all(key in keys for key in settings.keys()):
        raise Exception("Bad config file")

    return get_engine(
        settings["pguser"],
        settings["pgpasswd"],
        settings["pghost"],
        settings["pgport"],
        settings["pgdb"],
    )


def get_session():
    engine = get_engine_from_settings()
    session = sessionmaker(bind=engine)()
    return engine, session


engine, session = get_session()


# def add_department(session: Session):
#     s = select(StaffUser).where(StaffUser.department == "management")
#     for staff in session.scalars(s):
#         staff.department = "management"
#         session.commit()
#         new_department = Department(name="management", employees=staff.staff_id)
#         session.add(new_department)


# add_department(session)
# init_department(session)

# users = select(StaffUser).where(StaffUser.email == "jojo@jojo.fr")
# for user in session.scalars(users):
#     print(
#         user.first_name, user.last_name, user.department_id, user.password, user.email
#     )
# print(
#     session.query(StaffUser)
#     .filter(StaffUser.email == "jojo@jojo.fr")
#     .first()
#     .first_name
# )
# for user in session.scalars(users):
#     user: StaffUser

#     if user.staff_id == 14 or user.staff_id == 15:
#         user.department_id = 3
#     elif user.staff_id == 16 or user.staff_id == 17 or user.staff_id == 18 or user.staff_id == 19:
#         user.department_id = 2
#     elif user.staff_id == 13:
#         user.department_id = 1

#     session.commit()

# d = select(Department)
# for dep in session.scalars(d):
#     print(dep.id, dep.name, len(dep.employees))


# users = select(StaffUser)
# for user in session.scalars(users):
#     user.department = "support"
# session.commit()

# def init_permissions(session: Session):
#     permissions = [
#         # StaffUser permissions for management
#         Permission(department="management", model="StaffUser", department_name ="management", can_read=True, can_create=True, can_update=True, can_delete=True),

#         # EpicUser permissions for commercial
#         Permission(department="commercial", model="EpicUser", can_read=True, can_create=True, can_update=True),

#         # EpicContract permissions for management and commercial
#         Permission(department="management", model="EpicContract", can_read=True, can_create=True, can_update=True),
#         Permission(department="commercial", model="EpicContract", can_read=True, can_update=True),

#         # EpicEvent permissions for management, commercial, and support
#         Permission(department="management", model="EpicEvent", can_read=True),
#         Permission(department="commercial", model="EpicEvent", can_read=True, can_create=True),
#         Permission(department="support", model="EpicEvent", can_read=True, can_update=True),
#     ]

#     session.bulk_save_objects(permissions)
#     session.commit()

# Call this function after creating your database and tables


# new_staff = StaffUser(
#     first_name="Pam",
#     last_name="Beemsly",
#     department="commercial"
# )
# session.add(new_staff)
# session.commit()

# new_staff = StaffUser(
#     first_name="Karen",
#     last_name="Filippelli",
#     department="commercial"
# )
# session.add(new_staff)
# session.commit()

# new_event = EpicEvent(
#     contract_id=1,
#     start_date="2024-09-05",
#     end_date="2024-09-10",
#     support_contact=33,
#     location="Bordeaux",
#     attendees=688,
#     notes="This is a test event."
# )

# session.add(new_event)
# session.commit()

# users = session.query(EpicUser).order_by(EpicUser.first_name).all()

# for user in users:
#     print(user.first_name, user.last_name, user.email, user.phone, user.company, user.assign_to)

# query = select(EpicUser).where(func.lower(EpicUser.first_name).like('j%'))
# for user in session.scalars(query):
#     print(user.first_name, user.last_name, user.email, user.phone, user.company, user.assign_to)

# statement = (
#     select(EpicUser)
#     .join(StaffUser, EpicUser.assign_to == StaffUser.staff_id)
#     .where(EpicUser.first_name == "John")
#     .order_by(EpicUser.first_name)
# )
# print(session.scalars(statement).first().first_name)

# user_13 = select(EpicUser).where(EpicUser.assign_to == 18)
# for user in session.scalars(user_13):
#     user.assign_to_commercial_staff(session, 13)

# # functiun to print all EpicUser
# all_users = select(EpicUser)
# for user in session.scalars(all_users):
#     print(user.first_name, user.last_name, user.email, user.phone, user.company, user.assign_to)

# #create a table
# Base = declarative_base()
# Base.metadata.create_all(engine, tables=[Department.__table__])

# # Print the names of all tables in the database
# def print_all_tables(engine):
#     # To load metdata and existing database schema
#     metadata = MetaData()
#     metadata.reflect(bind=engine)

#     tables = metadata.tables.keys()

#     print("List of tables:")
#     for table in tables:
#         print(table)

# Print all tables in the in-memory database
# print_all_tables(engine)

# print(EpicUser.get_all_users(session))
# print(StaffUser.get_all_users(session))
# print(EpicContract.get_all_contracts(session))
# print(EpicEvent.get_all_events(session))
# jane = session.execute(select(StaffUser).where(StaffUser.staff_id == 14)).scalar_one()
# session.delete(jane)
# session.commit()
