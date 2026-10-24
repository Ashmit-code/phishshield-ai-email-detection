"""
Unit and integration tests for predictor.py (EmailPredictor engine).
"""
import unittest
from predictor import predictor

class TestEmailPredictor(unittest.TestCase):
    def test_predictor_bundle_loaded(self):
        self.assertIsNotNone(predictor.bundle)
        self.assertIsNotNone(predictor.tfidf)
        self.assertIsNotNone(predictor.scaler)
        self.assertGreater(len(predictor.models), 0)
        self.assertEqual(len(predictor.feature_names), 14)

    def test_parse_structured_input(self):
        msg = predictor.parse_input_to_email(
            raw_input="Test content inside email.",
            sender="boss@corporate.com",
            recipient="employee@corporate.com",
            subject="Meeting Schedule"
        )
        self.assertEqual(msg["From"], "boss@corporate.com")
        self.assertEqual(msg["Subject"], "Meeting Schedule")
        self.assertIn("Test content", msg.get_content())

    def test_analyze_phishing_email(self):
        phishing_text = (
            "From: service@paypal-update-account.com\n"
            "To: victim@example.com\n"
            "Subject: Urgent: Your Account Has Been Suspended!\n\n"
            "Dear Customer, please verify your credentials immediately at http://192.168.1.100/login "
            "to restore account access. If you fail to confirm, your funds will be permanently locked."
        )
        res = predictor.analyze_email(phishing_text)
        self.assertIn("verdict", res)
        self.assertEqual(res["verdict"], "PHISHING")
        self.assertTrue(res["is_phishing"])
        self.assertGreater(res["risk_score"], 50)
        self.assertIn(res["threat_level"], ["CRITICAL", "HIGH", "SUSPICIOUS"])
        self.assertGreater(len(res["red_flags"]), 0)
        self.assertEqual(len(res["features"]), 14)

    def test_analyze_legitimate_email(self):
        legit_text = (
            "From: colleague@enron.com\n"
            "To: teammate@enron.com\n"
            "Subject: Weekly Project Sync Notes\n\n"
            "Hi team, attached are the meeting minutes from Tuesday's planning session. "
            "Please review the action items before Friday's standup."
        )
        res = predictor.analyze_email(legit_text)
        self.assertIn("verdict", res)
        self.assertEqual(res["verdict"], "LEGITIMATE")
        self.assertFalse(res["is_phishing"])
        self.assertLess(res["risk_score"], 50)

if __name__ == "__main__":
    unittest.main()
