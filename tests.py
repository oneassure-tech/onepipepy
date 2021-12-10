import unittest
from api import *
from models import *
from datetime import datetime


class PDTest(unittest.TestCase):
    api = API(Config.PD_API_KEY)
    vars = dict()

    def test_search_person(self):
        self.assertIsInstance(
            self.api.search.search_items(
                term="Shreyans",
                item_types="person"
            ),
            Person
        )

    def test_search_deal(self):
        self.assertIsInstance(
            self.api.search.search_items(
                term="Shreyans",
                item_types="deal"
            ),
            Deal
        )

    def add_deal(self):
        deal = self.api.deal.add_deal(
            title="Shreyans - 9686421633"
        )
        self.vars["deal_id"] = deal.data["id"]
        self.assertIsInstance(
            deal,
            Deal
        )

    def update_deal(self):
        self.assertIsInstance(
            self.api.deal.update_deal(
                id=self.vars["deal_id"],
                data=dict(
                    title="Shreyans - new -deal"
                )
            ),
            Deal
        )

    def get_deal_by_id(self):
        self.assertIsInstance(
            self.api.deal.get_deal_by_id(
                id=self.vars["deal_id"]
            ),
            Deal
        )

    def add_activity_to_deal(self):
        self.assertIsInstance(
            self.api.activity.add_activity(
                deal_id=self.vars["deal_id"],
                data=dict(
                    subject="Test activity",
                    due_data=datetime.today().strftime('%Y-%m-%d'),
                    due_time=""
                )
            ),
            Activites
        )

    def test_deals(self):
        self.add_deal()
        self.update_deal()
        self.get_deal_by_id()
        self.add_activity_to_deal()


if __name__ == "__main__":
    unittest.main()

