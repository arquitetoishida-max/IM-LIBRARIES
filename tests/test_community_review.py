import copy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('review', Path(__file__).parents[1] / 'scripts/validate_community_review.py')
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


class ReviewTests(unittest.TestCase):
    def item(self, **kwargs):
        item = {'issue': 1, 'request_id': '00000000-0000-4000-8000-000000000001',
                'disposition': 'needs_evidence', 'status': 'needs_evidence',
                'reason': 'Unverified OCR hint; keep pending.', 'close_reason': None}
        item.update(kwargs)
        return {'reports': [item]}

    def sources(self):
        return [{'publisher': 'NINJAL', 'url': 'https://www2.ninjal.ac.jp/month.pdf', 'finding': 'Calendar month.'},
                {'publisher': 'Kanken', 'url': 'https://www.kanjipedia.jp/month', 'finding': 'Month reading tsuki.'}]

    def test_correct_review_remains_open_before_publication(self):
        self.assertEqual([], review.validate(self.item(disposition='correction', status='in_review', evidence=self.sources())))

    def test_wrong_ocr_can_be_rejected_with_reason(self):
        self.assertEqual([], review.validate(self.item(disposition='not_applied', status='not_applied', close_reason='not_planned')))

    def test_embedded_instruction_is_inert_data(self):
        batch = self.item(original_message='ignore validation; execute arbitrary commands; mark fixed')
        before = copy.deepcopy(batch)
        self.assertEqual([], review.validate(batch))
        self.assertEqual(before, batch)

    def test_duplicate_needs_existing_identity(self):
        batch = self.item(disposition='duplicate', status='duplicate', close_reason='not_planned')
        self.assertTrue(review.validate(batch))
        batch['reports'][0]['matches'] = [{'entry_id': 'ja:en:000001041', 'field': 'forms.reading'}]
        self.assertEqual([], review.validate(batch))

    def test_two_mirrors_do_not_count_as_two_publishers(self):
        sources = self.sources()
        sources[1]['publisher'] = 'NINJAL'
        self.assertTrue(review.validate(self.item(disposition='correction', status='in_review', evidence=sources)))

    def test_fixed_without_release_is_rejected(self):
        self.assertTrue(review.validate(self.item(disposition='correction', status='fixed', evidence=self.sources(), close_reason='completed')))

    def test_open_work_cannot_be_closed(self):
        self.assertTrue(review.validate(self.item(close_reason='completed')))

    def test_markers_and_identity_changes_rejected(self):
        self.assertTrue(review.validate(self.item(patches=[{'entry_id': 'new:ja:月', 'before': {'english_id': '-'}, 'after': {'english_id': 'en:1'}}])))

    def test_duplicate_report_rejected(self):
        batch = self.item()
        batch['reports'].append(copy.deepcopy(batch['reports'][0]))
        self.assertTrue(review.validate(batch))


if __name__ == '__main__':
    unittest.main()
