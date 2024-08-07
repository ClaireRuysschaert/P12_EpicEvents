from datetime import datetime
from typing import Union

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    select,
)
from sqlalchemy.orm import DeclarativeBase, Session, relationship

from utils import get_session


class Base(DeclarativeBase):
    pass


password_hasher = PasswordHasher(salt_len=32)


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    name = Column("name", String, nullable=False, unique=True)
    # management, commercial and support
    employees = relationship("StaffUser", backref="department")


class StaffUser(Base):
    __tablename__ = "staff_user"
    staff_id = Column("staff_id", Integer, primary_key=True)
    first_name = Column("first_name", String)
    last_name = Column("last_name", String)
    email = Column("email", String, nullable=True, unique=True)
    department_id = Column("department_id", Integer, ForeignKey("departments.id"))
    password = Column("password", String)

    def hash_password(self, password: str) -> None:
        """
        Hash the password using the argon2 algorithm.
        """
        self.password = password_hasher.hash(password)

    def verify_password(self, session, email, password: str) -> bool:
        """
        Compare the stored hashed password and the password provided by the user
        when logging in. If not the same, return False.
        """
        staff = self.get_user_by_email(session, email)
        stored_password = staff.password
        try:
            return password_hasher.verify(stored_password, password)
        except VerifyMismatchError:
            return False

    def check_password_needs_rehash(self) -> bool:
        """
        Check if the password needs to be rehashed.
        """
        return password_hasher.check_needs_rehash(self.password)

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> Union["StaffUser", None]:
        """
        Fetch staff user by email and return it. If not found, return None.
        """
        return session.query(StaffUser).filter(StaffUser.email == email).first()

    @staticmethod
    def get_user_by_id(session: Session, staff_id: int) -> Union["StaffUser", None]:
        """
        Fetch a staff user by its id and return it. If not found, return None.
        """
        return session.query(StaffUser).filter(StaffUser.staff_id == staff_id).first()

    @staticmethod
    def get_all_staffusers(session: Session) -> list["StaffUser"]:
        """
        Fetch all staff users from the database.
        """
        all_users = select(StaffUser).order_by(StaffUser.staff_id)
        return session.scalars(all_users)

    def update(staff_id: int, **kwargs) -> None:
        """
        Update the attributes of a staff user with the given staff_id from the database.
        """
        _, session = get_session()
        try:
            staff = StaffUser.get_user_by_id(session, staff_id)
            if not staff:
                print(f"Staff with id {staff_id} does not exist")
            for key, value in kwargs.items():
                setattr(staff, key, value)
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error updating staff user: {e}")
        finally:
            session.close()

    def delete(staff_id: int) -> bool:
        """
        Deletes a staff user with the given staff_id from the database.
        """
        _, session = get_session()
        try:
            staff = StaffUser.get_user_by_id(session, staff_id)
            session.delete(staff)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error deleting staff user: {e}")
            return False


class EpicUser(Base):
    __tablename__ = "epic_user"
    user_id = Column("user_id", Integer, primary_key=True)
    first_name = Column("first_name", String)
    last_name = Column("last_name", String)
    email = Column("email", String, unique=True)
    phone = Column("phone", String)
    company = Column("company", String)
    created_on = Column("created_on", DateTime, default=datetime.now())
    updated_on = Column("updated_on", DateTime, onupdate=datetime.now())
    assign_to = Column("assign_to", Integer, ForeignKey("staff_user.staff_id"))

    @staticmethod
    def get_all_users(session: Session) -> list["EpicUser"]:
        """
        Fetch all client users from the database.
        """
        all_users = select(EpicUser).order_by(EpicUser.user_id)
        return session.scalars(all_users)

    @staticmethod
    def get_epic_user_by_id(session: Session, user_id: int) -> Union["EpicUser", None]:
        """
        Fetch epic user by id and return it. If not found, return None.
        """
        return session.query(EpicUser).filter(EpicUser.user_id == user_id).first()

    def assign_commercial_to_epic_user(client_id: int, commercial_contact: int) -> None:
        """
        Assigns a commercial contact to a client.
        If the client does not have an assigned commercial when creating the contract,
        the newly created commercial contact is used for assignment.
        """
        _, session = get_session()
        user = EpicUser.get_epic_user_by_id(session, client_id)
        user.assign_to = commercial_contact
        session.commit()

    def update(user_id: int, **kwargs) -> None:
        """
        Update the attrs of a user with the given user_id from the database.
        """
        _, session = get_session()
        try:
            user = EpicUser.get_epic_user_by_id(session, user_id)
            if not user:
                print(f"User with id {user_id} does not exist")
            for key, value in kwargs.items():
                setattr(user, key, value)
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error updating user: {e}")
        finally:
            session.close()


