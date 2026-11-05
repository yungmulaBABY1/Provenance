CANDIDATES — PROPOSED INSTRUMENT VERSIONS (NOT CANONICAL)

Files under candidates/ are proposals under review. The canonical instruments are the files
under prompts/. Nothing here is embedded in webapp/provenance.html, pinned by the Atlas
baseline, or used by any committed receipt.

A candidate becomes canonical for a new method version only through an explicit, reviewed
adoption by the repository owner. Passing its own tests is not adoption. No candidate judges
outputs produced under an earlier version: a candidate's checker reports NOT_APPLICABLE for
them.

research-analysis/
  2-citation-network.v2-candidate.txt          proposed v2 of the citation-network instrument
                                               (FAIL-CN-007), revision 2 (v2-candidate.2,
                                               class map cn7-map-2). Built from the canonical v1 file
                                               by make_v2_candidate.py; every change is one
                                               named, single-occurrence edit there.
  2-citation-network.v2-candidate.CHANGES.txt  rule records: requirement, origin, inherited
                                               vs changed, enforcement, acceptance case, test
                                               receipt, open conflicts; promotion criteria.
  check-citation-network-v2-gates.py           candidate checker for the new Sections A0 and
                                               K0. Run it in addition to the v1 checker.
  make_v2_candidate.py                         reproducible build of the candidate from v1.

Tests: tests/test-citation-network-v2-gates.py; rule ablation: tests/ablate-citation-network-v2-gates.py;
fixtures in tests/cases/citation-network-v2-gates/.
