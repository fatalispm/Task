import os.path
import string
from collections import namedtuple
from multiprocessing import Pool

from db_connection import *
from utils import *

Triple = namedtuple('Triple', 'resource property value')
NUMBER_OF_FILES = 19


def is_last_file(name: str):
    return string.ascii_lowercase.index(name[-1]) == NUMBER_OF_FILES - 1


def next_file(name: str):
    """

    :param name: str
    :return: str
    """
    return name[:-1] + \
           string.ascii_lowercase[string.ascii_lowercase.index(name[-1]) + 1]


def read_head(file, name):
    """
    If the file is not the first we must ignore it's beginning because it can be
    continuation of the previous item
    :param file:
    :param name:
    :return:
    """
    line = ""
    groupped = None
    while not line.startswith('<'):
        line = file.readline()
        if not name[-1] == 'a':  # if the file is not first ignore first group
            groupped = groupped_triple(file, process_triple(line))
            line = groupped[1]
    return line, groupped


def process_list_triple(text: list) -> Triple:
    resource, property, *value = text
    value = " ".join(value)
    return Triple(resource, property, value)


def process_triple(text: str) -> Triple:
    """
    Example of triple:
    <http://dbpedia.org/resource/St._Michael-Sidman,_Pennsylvania>
     <http://dbpedia.org/property/name>
     "St. Michael-Sidman"@en ."
    """
    resource, property, *value = text.split(" ")
    value = " ".join(value)
    return Triple(resource, property, value)


def groupped_triple(file, start):
    """
    Function that collects triples until their resource differs
    :param file: file
    :param start: Triple
    :return: tuple
    """
    result = [start]
    for line in file:
        item = process_triple(line)
        if item.resource == start.resource:
            result.append(item)
        else:
            return result, line
    return result, None


def get_person(groupped):
    birth_date = get_date_of(groupped)
    if birth_date is None:
        birth_date = get_date_of(groupped, 'dateOfBirth')
    name = get_name(groupped)
    return Persons(name=name,
                   birth_date=birth_date,
                   additional_info=groupped,
                   nationality='britain')


def process_file(name):
    """
    Function that processes one file and writes results to the database
    :param name: str
    :return:
    """
    print("Working on %s" % name)
    result = []
    info = []
    with open(name, 'r') as f:
        line, group = read_head(f, name)
        if group:
            info.append(Info(data=group[0], start=True, file_name=name,
                             title=group[0][0].resource))
        while True:
            groupped = groupped_triple(f, process_triple(line))
            if groupped[1] is None:  # reached end of the file
                # This is a bit clumsy, but it's probably the fastest way
                if is_last_file(name):
                    if triple_predicate(groupped[0]):
                        result.append(groupped[0])
                else:
                    info.append(
                        Info(
                            data=groupped[0],
                            start=False,
                            file_name=next_file(name),
                            title=groupped[0][0].resource))
                break
            else:
                if triple_predicate(groupped[0]):
                    print("Adding %s" % get_name(groupped[0]))
                    result.append(groupped[0])
            line = groupped[1]
    persons = map(get_person, result)
    session = create_session()
    session.add_all(persons)
    session.add_all(info)
    session.commit()


def process_files(dirname):
    names = ['infobox' + c for c in string.ascii_lowercase[:NUMBER_OF_FILES]]
    pool = Pool()
    results = pool.map(
        process_file, [
            os.path.join(
                dirname, name) for name in names])


def process_splitted_elements():
    """
    Function that processes elements that were the part of two files
    :return:
    """
    session = create_session()
    info_objects = session.query(Info).all()
    info_objects = sorted(
        info_objects,
        key=lambda x: x.title)  # sort objects by title
    persons = []
    for x, y in chunks(info_objects):
        if x.title == y.title:  # the same objects
            x.data += y.data
            processed = map(process_list_triple, x.data)
            if triple_predicate(processed):
                persons.append(get_person(processed))
        else:
            for i in [x, y]:
                processed = map(process_list_triple, i.data)
                if triple_predicate(processed):
                    persons.append(get_person(processed))
    session.add_all(persons)
    session.commit()


def main():
    process_files('/Users/igormelnyk/Documents/TaskForIDT')
    # There are still left several objects that belong to two files
    process_splitted_elements()


if __name__ == "__main__":
    main()
