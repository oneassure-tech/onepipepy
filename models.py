class PDModel(object):
    _keys = None

    def __init__(self, **kwargs):
        self._keys = set()
        for k, v in kwargs.items():
            setattr(self, k, v)
            self._keys.add(k)
        """if "custom_field" in kwargs.keys() and len(kwargs["custom_field"]) > 0:
            custom_fields = kwargs.pop("custom_field")
            kwargs.update(custom_fields)
        for k, v in kwargs.items():
            if hasattr(Ticket, k):
                k = '_' + k
            setattr(self, k, v)
            self._keys.add(k)
        self.created_at = self._to_timestamp(self.created_at)
        self.updated_at = self._to_timestamp(self.updated_at)"""

    """def _to_timestamp(self, timestamp_str):
        Converts a timestamp string as returned by the API to
        a native datetime object and return it.
        return dateutil.parser.parse(timestamp_str)"""


class Deal(PDModel):
    def __str__(self):
        return self.title

    def __repr__(self):
        return '<DealTitle: \'{}\', DealID: \'{}\'>'.format(self.title, self.id)


class Person(PDModel):
    def __str__(self):
        return self.name

    def __repr__(self):
        return '<PersonName: \'{}\', PersonID: \'{}\'>'.format(self.name, self.id)


class Activites(PDModel):
    def __str__(self):
        return self.subject

    def __repr__(self):
        return '<Activity Subject: \'{}\', DealID: \'{}\'>'.format(self.subject, self.deal_id)


class Search(PDModel):
    def __str__(self):
        return "Search Result Object"

    def __repr__(self):
        return "Search Result Object"

    def get_item(self, *args):
        for i in self.data["items"]:
            if i["item"].get("type") in args[0]:
                return globals()[i["item"]["type"].capitalize()](**i["item"])
