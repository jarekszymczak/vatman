from etl.interface.common_etl import CommonETL


class InterfaceUserETL(CommonETL):
    def get_nip(self, contact_data_field):
        raise NotImplementedError()

    def get_phone_numbers(self, phone_number_field):
        raise NotImplementedError()

    def get_emails(self, email_field):
        raise NotImplementedError()

    def get_username(self, username_field):
        raise NotImplementedError()

    def get_other_candidate_numbers(self, all_fields):
        raise NotImplementedError()

    def get_other_candidate_emails(self, all_fields):
        raise NotImplementedError()
