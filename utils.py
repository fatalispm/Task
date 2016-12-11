import datetime

import re

NATIONALITIES = ['britain', 'british']


def check_date(groupped_triple):
    birth_date_string = get_date_of(groupped_triple)
    if not birth_date_string:
        return False
    birth_date = datetime.datetime.strptime(birth_date_string, "%Y-%m-%d")
    return (datetime.datetime.now() - birth_date).days / 365.25 <= 50


def check_nationality(groupped_triple):
    for item in groupped_triple:
        if 'nationality' in item.property:
            for nationality in NATIONALITIES:
                if nationality in item.value.lower():
                    return True
    else:
        return False


def triple_predicate(group_triple):
    return check_nationality(group_triple) and check_date(group_triple)


def get_date_of(group_triple: list, parameter='birthDate'):
    """
    :param group_triple: list of Triple
    :return: str|None
    """

    date_pattern = re.compile(r"\d\d\d\d-\d\d-\d\d")

    try:
        date_value = next(
            filter(
                lambda x: x.property.count(parameter),
                group_triple)).value
        return re.search(date_pattern, date_value).group(0)
    except (StopIteration, AttributeError):
        pass


def get_name(group_triple: list):
    """
    :param group_triple: list of Triple
    :return: str|None
    """
    try:
        name = next(
            filter(
                lambda x: x.property.count('name'),
                group_triple)).value
        name_regexp = r'"(.*?)"'
        return re.search(name_regexp, name).group(1)

    except (StopIteration, AttributeError):
        pass


def chunks(l):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), 2):
        yield l[i:i + 2]
