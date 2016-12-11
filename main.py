import os.path
from multiprocessing import Pool
from collections import namedtuple
import pickle
import datetime
import string
import re
from db_connection import *
from utils import *

Triple = namedtuple('Triple', 'resource property value')
NUMBER_OF_FILES = 19


def is_last_file(name):
    return string.ascii_lowercase.index(name[-1]) == NUMBER_OF_FILES - 1

def next_file(name):
    """
    Returns name of the next file
    :param name: str
    :return: str
    """
    return name[:-1]+string.ascii_lowercase[string.ascii_lowercase.index(name[-1])+1]

def process_triple(text):
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
    with open(name, 'r') as f:
        line = ""
        while not line.startswith('<'):
            line = f.readline()
        if not name[-1] == 'a':  # if the file is not first ignore first group
            groupped = groupped_triple(f, process_triple(line))
            line = groupped[1]
        while True:
            groupped = groupped_triple(f, process_triple(line))
            if groupped[1] is None:  # reached end of the file
                # This is a bit clumsy, but it's probably the fastest way
                if is_last_file(name):
                    if triple_predicate(groupped[0]):
                        result.append(groupped[0])
                else:
                    next_file_name = next_file(name)
                    
                break
            else:
                if triple_predicate(groupped[0]):
                    print("Adding %s" % get_name(groupped[0]))
                    result.append(groupped[0])
            line = groupped[1]
    persons = map(get_person, result)
    session = create_session()
    session.add_all(persons)
    session.commit()


def process_files(dirname):
    names = ['infobox' + c for c in string.ascii_lowercase[:NUMBER_OF_FILES]]
    pool = Pool()
    results = pool.map(
        process_file, [
            os.path.join(
                dirname, name) for name in names])


if __name__ == "__main__":
    process_files('/Users/igormelnyk/Documents/TaskForIDT')
