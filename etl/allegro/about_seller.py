import glob
import pathlib
import re
from commons.utils import (remove_empty_lines, cleanup_and_join_numbers_in_text, extract_numbers_from_text)
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

contact_data_selector = "#sellerUserData > div > div.col-ss-12.col-sm-9.col-md-10 > div"
phone_number_selector = "#sellerInfoContactInfo > div > div.seller-info-data.col-ss-6.col-sm-4.col-md-5"
email_selector = "#sellerInfoContactInfo > div > div.seller-info-data.col-ss-6.col-sm-4.col-md-5"
username_selector = "div.main-title-breadcrumbs.clearfix > div > h1 > span > span.uname"
all_fields_id = "showItemSellerInfo"

def get_nip(contact_data_field):
    if not contact_data_field or not contact_data_field.text:
        return None
    words = cleanup_and_join_numbers_in_text(contact_data_field.text)
    nip_candidates = {x for x in words if re.findall(r'^[0-9]+$', x)}
    if not nip_candidates:
        return None
    if len(nip_candidates) == 1:
        return nip_candidates[0]
    for idx, word in enumerate(words):
        if idx > 0 and word in nip_candidates and "nip" == words[idx-1].lower():
            return word
    return None

def get_phone_numbers(phone_number_field):
    if not phone_number_field:
        return set()
    phone_numbers = set()
    for number in remove_empty_lines(phone_number_field.text):
        if number and len(number) >= 9 and len(number) <= 11:
            phone_numbers.update(extract_numbers_from_text(number))
    return phone_numbers

def get_emails(email_field):
    if not email_field:
        return set()
    emails = set()
    for word in email_field.text.split():
        if "@" in word:
            while not word[-1].isalnum():
                word = word[:-1]
            emails.add(word.strip())
    return emails

def get_username(username_field):
    if not username_field:
        return None
    return username_field.text.strip()

def get_other_candidate_numbers(all_fields):
    if not all_fields or not all_fields.text:
        return set(), None
    words = cleanup_and_join_numbers_in_text(all_fields.text)
    nums = {x for x in words if re.findall(r'^[0-9]+$', x)}
    if not nums:
        return set(), None
    nip_candidates = [num for num in nums if len(num) == 10]
    potential_nip = None
    if not nip_candidates:
        potential_nip = None
    if len(nip_candidates) == 1:
        potential_nip = nip_candidates[0].strip()
    for idx, word in enumerate(words):
        if idx > 0 and word in nip_candidates and "nip" == words[idx-1].lower():
            potential_nip = word.strip()
    return ({num.strip() for num in nums if num and (len(num) == 9 or len(num) == 11)}, potential_nip)

def get_other_candidate_emails(all_fields):
    if not all_fields or not all_fields.text:
        return set()
    emails = set()
    for word in all_fields.text.split():
        if "@" in word:
            while word and not word[-1].isalnum():
                word = word[:-1]
            emails.add(word.strip())
    return emails

def extract_data_from_seller(file_path):
    with open(file_path, 'r') as myfile:
        print("Processing file: {}".format(file_path))
        data = myfile.read()

    soup = BeautifulSoup(data, 'html.parser')

    contact_data_field = soup.select_one(contact_data_selector)
    phone_number_field = soup.select_one(phone_number_selector)
    email_field = soup.select_one(email_selector)
    username_field = soup.select_one(username_selector)
    all_fields = soup.find(id=all_fields_id)

    nip = get_nip(contact_data_field)
    phone_numbers = get_phone_numbers(phone_number_field)
    username = get_username(username_field)
    emails = get_emails(email_field)
    (other_candidate_phone_numbers, alternative_nip) = get_other_candidate_numbers(all_fields)
    other_candidate_emails = get_other_candidate_emails(all_fields)

    user_id = str(file_path).split('/')[-1]

    return {
        "user_id":user_id,
        "nip": nip or alternative_nip,
        "phone_numbers": tuple(phone_numbers),
        "username": username,
        "emails": tuple(emails),
        "more_phones": tuple(other_candidate_phone_numbers),
        "more_emails": tuple(other_candidate_emails),
    }


pattern = str(pathlib.Path(__file__).absolute().parent.parent.parent / 'examples' / 'vatman' / 'users' / '*')
parsed_users = [extract_data_from_seller(file_path) for file_path in tqdm(glob.glob(pattern))]
df = pd.io.json.json_normalize(parsed_users)
a = df