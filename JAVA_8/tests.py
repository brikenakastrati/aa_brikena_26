import csv
import os
import tempfile
import unittest

from fraud_detector import (
    ABBREVIATIONS_CSV,
    DEFAULT_CSV,
    AbbreviationRules,
    load_abbreviation_rules,
    FraudDetector,
    format_alerts,
    normalize_address,
    read_orders_csv,
    write_alerts_csv,
)

EXAMPLE_ORDERS = list(read_orders_csv(DEFAULT_CSV))


def order(order_id, email, address, timestamp):
    return {"order_id": order_id, "email": email,
            "address": address, "timestamp": timestamp}


class TestNormalizeAddress(unittest.TestCase):

    def test_case_punctuation_and_spaces(self):
        a = normalize_address("123 Main St, Apt 4B, Boston")
        b = normalize_address("  123   MAIN st.  apt 4b ;  boston ")
        self.assertEqual(a, b)
        self.assertEqual(a, "123 main st apt 4b boston")

    def test_abbreviations(self):
        cases = {
            "street": "st", "avenue": "ave", "road": "rd",
            "boulevard": "blvd", "drive": "dr", "lane": "ln",
            "court": "ct", "place": "pl",
        }
        for full, short in cases.items():
            with self.subTest(word=full):
                self.assertEqual(normalize_address(f"10 Elm {full}"),
                                 normalize_address(f"10 Elm {short}"))

    def test_unit_words(self):
        self.assertEqual(normalize_address("1 Elm St Apartment 2"),
                         normalize_address("1 Elm St Apt 2"))
        self.assertEqual(normalize_address("1 Elm St Unit 2"),
                         normalize_address("1 Elm St Apt 2"))
        self.assertEqual(normalize_address("1 Elm St Suite 2"),
                         normalize_address("1 Elm St Ste 2"))
        self.assertEqual(normalize_address("1 Elm St #2"),
                         normalize_address("1 Elm St Apt 2"))
        self.assertEqual(normalize_address("1 Elm St Apt #2"),
                         normalize_address("1 Elm St Apt 2"))

    def test_directions(self):
        self.assertEqual(normalize_address("5 North Main Street"),
                         normalize_address("5 N Main St"))
        self.assertEqual(normalize_address("5 West 3rd Avenue"),
                         normalize_address("5 W 3rd Ave"))

    def test_apartment_number_formats(self):
        expected = normalize_address("1 Elm St Apt 4B")
        self.assertEqual(normalize_address("1 Elm St Apt 4-B"), expected)
        self.assertEqual(normalize_address("1 Elm St Apt 4 - b"), expected)

    def test_number_ranges_not_joined(self):
        self.assertNotEqual(normalize_address("10-12 Elm St"),
                            normalize_address("1012 Elm St"))

    def test_nyc_variants(self):
        expected = normalize_address("1 Elm St, NYC")
        self.assertEqual(normalize_address("1 Elm St, New York City"), expected)
        self.assertEqual(normalize_address("1 Elm St, New York"), expected)

    def test_example_addresses_match(self):
        keys = {normalize_address(o["address"])
                for o in EXAMPLE_ORDERS if o["order_id"] in ("ORD001", "ORD003", "ORD005")}
        self.assertEqual(keys, {"123 main st apt 4b nyc"})

    def test_different_addresses_differ(self):
        self.assertNotEqual(normalize_address("123 Main St Apt 4B"),
                            normalize_address("123 Main St Apt 4C"))