class EpicContract(Base):
    __tablename__ = "epic_contract"
    contract_id = Column("contract_id", Integer, primary_key=True)
    client_id = Column(
        "client_info",
        Integer,
        ForeignKey("epic_user.user_id"),
    )
    total_amount = Column("total_amount", Numeric)
    amount_due = Column("amount_due", Numeric)
    created_on = Column("created_on", DateTime, default=datetime.now())
    status = Column(Enum("To sign", "Signed", "Cancelled", name="status_contract"))
    commercial_contact = Column(
        "commercial_contact", Integer, ForeignKey("staff_user.staff_id")
    )

    @staticmethod
    def get_all_contracts(session: Session) -> list["EpicContract"]:
        """
        Fetch all contracts from the database.
        """
        all_contracts = select(EpicContract).order_by(EpicContract.contract_id)
        return session.scalars(all_contracts)

    @staticmethod
    def get_contract_by_id(
        session: Session, contract_id: int
    ) -> Union["EpicContract", None]:
        """
        Fetch contract by id and return it. If not found, return None.
        """
        contract = (
            session.query(EpicContract)
            .filter(EpicContract.contract_id == contract_id)
            .first()
        )
        return contract

    @staticmethod
    def get_contracts_by_client_id(
        session: Session, client_id: int
    ) -> list["EpicContract"]:
        """
        Fetch all contracts by client id from the database.
        """
        contract = (
            session.query(EpicContract)
            .filter(EpicContract.client_id == client_id)
            .all()
        )
        return contract

    @staticmethod
    def get_contracts_with_due_amount(session: Session) -> list["EpicContract"]:
        """
        Fetch all contracts with due amount > 0.
        """
        contracts = (
            session.query(EpicContract).filter(EpicContract.amount_due > 0).all()
        )
        return contracts

    @staticmethod
    def get_contracts_by_staff_id(
        session: Session, staff_id: int
    ) -> list["EpicContract"]:
        """
        Fetch all staff contracts by staff id from the database.
        """
        contract = (
            session.query(EpicContract)
            .filter(EpicContract.commercial_contact == staff_id)
            .all()
        )
        return contract

    def update(contract_id: int, **kwargs) -> None:
        """
        Update the attrs of a contract with the given contract_id from the database.
        If 'client_id' is provided in kwargs, also update the commercial_contact
        of the client.
        """
        _, session = get_session()
        try:
            contract = EpicContract.get_contract_by_id(session, contract_id)
            if not contract:
                print(f"Contract with id {contract_id} does not exist")
            for key, value in kwargs.items():
                setattr(contract, key, value)
                session.commit()

            if "client_id" in kwargs and contract.commercial_contact is None:
                contract.commercial_contact = EpicUser.get_epic_user_by_id(
                    session, kwargs["client_id"]
                ).assign_to
                session.commit()

        except Exception as e:
            session.rollback()
            print(f"Error updating contract user: {e}")
        finally:
            session.close()


class EpicEvent(Base):
    __tablename__ = "epic_event"
    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(
        "contract", Integer, ForeignKey("epic_contract.contract_id"), primary_key=True
    )
    contract = relationship("EpicContract")
    start_date = Column("start_date", DateTime)
    end_date = Column("end_date", DateTime)
    support_contact = Column(
        "support_contact", Integer, ForeignKey("staff_user.staff_id"), primary_key=True
    )
    location = Column("location", String)
    attendees = Column("attendees", Integer)
    notes = Column("notes", String)

    @staticmethod
    def get_event_by_id(session: Session, id: int) -> Union["EpicEvent", None]:
        """
        Get epic event by id.
        """
        event = session.query(EpicEvent).filter(EpicEvent.id == id).first()
        return event

    @staticmethod
    def get_all_events(session: Session) -> list["EpicEvent"]:
        """
        Fetch all events from the database.
        """
        all_events = select(EpicEvent).order_by(EpicEvent.id)
        return session.scalars(all_events)

    @staticmethod
    def get_all_staff_events(session: Session, staff_id: int) -> list["EpicEvent"]:
        """
        Fetch all staff events by staff id from the database.
        """
        all_staff_events = select(EpicEvent).filter(
            EpicEvent.support_contact == staff_id
        )
        return session.scalars(all_staff_events)

    def update(id: int, **kwargs) -> None:
        """
        Update the attrs of an event with the given id from the database.
        """
        _, session = get_session()
        try:
            event = EpicEvent.get_event_by_id(session, id)
            if not event:
                print(f"Event with id {id} does not exist")
            for key, value in kwargs.items():
                setattr(event, key, value)
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error updating event user: {e}")
        finally:
            session.close()
