from typing import Union

from utils import get_session

from ..models import EpicContract


def create_contract(
    client_id: int,
    total_amount: float,
    amount_due: float,
    status: str,
    commercial_contact: int,
) -> EpicContract:
    _, session = get_session()
    new_contract = EpicContract(
        client_id=client_id,
        total_amount=total_amount,
        amount_due=amount_due,
        status=status,
        commercial_contact=commercial_contact,
    )
    session.add(new_contract)
    session.commit()
    return new_contract


def get_all_contracts() -> Union[list[EpicContract], None]:
    _, session = get_session()
    contracts = EpicContract.get_all_contracts(session)
    if contracts:
        return contracts
    return None


def get_contract_by_staff_id(staff_id: int) -> Union[list[EpicContract], None]:
    _, session = get_session()
    contract: EpicContract = EpicContract.get_contract_by_staff_id(session, staff_id)
    if contract:
        return contract
    return None


def get_contract_by_user_id(user_id: int) -> Union[list[EpicContract], None]:
    _, session = get_session()
    contract: EpicContract = EpicContract.get_contract_by_client_id(
        session, client_id=user_id
    )
    if contract:
        return contract
    return None


def get_contract_with_due_amount() -> Union[list[EpicContract], None]:
    _, session = get_session()
    contract: EpicContract = EpicContract.get_contract_with_due_amount(session)
    if contract:
        return contract
    return None


def is_contract_exists(contract_id: int) -> Union[list[EpicContract], None]:
    _, session = get_session()
    contract: EpicContract = EpicContract.get_contract_by_id(session, contract_id)
    if contract:
        return contract
    return None


def is_staff_contract_commercial_contact(staff_id: int, contract_id: int) -> bool:
    """
    Verifies if the staff is the commercial contact of the contract.
    """
    contract: EpicContract = is_contract_exists(contract_id)
    if contract and staff_id == contract.commercial_contact:
        return True
    return False
