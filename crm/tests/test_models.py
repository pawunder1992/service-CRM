from django.test import TestCase
from crm.models import ServiceCategory, Client, Specialty, Worker, Order


class ModelsTest(TestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(name="test", hour_cost=250)
        self.client = Client.objects.create(owner_name="Ivan", license_plate="GH1256KO")
        self.specialty = Specialty.objects.create(name="test")
        self.username = "test"
        self.password = "test123"
        self.first_name = "test"
        self.last_name = "test"

        self.worker = Worker.objects.create_user(
            username=self.username,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
            specialty=self.specialty,
        )
        self.order = Order.objects.create(
            category=self.category,
            client=self.client,
            description="something",
            is_completed=False,
            norm_hours=2,
        )
        self.order.performers.add(self.worker.id)

    def test_order_total_price(self):
        self.assertEqual(self.order.total_price, 500)

    def test_order_get_absolute_url(self):
        self.assertEqual(self.order.get_absolute_url(), "/orders/1/")

    def test_client_get_absolute_url(self):
        self.assertEqual(self.client.get_absolute_url(), "/clients/1/")

    def test_client_str(self):
        self.assertEqual(
            str(self.client), f"{self.client.license_plate} {self.client.owner_name}"
        )

    def test_worker_get_absolute_url(self):
        self.assertEqual(self.worker.get_absolute_url(), "/workers/1/")

    def test_worker_str(self):
        self.assertEqual(
            str(self.worker), f"{self.worker.first_name} {self.worker.last_name}"
        )
        self.assertTrue(self.worker.check_password(self.password))

    def test_worker_active_orders_count(self):
        self.assertEqual(self.worker.active_orders_count(), 1)

    def test_specialty_get_absolute_url(self):
        self.assertEqual(self.specialty.get_absolute_url(), "/specialty/1/")

    def test_specialty_str(self):
        self.assertEqual(str(self.specialty), self.specialty.name)

    # def test_manufacturer_str(self):
    #     self.assertEqual(
    #         str(self.manufacturer),
    #         f"{self.manufacturer.name} {self.manufacturer.country}")
    #
    # def test_driver_str(self):
    #     self.assertEqual(
    #         str(self.driver),
    #         f"{self.driver.username} "
    #         f"({self.driver.first_name} {self.driver.last_name})")
    #     self.assertEqual(self.driver.license_number, self.license_number)
    #     self.assertTrue(self.driver.check_password(self.password))
    #
    # def test_car_str(self):
    #     car = Car.objects.create(model="test", manufacturer=self.manufacturer)
    #     self.assertEqual(str(car), car.model)
    #
    # def test_driver_get_absolute_url(self):
    #     self.assertEqual(self.driver.get_absolute_url(), "/drivers/1/")
