"""
There's really no good way to test this project without actually running it
on hardware (RFID reader and label printer). However, we can test the RFID
lookup function against known RFID values.
"""
from unittest import TestCase
from nametags.rfid import lookup_rfid


class TestRfidLookup(TestCase):
    def test_first_name(self):
        # ID: 94877866
        first_name = lookup_rfid("1111111111")
        self.assertEqual(first_name, "testy")

    def test_preferred_name(self):
        # ID: 86867117
        preferred_name = lookup_rfid("2222222222")
        self.assertEqual(preferred_name, "nickname")
