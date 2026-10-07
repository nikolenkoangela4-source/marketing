"""Integrity and decision-boundary tests; all figures here are synthetic fixtures."""
import copy
import unittest
import growth_cycle as engine


class IntegrityTests(unittest.TestCase):
    def payload(self, reach=2000, saves=24):
        return {"data": [{"media_id": "example", "timestamp": "2026-01-01T12:00:00Z",
                         "data_fetched_at": "2026-01-08T14:00:00Z", "media_type": "CAROUSEL_ALBUM",
                         "media_reach": reach, "media_saved": saves, "media_shares": 10}]}

    def experiment(self):
        return {"id": "synthetic-test", "format": "CAROUSEL_ALBUM",
                "design_type": "prospective_observational_test", "rules_locked_at": "2025-12-31T12:00:00Z",
                "primary_metric": "saves_per_1000_reached",
                "publication": {"media_id": "example", "published_at": "2026-01-01T12:00:00Z"},
                "decision_rules": {"target_age_hours": 168, "tolerance_hours": 24,
                                   "target_rate": 10, "minimum_reach": 2000}}

    def test_missing_is_not_zero(self):
        self.assertIsNone(engine.rate(None, 100))
        self.assertEqual(engine.rate(0, 100), 0)
        self.assertIsNone(engine.rate(10, 0))

    def test_unknown_primary_metric_is_not_substituted(self):
        exp = self.experiment(); exp['primary_metric'] = 'follows_per_1000'
        with self.assertRaises(ValueError): engine.decide(exp, [], '2026-01-09T12:00:00Z')

    def test_duplicates_do_not_inflate_lifetime_metrics(self):
        data = self.payload(); data["data"].append(copy.deepcopy(data["data"][0]))
        with self.assertRaises(ValueError): engine.normalize(data)

    def test_recent_posts_are_excluded_from_mature_context(self):
        data = self.payload(); data["data"][0]["data_fetched_at"] = "2026-01-02T12:00:00Z"
        out = engine.baseline(data, "2026-01-01")
        self.assertEqual(out["mature_rows"], 0)
        self.assertIsNone(out["cohorts"]["CAROUSEL_ALBUM"]["medians"]["reach"])

    def test_snapshot_uses_source_capture_time(self):
        snap = engine.record(self.experiment(), self.payload())
        self.assertEqual(snap["age_hours"], 170)

    def test_unpublished_is_not_completed(self):
        exp = self.experiment(); exp["publication"] = {}
        self.assertEqual(engine.decide(exp, [], "2026-01-09T12:00:00Z")["decision"], "WAITING_PUBLICATION")

    def test_cached_early_data_cannot_be_a_seven_day_result(self):
        data = self.payload(); data["data"][0]["data_fetched_at"] = "2026-01-02T12:00:00Z"
        snap = engine.record(self.experiment(), data)
        out = engine.decide(self.experiment(), [snap], "2026-01-08T16:00:00Z")
        self.assertEqual(out["decision"], "INCONCLUSIVE")

    def test_late_rules_are_not_preregistration(self):
        exp = self.experiment(); exp["rules_locked_at"] = "2026-01-02T12:00:00Z"
        with self.assertRaises(ValueError): engine.decide(exp, [], "2026-01-09T12:00:00Z")

    def test_operating_success_requests_replication_not_causality(self):
        exp = self.experiment(); snap = engine.record(exp, self.payload())
        out = engine.decide(exp, [snap], "2026-01-08T16:00:00Z")
        self.assertEqual(out["decision"], "RETEST")
        self.assertFalse(out["causal_claim"])
        self.assertFalse(out["matched_age_winner"])

    def test_missing_metric_stays_inconclusive(self):
        exp = self.experiment(); snap = engine.record(exp, self.payload(saves=None))
        self.assertEqual(engine.decide(exp, [snap], "2026-01-08T16:00:00Z")["decision"], "INCONCLUSIVE")

    def test_low_reach_is_not_a_failed_topic(self):
        exp = self.experiment(); snap = engine.record(exp, self.payload(reach=100))
        self.assertEqual(engine.decide(exp, [snap], "2026-01-08T16:00:00Z")["decision"], "RETEST")

    def test_wrong_media_and_future_snapshot_are_rejected(self):
        exp = self.experiment(); snap = engine.record(exp, self.payload())
        snap["media_id"] = "someone-else"
        with self.assertRaises(ValueError): engine.decide(exp, [snap], "2026-01-08T16:00:00Z")
        snap["media_id"] = "example"
        with self.assertRaises(ValueError): engine.decide(exp, [snap], "2026-01-08T13:00:00Z")


if __name__ == "__main__":
    unittest.main()
