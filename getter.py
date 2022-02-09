import requests

from constants import (
    API_ASSAYS,
    API_COMPOUNDS,
    API_SINGLE_ASSAY,
    API_SINGLE_COMPOUND,
)


def get_compounds() -> dict:
    """
    Poll the API for all compound data; return as a dict

    Returns:
        dict: a dictionary representation of the json data
    """
    r = requests.get(API_COMPOUNDS)
    return r.json()


def get_compound(compound_id: int) -> dict:
    """
    Poll the API for the data of one compound, specified by compound_id; return
    as a dict

    Args:
        compound_id (int): the compound_id e.g. 27648

    Returns:
        dict: a dictionary representation of the json data
    """
    r = requests.get(API_SINGLE_COMPOUND.format(compound_id))
    return r.json()


def get_assays() -> dict:
    """
    Poll the API for all assay data; return as a dict

    Returns:
        dict: a dictionary representation of the json data
    """
    r = requests.get(API_ASSAYS)
    return r.json()


def get_assay(result_id: int) -> dict:
    """
    Poll the API for the data of one assay, specified by result_id; return as a
    dict

    Args:
        result_id (int): the result_id e.g. 6364731

    Returns:
        dict: a dictionary representation of the json data
    """
    r = requests.get(API_SINGLE_ASSAY.format(result_id))
    return r.json()
