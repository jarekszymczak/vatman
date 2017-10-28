from bs4 import BeautifulSoup

contact_data_selector = "#sellerUserData > div > div.col-ss-12.col-sm-9.col-md-10 > div"
phone_number_selector = "#sellerInfoContactInfo > div > div.seller-info-data.col-ss-6.col-sm-4.col-md-5 > " \
                        "section:nth-of-type(1) > div.seller-contact-data.col-xm-10"
email_selector = "#sellerInfoContactInfo > div > div.seller-info-data.col-ss-6.col-sm-4.col-md-5 > " \
                 "section:nth-of-type(2) > div.seller-contact-data.col-xm-10"
username_selector = "div.main-title-breadcrumbs.clearfix > div > h1 > span > span.uname"
all_fields_id = "showItemSellerInfo"


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


def get_nip(contact_data_field):
    nip = None
    contact_data = cleanup_contact_data_field(contact_data_field)
    if contact_data:
        for line in contact_data.split("\n"):
            if "nip" in line.lower():
                nip = remove_non_numeric_data_from_line(line)
                if len(nip) == 10:
                    return nip.strip()
    # look for it among other numbers on page
    return nip.strip() if nip else None


def get_phone_number(phone_number_field):
    phone_number = remove_non_numeric_data_from_line(phone_number_field.text)
    if phone_number and len(phone_number) >= 9 and len(phone_number) <= 11:
        return phone_number.strip()
    # look for it among other numbers on page
    return phone_number.strip() if phone_number else None


def get_username(username_field):
    return username_field.text.strip()


def get_email(email_field):
    return email_field.text.strip()


def find_all_numbers(all_fields):
    potential_numbers = set()
    for all_info_element in all_fields.find_all("div"):
        words = all_info_element.text.split()
        digits = ''.join([''.join(ch for ch in word if ch.isdigit()) for word in words]).strip()
        if digits:
            potential_numbers.add(digits)
    return potential_numbers


def get_other_candidate_numbers(all_fields, remove_list=None):
    other_candidate_numbers = set()
    for number in find_all_numbers(all_fields):
        candidate_number = number
        for to_remove in remove_list:
            candidate_number = candidate_number.replace(to_remove, "").strip() if to_remove else None
        if candidate_number and len(candidate_number) >= 9 and len(candidate_number) <= 11:
            other_candidate_numbers.add(candidate_number)
    return other_candidate_numbers


def extract_data_from(id):
    with open(f'{str(id)}.html', 'r') as myfile:
        data = myfile.read()

    soup = BeautifulSoup(data, 'html.parser')

    contact_data_field = soup.select_one(contact_data_selector)
    phone_number_field = soup.select_one(phone_number_selector)
    email_field = soup.select_one(email_selector)
    username_field = soup.select_one(username_selector)
    all_fields = soup.find(id=all_fields_id)

    nip = get_nip(contact_data_field)
    phone_number = get_phone_number(phone_number_field)
    username = get_username(username_field)
    email = get_email(email_field)
    other_candidate_numbers = get_other_candidate_numbers(all_fields, [phone_number, nip])

    return {
        "id": id,
        "nip": nip,
        "phone_number": phone_number,
        "username": username,
        "email": email,
        "other_candidate_numbers": other_candidate_numbers,
    }
