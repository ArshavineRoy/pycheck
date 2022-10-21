import re
import sys


def abbreviation_to_raw(abbrev: str) -> str:
    return r'\.'.join(abbrev.split("."))


titles = tuple(map(abbreviation_to_raw, (
    "Mr.",
    "MR.",
    "a.m.",
    "p.m.",
    "Dr.",
    "v.",
    "Ms.",
    "MS.",
    "Mrs.",
    "MRS.",
    "Jr.",
    "JR.",
    "U.S.",
)))


substitutes_dict = {
    'cuz': 'because',
    'alright': 'all right',
    'video conference': 'videoconference',
    'Video conference': 'Videoconference'
}


parenthetical = (
    'Defendant',
    'Plaintiff',
    'Off the record',
    'The reporter read back',
    'The record was replayed',
    'Videoconference connection',
    'Witness sworn'
)

def substitute_qa(text: str) -> str:
    return re.sub(r"(\n([QA])\. )|(\n([QA]):\n)", r"\n\g<2>\g<4>.\t", text)


def substitute_colloquy(text: str) -> str:
    return re.sub(r"(?<!testified as follows)(:\n|: )(?=[^Q][^.])", r":  ", text)


def substitute_by_line_colon(text: str) -> str:
    return re.sub(r"(?<=\n)(by|BY.+)\n", r"\g<1>:\n", text)


def substitute_punctuation_one_space(text: str) -> str:
    return re.sub(r"([?.]\"?) ", r"\g<1>  ", text)


def substitute_title_abbreviations(text: str) -> str:
    t = r"|".join(titles)
    return re.sub(fr'\b({t})  ', r'\g<1> ', text)


def substitute_strike_that(text: str) -> str:
    return re.sub(r"([sS]trike that.*\n)", r"\g<1>\t\t", text)


def substitute_double_colon(text: str) -> str:
    return text.replace("::", ":")


def format_tabs(text: str) -> str:
    text = re.sub(r"\n([QA].)", r"\n\t\g<1>", text)
    text = re.sub(r"\n?(.+:  )", r"\n\t\t\g<1>", text).lstrip('\n')
    return text


def format_parentheticals(text: str) -> str:
    t = r"|".join(parenthetical)
    return re.sub(fr'\(({t})', r'\t\t(\g<1>', text)


def substitute_new_speaker(text: str):
    return text.replace("New Speaker:\n", "")


def substitute_words(text: str) -> str:
    for old, new in substitutes_dict.items():
        text = re.sub(fr'\b{old}\b', fr'{new}', text)
    return text


def perform_checks(file_name, mutators) -> str:
    with open(file_name, 'r') as f:
        text = f.read()

    for mutator in mutators:
        text = mutator(text)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide a file")
        exit(1)

    file = sys.argv[1]

    reformatters = (
        substitute_qa,
        substitute_colloquy,
        substitute_by_line_colon,
        substitute_punctuation_one_space,
        substitute_title_abbreviations,
        substitute_strike_that,
        substitute_double_colon,
        format_tabs,
        format_parentheticals,
        substitute_new_speaker,
        substitute_words,
    )
    
    perform_checks(file, reformatters)
