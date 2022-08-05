import re


def check_email(email: str) -> bool:
    regex = '^[a-z0-9]+[\._]?[a-z0-9]@psgitech.ac.in'
    return True if re.search(regex, email) else False


def check_id(id: str) -> bool:
    return len(id) == 12


def check_dob(dob: str) -> bool:
    regex = '^([1-9] |1[0-9]| 2[0-9]|3[0-1])(.|-)([1-9] |1[0-2])(.|-|){19}|{20}[0-9][0-9]$'