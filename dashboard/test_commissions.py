from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase, override_settings
from django.urls import reverse

from commissions.models import CommissionOrder


@override_settings(
    STORAGES={
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
)
class CommissionDashboardTests(TestCase):
    """
    Test commission listing, filtering, completion and permissions
    in the artist dashboard.
    """

    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()

        cls.customer = user_model.objects.create_user(
            username="commissioncustomer",
            password="testpassword123",
        )

        cls.artist = user_model.objects.create_user(
            username="commissionartist",
            password="testpassword123",
        )

        artist_group, _ = Group.objects.get_or_create(
            name="Artists",
        )
        cls.artist.groups.add(artist_group)

        cls.regular_user = user_model.objects.create_user(
            username="commissionregular",
            password="testpassword123",
        )

        cls.superuser = user_model.objects.create_superuser(
            username="commissionadmin",
            email="admin@example.com",
            password="testpassword123",
        )

        order_details = {
            "user": cls.customer,
            "creative_direction": "surprise",
            "artwork_format": "digital",
            "artwork_price": Decimal("100.00"),
            "shipping_cost": Decimal("0.00"),
            "total_price": Decimal("100.00"),
            "full_name": "Test Customer",
            "email": "customer@example.com",
        }

        cls.todo_order = CommissionOrder.objects.create(
            **order_details,
            payment_status="paid",
            is_completed=False,
        )

        cls.completed_order = CommissionOrder.objects.create(
            **order_details,
            payment_status="paid",
            is_completed=True,
        )

        cls.pending_order = CommissionOrder.objects.create(
            **order_details,
            payment_status="pending",
        )

        cls.failed_order = CommissionOrder.objects.create(
            **order_details,
            payment_status="failed",
        )

    def setUp(self):
        self.client.force_login(self.artist)
        self.list_url = reverse("dashboard:commission_list")
        self.complete_url = reverse(
            "dashboard:commission_mark_completed",
            kwargs={"pk": self.todo_order.pk},
        )

    def test_commission_list_uses_correct_template(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "dashboard/commission_list.html",
        )

    def test_default_filter_shows_only_paid_todo_orders(self):
        response = self.client.get(self.list_url)

        orders = list(response.context["orders"])

        self.assertEqual(response.context["selected_status"], "todo")
        self.assertEqual(orders, [self.todo_order])

    def test_completed_filter_shows_only_completed_paid_orders(self):
        response = self.client.get(
            self.list_url,
            {"status": "completed"},
        )

        orders = list(response.context["orders"])

        self.assertEqual(
            response.context["selected_status"],
            "completed",
        )
        self.assertEqual(orders, [self.completed_order])

    def test_all_filter_shows_all_paid_orders_only(self):
        response = self.client.get(
            self.list_url,
            {"status": "all"},
        )

        orders = list(response.context["orders"])

        self.assertEqual(len(orders), 2)
        self.assertIn(self.todo_order, orders)
        self.assertIn(self.completed_order, orders)
        self.assertNotIn(self.pending_order, orders)
        self.assertNotIn(self.failed_order, orders)

    def test_invalid_filter_falls_back_to_todo(self):
        response = self.client.get(
            self.list_url,
            {"status": "invalid"},
        )

        self.assertEqual(response.context["selected_status"], "todo")
        self.assertEqual(
            list(response.context["orders"]),
            [self.todo_order],
        )

    def test_artist_can_mark_paid_order_completed(self):
        response = self.client.post(self.complete_url)

        self.todo_order.refresh_from_db()

        self.assertTrue(self.todo_order.is_completed)
        self.assertRedirects(response, self.list_url)

    def test_completed_order_moves_to_completed_filter(self):
        self.client.post(self.complete_url)

        todo_response = self.client.get(self.list_url)
        completed_response = self.client.get(
            self.list_url,
            {"status": "completed"},
        )

        self.assertNotIn(
            self.todo_order,
            todo_response.context["orders"],
        )
        self.assertIn(
            self.todo_order,
            completed_response.context["orders"],
        )

    def test_get_request_cannot_mark_order_completed(self):
        response = self.client.get(self.complete_url)

        self.todo_order.refresh_from_db()

        self.assertEqual(response.status_code, 405)
        self.assertFalse(self.todo_order.is_completed)

    def test_pending_order_cannot_be_marked_completed(self):
        url = reverse(
            "dashboard:commission_mark_completed",
            kwargs={"pk": self.pending_order.pk},
        )

        response = self.client.post(url)

        self.pending_order.refresh_from_db()

        self.assertEqual(response.status_code, 404)
        self.assertFalse(self.pending_order.is_completed)

    def test_nonexistent_order_returns_404(self):
        url = reverse(
            "dashboard:commission_mark_completed",
            kwargs={"pk": 999999},
        )

        response = self.client.post(url)

        self.assertEqual(response.status_code, 404)

    def test_already_completed_order_remains_completed(self):
        url = reverse(
            "dashboard:commission_mark_completed",
            kwargs={"pk": self.completed_order.pk},
        )

        response = self.client.post(url)

        self.completed_order.refresh_from_db()

        self.assertTrue(self.completed_order.is_completed)
        self.assertRedirects(response, self.list_url)

    def test_anonymous_user_redirected_from_commission_list(self):
        self.client.logout()

        response = self.client.get(self.list_url)

        self.assertRedirects(
            response,
            f"/accounts/login/?next={self.list_url}",
        )

    def test_regular_user_cannot_access_commission_list(self):
        self.client.force_login(self.regular_user)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 403)

    def test_superuser_can_access_commission_list(self):
        self.client.force_login(self.superuser)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_cannot_complete_order(self):
        self.client.logout()

        response = self.client.post(self.complete_url)

        self.todo_order.refresh_from_db()

        self.assertRedirects(
            response,
            f"/accounts/login/?next={self.complete_url}",
        )
        self.assertFalse(self.todo_order.is_completed)

    def test_regular_user_cannot_complete_order(self):
        self.client.force_login(self.regular_user)

        response = self.client.post(self.complete_url)

        self.todo_order.refresh_from_db()

        self.assertEqual(response.status_code, 403)
        self.assertFalse(self.todo_order.is_completed)

    def test_superuser_can_complete_paid_order(self):
        self.client.force_login(self.superuser)

        response = self.client.post(self.complete_url)

        self.todo_order.refresh_from_db()

        self.assertTrue(self.todo_order.is_completed)
        self.assertRedirects(response, self.list_url)
