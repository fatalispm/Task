"""
    I spent some time choosing how to detect emoticons.
    First, I though about scrapping list of them from certain sites
    and doing exact match.
    This approach has several drawbacks, though it guarantees that we wont have "false positives"
    as in the case of regexp.
    Another approach is to write some sort of regexp. Though, it's hardly possible to match all cases with regexp
    this approach is more general.
    I also found this answer useful: http://stackoverflow.com/a/20583383/2660970
"""

import re


def get_emoticon_pattern():
    """
    Emoticon usually consists of eyes, nose, beards, mouths
    beard and nose is usually optional
    :return: pattern for emoticon
    """
    eyes, noses, beards, mouths = map(
        re.escape, ["x:;8BX=", r"-~'^", r"{}", r")(/\|DP)("])

    pattern = "[{eyes}][{noses}]?[{beards}]?[{mouths}]|[{mouths}][{eyes}]".format(
        eyes=eyes, noses=noses, beards=beards, mouths=mouths)
    return pattern


def find_emoticons(text):
    """

    :param text: str
    :return: tuple(list, str)
    """

    pattern = get_emoticon_pattern()
    return re.findall(pattern, text)


def find_emoticon_and_words(text):
    """
    Sometimes the order of the words doesn't matter so one can this function
    :param text: str
    :return: list of str
    """
    emoticons = find_emoticons(text)
    for e in emoticons:
        text = text.replace(e, "")
    return re.findall("[\w]+", text, re.UNICODE) + emoticons


def split_into_words(text):
    """
    Function that splits text into the list of worlds and emoticons
    :param text: str
    :return: list of str
    """
    word_emoticon_pattern = get_emoticon_pattern() + "|[\w]+"
    return re.findall(word_emoticon_pattern, text, re.UNICODE)


if __name__ == "__main__":
    text = "Hello world! How (sp?) are you today (;"
    print(split_into_words(text))
    assert (
        split_into_words(text) == [
            'Hello',
            'world',
            'How',
            'sp',
            'are',
            'you',
            'today',
            '(;'])
    assert (split_into_words("Hello world,:-) xD")
            == ['Hello', 'world', ':-)', 'xD'])