class TestFraudDetector(unittest.TestCase):

    def test_example(self):
        alerts = FraudDetector().process_stream(EXAMPLE_ORDERS)
        self.assertEqual(alerts, [("ORD003", "ORD001"), ("ORD005", "ORD001")])
        self.assertEqual(
            format_alerts(alerts),
            "FRAUD ALERT:\n"
            "ORD003 - Matches previous order ORD001 (different email, same address)\n"
            "ORD005 - Matches previous order ORD001 (different email, same address)",
        )

    def test_same_email_not_flagged(self):
        d = FraudDetector()
        d.process_order(order("A", "x@mail.com", "1 Elm St", "2025-01-01 10:00"))
        self.assertIsNone(
            d.process_order(order("B", " X@Mail.com ", "1 Elm Street", "2025-01-01 11:00")))

    def test_exactly_24_hours_is_flagged(self):
        d = FraudDetector()
        d.process_order(order("A", "x@mail.com", "1 Elm St", "2025-01-01 10:00"))
        self.assertEqual(
            d.process_order(order("B", "y@mail.com", "1 Elm St", "2025-01-02 10:00")),
            ("B", "A"))

    def test_24_hours_and_1_minute_not_flagged(self):
        d = FraudDetector()
        d.process_order(order("A", "x@mail.com", "1 Elm St", "2025-01-01 10:00"))
        self.assertIsNone(
            d.process_order(order("B", "y@mail.com", "1 Elm St", "2025-01-02 10:01")))

    def test_earliest_match_reported(self):
        d = FraudDetector()
        d.process_order(order("A", "a@mail.com", "1 Elm St", "2025-01-01 10:00"))
        d.process_order(order("B", "b@mail.com", "1 Elm St", "2025-01-01 11:00"))
        self.assertEqual(
            d.process_order(order("C", "c@mail.com", "1 Elm St", "2025-01-01 12:00")),
            ("C", "A"))

    def test_earliest_with_same_email_is_skipped(self):
        d = FraudDetector()
        d.process_order(order("A", "c@mail.com", "1 Elm St", "2025-01-01 10:00"))
        d.process_order(order("B", "b@mail.com", "1 Elm St", "2025-01-01 11:00"))
        self.assertEqual(
            d.process_order(order("C", "c@mail.com", "1 Elm St", "2025-01-01 12:00")),
            ("C", "B"))

    def test_expired_orders_are_evicted(self):
        d = FraudDetector()
        d.process_order(order("A", "a@mail.com", "1 Elm St", "2025-01-01 10:00"))
        d.process_order(order("B", "b@mail.com", "1 Elm St", "2025-01-02 09:00"))
        # A is now older than 24h, so B is the earliest match.
        self.assertEqual(
            d.process_order(order("C", "c@mail.com", "1 Elm St", "2025-01-02 11:00")),
            ("C", "B"))
        timestamps = [entry[1] for entry in d.orders_by_address["1 elm st"]]
        self.assertEqual(timestamps, ["B", "C"])

    def test_flagged_orders_are_stored(self):
        d = FraudDetector()
        d.process_order(order("A", "a@mail.com", "1 Elm St", "2025-01-01 00:00"))
        d.process_order(order("B", "b@mail.com", "1 Elm St", "2025-01-01 12:00"))  # flagged
        # 30h after A, 18h after B: only the flagged order B is in the window.
        self.assertEqual(
            d.process_order(order("C", "c@mail.com", "1 Elm St", "2025-01-02 06:00")),
            ("C", "B"))

    def test_no_alerts_message(self):
        self.assertEqual(format_alerts([]), "No suspicious orders detected.")


class TestAbbreviationRules(unittest.TestCase):

    def test_csv_has_required_rules(self):
        rules = AbbreviationRules.from_csv(ABBREVIATIONS_CSV)
        self.assertEqual(rules.mapping["street"], "st")
        self.assertEqual(rules.mapping["apartment"], "apt")
        self.assertEqual(rules.mapping["new york city"], "nyc")

    def test_longer_phrases_applied_first(self):
        # Even if the shorter phrase is listed first, "new york city" must win.
        rules = AbbreviationRules({"new york": "ny", "new york city": "nyc"})
        self.assertEqual(normalize_address("1 Elm St New York City", rules),
                         "1 elm st nyc")

    def test_custom_rules_from_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "abbr.csv")
            with open(path, "w", newline="", encoding="utf-8") as f:
                f.write("pattern,replacement\nhighway,hwy\n\n Los  Angeles ,LA\n")
            rules = AbbreviationRules.from_csv(path)
        self.assertEqual(normalize_address("9 Pacific Highway, Los Angeles", rules),
                         "9 pacific hwy la")

    def test_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            load_abbreviation_rules("does_not_exist.csv")

    def test_bad_header_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "bad.csv")
            with open(path, "w", encoding="utf-8") as f:
                f.write("from,to\nstreet,st\n")
            with self.assertRaises(ValueError):
                AbbreviationRules.from_csv(path)


class TestAlertsCsv(unittest.TestCase):

    def test_alerts_written_to_csv(self):
        alerts = FraudDetector().process_stream(EXAMPLE_ORDERS)
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "fraud_alerts.csv")
            write_alerts_csv(alerts, path)
            with open(path, newline="", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
        self.assertEqual(rows, [
            {"order_id": "ORD003", "matched_order_id": "ORD001",
             "reason": "different email, same address"},
            {"order_id": "ORD005", "matched_order_id": "ORD001",
             "reason": "different email, same address"},
        ])

    def test_no_alerts_writes_header_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "fraud_alerts.csv")
            write_alerts_csv([], path)
            with open(path, encoding="utf-8") as f:
                content = f.read()
        self.assertEqual(content.strip(), "order_id,matched_order_id,reason")


if __name__ == "__main__":
    unittest.main()