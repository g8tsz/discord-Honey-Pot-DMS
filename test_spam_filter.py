import unittest

from spam_filter import is_promotional_spam


class SpamFilterTests(unittest.TestCase):
    def test_promotions(self):
        for message in (
            "Like Poker or sports betting? We got you! discord.gg/example",
            "GENER­ATIONAL RUN ALERT. Super Whale Plays, Diamond Plays, Daily picks. "
            "100 percent FREE Discord. Join Our Discord https://discord.gg/example",
            "Casino deposit bonus. Register today!",
            "VIP picks — DM me for access.",
        ):
            with self.subTest(message=message):
                self.assertTrue(is_promotional_spam(message))

    def test_ordinary_dms(self):
        for message in ("hi", "", "Anyone playing poker tonight?", "I just won at slots!",
                        "discord.gg/example", "What does daily rakeback mean?",
                        "Poker rules: https://example.org/rules"):
            with self.subTest(message=message):
                self.assertFalse(is_promotional_spam(message))
