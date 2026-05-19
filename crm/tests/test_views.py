from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from crm.models import Client, ServiceCategory, Worker, Order, Specialty

INDEX_URL = reverse("crm:index")


class PublicIndexTest(TestCase):
    def test_login_required(self):
        res = self.client.get(INDEX_URL)
        self.assertNotEqual(res.status_code, 200)


class BaseTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_superuser(
            username="testuser", password="user12test"
        )
        self.client.force_login(self.user)
        self.form_data = {"name": "newcategory", "hour_cost": 400}
        self.client.post(reverse("crm:service-category-create"), self.form_data)
        self.new_category = ServiceCategory.objects.get(name=self.form_data["name"])
        self.new_specialty = Specialty.objects.create(name="new_specialty")
        self.new_client = Client.objects.create(
            model="BMW",
            license_plate="AS1526KI",
            owner_name="Igor",
            phone_number="+380954235698",
        )


class PrivateIndexTest(BaseTestCase):
    def test_index_context(self):
        response1 = self.client.get(INDEX_URL)
        self.assertEqual(response1.context["num_visits"], 1)
        response2 = self.client.get(INDEX_URL)
        self.assertEqual(response2.context["num_visits"], 2)
        keys = ["sum_all", "sum_month", "num_orders", "num_worker"]
        for key in keys:
            self.assertIn(key, response1.context)
        self.assertTemplateUsed(response1, "crm/index.html")


class PrivateServiceCategoryTests(BaseTestCase):

    def test_create_service_category(self):
        self.assertEqual(
            (self.new_category.name, self.new_category.hour_cost),
            (self.form_data["name"], self.form_data["hour_cost"]),
        )

    def test_service_category_list_context(self):
        res = self.client.get(reverse("crm:service-category-list"), {"name": "test"})
        self.assertIn("search_form", res.context)
        form = res.context["search_form"]
        self.assertEqual(form.initial["name"], "test")


class PrivateWorkerTests(BaseTestCase):

    def test_create_worker(self):
        form_data = {
            "username": "newuser",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "test",
            "last_name": "user",
            "specialty": self.new_specialty.id,
        }
        self.client.post(reverse("crm:worker-create"), form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.specialty.id, form_data["specialty"])
        self.assertEqual(
            (new_user.first_name, new_user.last_name, new_user.username),
            (form_data["first_name"], form_data["last_name"], form_data["username"]),
        )

    def test_worker_list_context(self):
        res = self.client.get(reverse("crm:worker-list"), {"last_name": "test"})
        self.assertIn("search_form", res.context)
        form = res.context["search_form"]
        self.assertEqual(form.initial["last_name"], "test")

    def test_worker_detail_context(self):
        res = self.client.get(reverse("crm:worker-detail", kwargs={"pk": self.user.pk}))
        self.assertEqual(res.status_code, 200)
        self.assertIn("earn_all_time", res.context)
        self.assertIn("year", res.context)
        self.assertIn("month", res.context)
        self.assertIn("earn_month", res.context)
        self.assertIn("count_all_time", res.context)
        self.assertIn("count_month", res.context)
        self.assertIn("monthly_stats", res.context)
        self.assertIn("orders", res.context)


class PrivateOrderTests(BaseTestCase):

    def test_create_order(self):
        form_data = {
            "category": self.new_category.id,
            "client": self.new_client.id,
            "description": "Big problem",
            "performers": [self.user.id],
            "norm_hours": 4,
        }
        response = self.client.post(reverse("crm:order-create"), form_data)
        self.assertEqual(response.status_code, 302)
        new_order = Order.objects.get(description="Big problem")
        self.assertEqual(new_order.category.id, form_data["category"])
        self.assertEqual(new_order.client.id, form_data["client"])
        self.assertEqual(new_order.description, form_data["description"])
        self.assertEqual(new_order.norm_hours, form_data["norm_hours"])
        self.assertIn(self.user, new_order.performers.all())
