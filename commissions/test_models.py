from django.contrib.auth import get_user_model
from django.db.models.deletion import ProtectedError
from django.test import TestCase

from .models import CommissionOrder


class CommissionOrderModelTest(TestCase):
    """
    Tests commission order creation, default values,
    unique references and relationships.
    """

    @classmethod
    def setUpTestData(cls):
        # Create a registered customer shared by the tests.
        cls.user = get_user_model().objects.create_user(
            username="testcustomer",
            email="customer@example.com",
            password="testpass123",
        )

    def create_commission(self, **overrides):
        """
        Create a valid commission with reusable test data.
        Individual tests can override specific fields.
        """
        data = {
            "user": self.user,
            "creative_direction": "idea",
            "story": "A dreamlike landscape with classical elements.",
            "moods": ["dreamlike", "nostalgic"],
            "colours": ["blue", "pink"],
            "imagery": "classical",
            "artwork_format": "digital",
            "artwork_price": "180.00",
            "shipping_cost": "0.00",
            "total_price": "180.00",
            "full_name": "Test Customer",
            "email": "customer@example.com",
        }

        # Allow each test to change only the fields it needs.
        data.update(overrides)

        return CommissionOrder.objects.create(**data)

    def test_commission_order_creation(self):
        """
        Test that a commission stores creative choices,
        customer details and prices correctly.
        """
        order = self.create_commission()

        saved_order = CommissionOrder.objects.get(pk=order.pk)

        self.assertEqual(saved_order.creative_direction, "idea")
        self.assertEqual(
            saved_order.story,
            "A dreamlike landscape with classical elements.",
        )
        self.assertEqual(
            saved_order.moods,
            ["dreamlike", "nostalgic"],
        )
        self.assertEqual(saved_order.colours, ["blue", "pink"])
        self.assertEqual(saved_order.imagery, "classical")
        self.assertEqual(saved_order.artwork_format, "digital")
        self.assertEqual(saved_order.full_name, "Test Customer")
        self.assertEqual(saved_order.email, "customer@example.com")
        self.assertEqual(saved_order.total_price, 180)

    def test_order_numbers_are_unique(self):
        """
        Test that each commission receives a different UUID.
        """
        first_order = self.create_commission()
        second_order = self.create_commission()

        self.assertNotEqual(
            first_order.order_number,
            second_order.order_number,
        )

    def test_new_order_defaults_to_pending(self):
        """
        Test that newly created orders are awaiting payment.
        """
        order = self.create_commission()

        self.assertEqual(order.payment_status, "pending")

    def test_commission_belongs_to_registered_user(self):
        """
        Test the relationship between a commission and its customer.
        """
        order = self.create_commission()

        self.assertEqual(order.user, self.user)
        self.assertIn(order, self.user.commission_orders.all())

    def test_user_with_commission_cannot_be_deleted(self):
        """
        Test that PROTECT prevents deleting customers
        who have existing commission orders.
        """
        order = self.create_commission()

        # Preserve order history by preventing customer deletion.
        with self.assertRaises(ProtectedError):
            self.user.delete()

        self.assertTrue(get_user_model().objects.filter(pk=self.user.pk).exists())
        self.assertTrue(CommissionOrder.objects.filter(pk=order.pk).exists())

    def test_commission_string_method(self):
        """
        Test that the order's string representation
        contains its reference and customer name.
        """
        order = self.create_commission()

        expected = f"Commission {order.order_number} - Test Customer"

        self.assertEqual(str(order), expected)
