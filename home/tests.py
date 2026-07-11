from django.test import TestCase

from home.templatetags.minitower_extras import status_badge_class


class StatusBadgeClassFilterTests(TestCase):
    def test_connected_is_up(self):
        self.assertEqual(status_badge_class("Connected"), "status-badge--up")

    def test_case_insensitive(self):
        self.assertEqual(status_badge_class("ACTIVE"), "status-badge--up")

    def test_unknown_value_is_down(self):
        self.assertEqual(status_badge_class("Disconnected"), "status-badge--down")

    def test_empty_value_is_down(self):
        self.assertEqual(status_badge_class(""), "status-badge--down")

    def test_none_value_is_down(self):
        self.assertEqual(status_badge_class(None), "status-badge--down")
