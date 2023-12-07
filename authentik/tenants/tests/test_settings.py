"""Test Settings API"""
from json import loads

from django.urls import reverse
from django_tenants.utils import get_public_schema_name

from authentik.core.tests.utils import create_test_admin_user
from authentik.lib.config import CONFIG
from authentik.lib.generators import generate_id
from authentik.tenants.models import Domain, Tenant
from authentik.tenants.tests.utils import TenantAPITestCase

TENANTS_API_KEY = generate_id()
HEADERS = {"Authorization": f"Bearer {TENANTS_API_KEY}"}


class TestSettingsAPI(TenantAPITestCase):
    def setUp(self):
        super().setUp()
        self.tenant_1 = Tenant.objects.get(schema_name=get_public_schema_name())
        with self.tenant_1:
            self.admin_1 = create_test_admin_user()
        self.tenant_2 = Tenant.objects.create(
            name=generate_id(), schema_name="t_" + generate_id().lower()
        )
        Domain.objects.create(tenant=self.tenant_2, domain="tenant_2.testserver")
        with self.tenant_2:
            self.admin_2 = create_test_admin_user()

    def test_settings(self):
        """Test settings API"""
        # We need those context managers here because the test client doesn't put itself
        # in the tenant context as a real request would.
        with self.tenant_1:
            self.client.force_login(self.admin_1)
        response = self.client.patch(
            reverse("authentik_api:tenant_settings"),
            data={
                "avatars": "tenant_1_mode",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.tenant_1.refresh_from_db()
        self.assertEqual(self.tenant_1.avatars, "tenant_1_mode")
        with self.tenant_1:
            self.client.logout()

        # with self.tenant_2:
        #     self.client.force_login(self.admin_2)
        # response = self.client.patch(
        #     reverse("authentik_api:tenant_settings"),
        #     data={
        #         "avatars": "tenant_2_mode",
        #     },
        #     headers={
        #         "Host": "tenant_2.testserver",
        #     },
        # )
        # self.assertEqual(response.status_code, 200)
        # self.tenant_2.refresh_from_db()
        # self.assertEqual(self.tenant_2.avatars, "tenant_2_mode")
        # with self.tenant_2:
        #     self.client.logout()

        # with self.tenant_1:
        #     self.client.force_login(self.admin_1)
        # response_1 = self.client.get(
        #     reverse("authentik_api:tenant_settings"),
        # )
        # self.assertEqual(response_1.status_code, 200)
        # body_1 = loads(response_1.content.decode())
        # with self.tenant_1:
        #     self.client.logout()
        # with self.tenant_2:
        #     self.client.force_login(self.admin_2)
        # response_2 = self.client.get(
        #     reverse("authentik_api:tenant_settings"),
        #     headers={
        #         "host": "tenant_2.testserver",
        #     },
        # )
        # self.assertEqual(response_2.status_code, 200)
        # body_2 = loads(response_2.content.decode())
        # with self.tenant_2:
        #     self.client.logout()
        # self.assertNotEqual(body_1["avatars"], body_2["avatars"])