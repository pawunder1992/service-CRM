from django.test import TestCase

from crm.forms import *


class FormsTests(TestCase):
    def test_client_license_plate_validation(self):
        wrong_license_plates = [
            "ABC12345",
            "aa1234AA",
            "AA123AA",
            "AA12A4AA",
        ]

        for plate in wrong_license_plates:
            form = ClientCreationForm(
                data={
                    "model": "Client",
                    "license_plate": plate,
                    "phone_number": "0961234567",
                    "owner_name": "Test Owner",
                }
            )

            self.assertIn(
                "license_plate", form.errors, f"Plate {plate} should be invalid!"
            )

    def test_client_phone_number_validation(self):
        wrong_numbers = [
            "098732224",
            "09873224658",
        ]

        for number in wrong_numbers:
            form = ClientCreationForm(
                data={
                    "model": "Client",
                    "license_plate": "AA1256LP",
                    "phone_number": number,
                    "owner_name": "Test Owner",
                }
            )

            self.assertIn(
                "phone_number", form.errors, f"Plate {number} should be invalid!"
            )
