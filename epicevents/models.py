from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
    Column,
    DateTime,
    Enum,
    Numeric,
    Boolean,
    select,
)
from sqlalchemy.orm import DeclarativeBase, Session, relationship
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from functools import wraps
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
        self.password = password_hasher.hash(password)

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> "StaffUser":
        return session.query(StaffUser).filter(StaffUser.email == email).first()
    
    def verify_password(self, session, email, password: str) -> bool:
        staff = self.get_user_by_email(session, email)
        stored_password = staff.password
        try:
            return password_hasher.verify(stored_password, password)
        except VerifyMismatchError:
            return False

    def check_password_needs_rehash(self) -> bool:
        return password_hasher.check_needs_rehash(self.password)

    @staticmethod
    def get_user_by_id(session: Session, staff_id: int) -> "StaffUser":
        return session.query(StaffUser).filter(StaffUser.staff_id == staff_id).first()

    @staticmethod
    def get_all_staffusers(session: Session) -> list["StaffUser"]:
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
    email = Column("email", String)
    phone = Column("phone", String)
    company = Column("company", String)
    created_on = Column("created_on", DateTime, default=datetime.now())
    updated_on = Column("updated_on", DateTime, onupdate=datetime.now())
    assign_to = Column("assign_to", Integer, ForeignKey("staff_user.staff_id"))

    @staticmethod
    # @has_permission("read")
    def get_all_users(session: Session):
        all_users = select(EpicUser)
        for user in session.scalars(all_users):
            print(
                user.first_name,
                user.last_name,
                user.email,
                user.phone,
                user.company,
                user.assign_to,
            )

    # @has_permission("create")
    def assign_to_commercial_staff(self, session: Session, staff_id: int):
        """
        Assign the user to a commercial staff.
        """
        staff = session.query(StaffUser).filter(StaffUser.staff_id == staff_id).first()
        if staff.department == "commercial":
            self.assign_to = staff_id
            session.commit()
        else:
            print("Staff is not commercial")

    # @has_permission("read")
    def get_user_by_staff_id(self, session: Session, staff_id: int):
        """
        Get user by staff id.
        """
        user = session.query(EpicUser).filter(EpicUser.assign_to == staff_id).all()
        return user


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
    status = Column(Enum("To sign", "Signed", "Cancelled", name="status_contract")
    )
    commercial_contact = Column(
        "commercial_contact", Integer, ForeignKey("staff_user.staff_id")
    )

    @staticmethod
    # @has_permission("read")
    def get_all_contracts(session: Session):
        all_contracts = select(EpicContract)
        for contract in session.scalars(all_contracts):
            print(
                contract.contract_id,
                contract.client_id,
                contract.total_amount,
                contract.amount_due,
                contract.status,
            )

    # @has_permission("read")
    def get_contract_by_client_id(self, session: Session, client_id: int):
        """
        Get contract by client id.
        """
        contract = (
            session.query(EpicContract)
            .filter(EpicContract.client_info == client_id)
            .all()
        )
        return contract

    # @has_permission("read")
    def get_client_infos(self, session: Session, client_id: int):
        """
        Get client infos by client id.
        """
        client = session.query(EpicUser).filter(EpicUser.user_id == client_id).first()
        return client


class EpicEvent(Base):
    __tablename__ = "epic_event"
    event_id = Column("event_id", Integer, primary_key=True)
    contract_id = Column(
        "contract", Integer, ForeignKey("epic_contract.contract_id"), primary_key=True
    )
    start_date = Column("start_date", DateTime)
    end_date = Column("end_date", DateTime)
    support_contact = Column(
        "support_contact", Integer, ForeignKey("staff_user.staff_id"), primary_key=True
    )
    location = Column("location", String)
    attendees = Column("attendees", Integer)
    notes = Column("notes", String)

    # @has_permission("read")
    def get_client_name(self, session: Session, contract_id: int):
        """
        Get client name by contract id.
        """
        contract = (
            session.query(EpicContract)
            .filter(EpicContract.contract_id == contract_id)
            .first()
        )
        if contract:
            client_id = contract.client_id
            client = (
                session.query(EpicUser).filter(EpicUser.user_id == client_id).first()
            )
            if client:
                return client.first_name, client.last_name
        return None

    # @has_permission("read")
    def get_client_contact(self, session: Session, contract_id: int):
        """
        Get client contact by contract id.
        """
        contract = (
            session.query(EpicContract)
            .filter(EpicContract.contract_id == contract_id)
            .first()
        )
        if contract:
            client_id = contract.client_id
            client = (
                session.query(EpicUser).filter(EpicUser.user_id == client_id).first()
            )
            if client:
                return client.email, client.phone
        return None

    # @has_permission("read")
    def get_support_contact_name(self, session: Session, event_id: int):
        """
        Get support contact name by event id.
        """
        event = session.query(EpicEvent).filter(EpicEvent.event_id == event_id).first()
        if event:
            support_contact_id = event.support_contact
            support_contact = (
                session.query(StaffUser)
                .filter(StaffUser.staff_id == support_contact_id)
                .first()
            )
            if support_contact:
                return support_contact.first_name, support_contact.last_name
        return None

    # @has_permission("read")
    def get_all_events(self, session: Session):
        """
        Get all events.
        """
        all_events = select(EpicEvent)
        for event in session.scalars(all_events):
            print(
                event.event_id,
                event.contract_id,
                event.start_date,
                event.end_date,
                event.location,
                event.attendees,
                event.notes,
            )
