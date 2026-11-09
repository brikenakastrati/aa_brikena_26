import csv
import re
import sys
from collections import deque
from datetime import datetime, timedelta
from pathlib import Path

WINDOW = timedelta(hours=24)
TIME_FORMAT = "%Y-%m-%d %H:%M"
ALERT_REASON = "different email, same address"

DEFAULT_CSV = Path(__file__).with_name("orders.csv")
DEFAULT_ALERTS_CSV = Path(__file__).with_name("fraud_alerts.csv")
ABBREVIATIONS_CSV = Path(__file__).with_name("abbreviations.csv")

UNIT_HYPHEN = re.compile(r"\b(\d+)\s*-\s*([a-z])\b")


class AbbreviationRules:
    """Address replacement rules, split into multi-word phrases and single words."""

    def __init__(self, mapping: dict):
        """Build the rules from a {pattern: replacement} dictionary."""
        self.mapping = {}
        for pattern, replacement in mapping.items():
            pattern = " ".join(pattern.lower().split())
            replacement = replacement.strip().lower()
            if pattern and replacement:
                self.mapping[pattern] = replacement

        phrase_items = sorted(
            ((p, r) for p, r in self.mapping.items() if " " in p),
            key=lambda item: len(item[0]),
            reverse=True,
        )
        self.phrases = [
            (re.compile(r"\b" + r"\s+".join(map(re.escape, p.split())) + r"\b"), r)
            for p, r in phrase_items
        ]
        self.words = {p: r for p, r in self.mapping.items() if " " not in p}

    @classmethod
    def from_csv(cls, path):
        """Load the rules from a CSV file with the columns pattern,replacement."""
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames or not {"pattern", "replacement"} <= set(reader.fieldnames):
                raise ValueError(f"{path} must have the columns: pattern,replacement")
            mapping = {
                row["pattern"]: row["replacement"]
                for row in reader
                if (row.get("pattern") or "").strip() and (row.get("replacement") or "").strip()
            }
        return cls(mapping)


def load_abbreviation_rules(path=ABBREVIATIONS_CSV) -> AbbreviationRules:
    """Load the address rules from abbreviations.csv."""
    if not Path(path).exists():
        raise FileNotFoundError(f"Abbreviations file not found: {path}")
    return AbbreviationRules.from_csv(path)


RULES = load_abbreviation_rules()


def normalize_address(address: str, rules: AbbreviationRules = None) -> str:
    """Turn an address into a standard form so small variations give the same key.

    Uses the rules from abbreviations.csv unless other rules are given.

    Example: "123 Main Street Apt 4-B New York City" -> "123 main st apt 4b nyc"
    """
    rules = rules or RULES

    text = address.lower().strip()
    for pattern, replacement in rules.phrases:
        text = pattern.sub(replacement, text)
    text = UNIT_HYPHEN.sub(r"\1\2", text)
    text = text.replace("#", " apt ")
    text = re.sub(r"[^\w\s]", " ", text)

    tokens = [rules.words.get(tok, tok) for tok in text.split()]

    cleaned = []
    for tok in tokens:
        if tok in ("apt", "ste") and cleaned and cleaned[-1] == tok:
            continue
        cleaned.append(tok)
    return " ".join(cleaned)


def normalize_email(email: str) -> str:
    """Lowercase an email and remove surrounding spaces."""
    return email.strip().lower()


def parse_timestamp(value):
    """Convert a 'YYYY-MM-DD HH:MM' string to a datetime."""
    if isinstance(value, datetime):
        return value
    return datetime.strptime(value.strip(), TIME_FORMAT)


class FraudDetector:
    """Flags orders that reuse a recent order's address with a different email."""

    def __init__(self, window: timedelta = WINDOW):
        """Create an empty detector with a hash table of address -> recent orders."""
        self.window = window
        self.orders_by_address = {}

    def process_order(self, order: dict):
        """Check one order and store it.

        Returns (order_id, matched_order_id) if it matches the earliest order
        from the last 24 hours with a different email, otherwise None.
        """
        order_id = order["order_id"]
        email = normalize_email(order["email"])
        timestamp = parse_timestamp(order["timestamp"])
        key = normalize_address(order["address"])

        bucket = self.orders_by_address.setdefault(key, deque())

        while bucket and timestamp - bucket[0][0] > self.window:
            bucket.popleft()

        match = None
        for _prev_time, prev_id, prev_email in bucket:
            if prev_email != email:
                match = prev_id
                break

        bucket.append((timestamp, order_id, email))
        return (order_id, match) if match is not None else None

    def process_stream(self, orders):
        """Process orders in order and return the list of alerts."""
        alerts = []
        for order in orders:
            result = self.process_order(order)
            if result:
                alerts.append(result)
        return alerts


def format_alerts(alerts) -> str:
    """Return the alerts as printable text."""
    if not alerts:
        return "No suspicious orders detected."
    lines = ["FRAUD ALERT:"]
    for order_id, matched_id in alerts:
        lines.append(f"{order_id} - Matches previous order {matched_id} ({ALERT_REASON})")
    return "\n".join(lines)


def read_orders_csv(path):
    """Yield orders one by one from a CSV file (order_id, email, address, timestamp)."""
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            yield row


def write_alerts_csv(alerts, path):
    """Save the alerts to a CSV file (order_id, matched_order_id, reason)."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["order_id", "matched_order_id", "reason"])
        for order_id, matched_id in alerts:
            writer.writerow([order_id, matched_id, ALERT_REASON])


def main():
    """Read orders.csv, print the alerts and save them to fraud_alerts.csv.

    Other files can be given: python fraud_detector.py [orders.csv] [fraud_alerts.csv]
    """
    orders_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CSV
    alerts_path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_ALERTS_CSV

    alerts = FraudDetector().process_stream(read_orders_csv(orders_path))

    print(format_alerts(alerts))
    write_alerts_csv(alerts, alerts_path)
    print(f"\n{len(alerts)} alert(s) written to {alerts_path}")


if __name__ == "__main__":
    main()