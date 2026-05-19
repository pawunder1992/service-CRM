from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from crm.models import Specialty


class AdminTest(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="testadmin"
        )
        self.client.force_login(self.admin_user)
        self.specialty = Specialty.objects.create(name="specialty")
        self.worker = get_user_model().objects.create_user(
            username="worker",
            first_name="firstTest",
            last_name="lastTest",
            password="workerpassword",
            specialty=self.specialty,
        )

    def test_worker_specialty_listed(self):
        """
        Test that the worker specialty listed in the admin panel
        :return:
        """
        url = reverse("admin:crm_worker_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.worker.specialty.name)

    def test_worker_detail_specialty_listed(self):
        """
        Test that the worker detail specialty listed in the admin panel
        :return:
        """
        url = reverse("admin:crm_worker_change", args=[self.worker.id])
        res = self.client.get(url)
        self.assertContains(res, self.worker.specialty.name)

    def test_worker_add_changelist(self):
        url = reverse("admin:crm_worker_add")
        res = self.client.get(url)
        self.assertContains(res, "First name")
        self.assertContains(res, "Last name")
        self.assertContains(res, "Specialty")
        self.assertContains(res, "Additional info")
