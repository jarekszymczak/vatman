import re

from bs4 import Comment


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_soup(soup):
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts).strip()


def remove_empty_lines(text):
    if not text:
        return []
    return [line for line in text.split("\n") if line]


def remove_non_numeric_data_from_line(line):
    if not line:
        return ''
    return ''.join([''.join(ch for ch in word if ch.isdigit()) for word in line.split()])


def extract_numbers_from_text(text):
    if not text:
        return set()
    return {x for x in cleanup_and_join_numbers_in_text(text) if re.findall(r'^[0-9]+$', x)}


def cleanup_and_join_numbers_in_text(text):
    if not text:
        return []
    words = [''.join(ch for ch in word if ch.isalnum()) for word in text.replace("\n", ' x ').replace(":", " ").split()
             if word]
    words = [x for x in words if x]
    tmp_list = []
    number_candidates = []
    for x in words:
        if not re.findall(r'^[0-9]+$', x):
            if tmp_list:
                number_candidates.append(''.join(tmp_list))
                tmp_list = []
            number_candidates.append(x)
        else:
            tmp_list.append(x)
    if tmp_list:
        number_candidates.append(''.join(tmp_list))
    return number_candidates
