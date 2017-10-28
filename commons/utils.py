from bs4 import BeautifulSoup, Comment

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
        return None
    return '\n'.join([line for line in text.split("\n") if line])


def cleanup_contact_data_field(contact_data):
    if not contact_data or not contact_data.text:
        return None
    return remove_empty_lines(contact_data.text)


def remove_non_numeric_data_from_line(line):
    if not line:
        return None
    return ''.join([''.join(ch for ch in word if ch.isdigit()) for word in line.split()])
