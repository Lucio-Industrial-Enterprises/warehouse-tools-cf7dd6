import unittest

from warehouse.rates import shipping_quote


class StandardRateTests(unittest.TestCase):
    def test_standard_local(self):
        self.assertEqual(shipping_quote(2, "local"), 8.0)

    def test_standard_regional(self):
        self.assertEqual(shipping_quote(2, "regional"), 11.0)

    def test_standard_explicit_service(self):
        self.assertEqual(shipping_quote(2, "local", service="standard"), 8.0)

    def test_invalid_weight(self):
        with self.assertRaises(ValueError):
            shipping_quote(0, "local")

    def test_invalid_zone(self):
        with self.assertRaises(ValueError):
            shipping_quote(1, "international")

    def test_invalid_service(self):
        with self.assertRaises(ValueError):
            shipping_quote(1, "local", service="overnight")


class ExpressRateTests(unittest.TestCase):
    # Express adds $7 to the standard base for the given zone.

    def test_express_local(self):
        # standard local: 5.0 + 1.5*2 = 8.0  →  express: 8.0 + 7.0 = 15.0
        self.assertEqual(shipping_quote(2, "local", service="express"), 15.0)

    def test_express_regional(self):
        # standard regional: 8.0 + 1.5*2 = 11.0  →  express: 11.0 + 7.0 = 18.0
        self.assertEqual(shipping_quote(2, "regional", service="express"), 18.0)

    def test_express_fractional_weight(self):
        # local base 5+7=12, weight portion 1.5*1.5=2.25  →  14.25
        self.assertEqual(shipping_quote(1.5, "local", service="express"), 14.25)

    def test_express_costs_more_than_standard(self):
        for zone in ("local", "regional"):
            with self.subTest(zone=zone):
                standard = shipping_quote(5, zone, service="standard")
                express = shipping_quote(5, zone, service="express")
                self.assertGreater(express, standard)

    def test_express_surcharge_is_seven_dollars(self):
        for zone in ("local", "regional"):
            with self.subTest(zone=zone):
                diff = (
                    shipping_quote(3, zone, service="express")
                    - shipping_quote(3, zone, service="standard")
                )
                self.assertAlmostEqual(diff, 7.0)
