"""Validate editorial report decisions; never execute messages, close issues or publish."""
import argparse
import json
import re
from urllib.parse import urlparse

STATES = {'in_review', 'needs_evidence', 'not_applied', 'duplicate', 'fixed', 'accepted'}
DISPOSITIONS = {'correction', 'clarification', 'not_applied', 'duplicate', 'needs_evidence'}
IDENTITY = {'id', 'english_id', 'english_sense_id', 'kind', 'forms'}


def validate(batch):
    errors = []
    reports = batch.get('reports', [])
    seen_issues, seen_requests = set(), set()
    for item in reports:
        n = item.get('issue')
        prefix = f'issue {n}: '
        request = item.get('request_id', '')
        if not isinstance(n, int) or isinstance(n, bool) or n <= 0 or n in seen_issues:
            errors.append(prefix + 'invalid or repeated issue')
        seen_issues.add(n)
        if not re.fullmatch(r'[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}', request) or request in seen_requests:
            errors.append(prefix + 'invalid or repeated request_id')
        seen_requests.add(request)
        disposition, status = item.get('disposition'), item.get('status')
        if disposition not in DISPOSITIONS or status not in STATES or not item.get('reason'):
            errors.append(prefix + 'missing disposition, status or reason')
        allowed = {'correction': {'in_review', 'fixed', 'accepted'},
                   'clarification': {'in_review', 'not_applied', 'fixed'},
                   'duplicate': {'duplicate'}, 'not_applied': {'not_applied'},
                   'needs_evidence': {'needs_evidence'}}
        if disposition in allowed and status not in allowed[disposition]:
            errors.append(prefix + 'status conflicts with disposition')
        sources = item.get('evidence', [])
        publishers, hosts = set(), set()
        for source in sources:
            parsed = urlparse(source.get('url', ''))
            publisher = source.get('publisher', '').strip().casefold()
            if parsed.scheme != 'https' or not parsed.hostname or not publisher or not source.get('finding'):
                errors.append(prefix + 'invalid evidence')
            else:
                publishers.add(publisher)
                hosts.add(parsed.hostname.removeprefix('www.'))
        if disposition in {'correction', 'clarification'} or status in {'accepted', 'fixed'}:
            if len(publishers) < 2 or len(hosts) < 2:
                errors.append(prefix + 'requires two independent evidence publishers/hosts')
        if disposition == 'duplicate' and not item.get('matches') and not item.get('canonical_issue'):
            errors.append(prefix + 'duplicate requires entry/form matches or canonical issue')
        for patch in item.get('patches', []):
            if patch.get('entry_id', '').startswith(('new:', '-')) or not patch.get('entry_id'):
                errors.append(prefix + 'intake marker is not a published identity')
            before, after = patch.get('before', {}), patch.get('after', {})
            if not after or set(before) != set(after):
                errors.append(prefix + 'patch requires equal nonempty before/after field sets')
            if IDENTITY.intersection(after):
                errors.append(prefix + 'identity/forms changes need their separate migration review')
        if status in {'fixed', 'accepted'}:
            release = item.get('release', {})
            if not release.get('version') or not release.get('catalog_commit') or not re.fullmatch(r'[0-9a-f]{64}', release.get('sha256', '')) or release.get('catalog_verified') is not True:
                errors.append(prefix + 'terminal success requires verified publication/version/hash/commit')
        expected_close = 'completed' if status in {'fixed', 'accepted'} else 'not_planned' if status in {'not_applied', 'duplicate'} else None
        if item.get('close_reason') != expected_close:
            errors.append(prefix + 'closing before resolution or incorrect state reason')
    if not reports:
        errors.append('empty batch')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('review')
    args = parser.parse_args()
    with open(args.review, encoding='utf-8') as f:
        batch = json.load(f)
    errors = validate(batch)
    for error in errors:
        print('ERROR', error)
    print(f"{len(batch.get('reports', []))} reports; {len(errors)} errors")
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
