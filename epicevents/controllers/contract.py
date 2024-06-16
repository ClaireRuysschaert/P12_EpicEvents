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


def get_all_contracts() -> list[EpicContract]:
    _, session = get_session()
    all_contracts = EpicContract.get_all_contracts(session)
    return all_contracts


def is_contract_exists(contract_id: int) -> EpicContract:
    _, session = get_session()
    contract: EpicContract = EpicContract.get_contract_by_id(session, contract_id)
    if contract:
        return contract
    else:
        return None
