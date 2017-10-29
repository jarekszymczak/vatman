from etl.interface.common_etl import CommonETL


class InterfaceItemETL(CommonETL):
    def get_item_id(self, object):
        raise NotImplementedError()

    def get_category_id(self, object):
        raise NotImplementedError()

    def get_category_name(self, object):
        raise NotImplementedError()

    def get_category_tree(self, object):
        raise NotImplementedError()

    def get_price(self, object):
        raise NotImplementedError()

    def get_nick(self, object):
        raise NotImplementedError()

    def get_description(self, object):
        raise NotImplementedError()

    def get_title(self, object):
        raise NotImplementedError()

    def get_item_condition(self, object):
        raise NotImplementedError()

    def get_item_invoice(self, object):
        raise NotImplementedError()

    def get_buyers_count(self, object):
        raise NotImplementedError()

    def get_bought_items_count(self, object):
        raise NotImplementedError()

    def get_available_items_count(self, object):
        raise NotImplementedError()
