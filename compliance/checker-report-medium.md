Exit code: 0

Checked: /mnt/data/citation_network_pilot_02/citation-network-compliance-pilot-02-audit.txt
Required headings: 25
Present: 25
Missing: 0
Placeholder-screen threshold: 12 words
NOTICE	A body-length pass means only that the section is not empty or an obvious placeholder. It does not establish analytical adequacy.
ORDER_PASS	ARTIFACT 9: NETWORK MAP precedes COMPLETION LEDGER
ORDER_PASS	COMPLETION LEDGER precedes ARTIFACT 10: FINAL VERDICT
ORDER_PASS	ARTIFACT 10: FINAL VERDICT precedes FINAL SECTION: STANDARDIZED FINDING TABLE
PLACEHOLDER_SCREEN_PASS	PRE-AUDIT CLAIM CONFIRMATION	109 words	status=COMPLETED_INFERRED
PLACEHOLDER_SCREEN_PASS	SECTION A: CITATION NETWORK STRUCTURE AND CARTEL DETECTION	218 words	status=COMPLETED_INFERRED
PLACEHOLDER_SCREEN_PASS	SECTION B: EVIDENCE TYPE CODING	152 words	status=COMPLETED_INFERRED
PLACEHOLDER_SCREEN_PASS	SECTION C: CITATION POLARITY AND CLAIM USE	160 words	status=COMPLETED_INFERRED
PLACEHOLDER_SCREEN_PASS	SECTION D: CLAIM MUTATION TRACKING	145 words	status=COMPLETED_INFERRED
PLACEHOLDER_SCREEN_PASS	SECTION E: ADJACENT FIELD ENGAGEMENT / NEGLECT	117 words	status=COMPLETED_INFERRED
PLACEHOLDER_SCREEN_PASS	SECTION F: HUB DEPENDENCY AND REVIEW-PAPER LAUNDERING	154 words	status=COMPLETED_INFERRED
PLACEHOLDER_SCREEN_PASS	SECTION G: PATTERN RECOGNITION AND RATCHET BEHAVIOR	124 words	status=COMPLETED_INFERRED
PLACEHOLDER_SCREEN_PASS	SECTION H: IGNORED CRITIQUE AND NON-UPTAKE	112 words	status=COMPLETED_INFERRED
PLACEHOLDER_SCREEN_PASS	SECTION I: AUTHOR, INSTITUTION, JOURNAL, AND FUNDING CLUSTERING	132 words	status=COMPLETED_INFERRED
PLACEHOLDER_SCREEN_PASS	SECTION J: FALSE-POSITIVE AND BASELINE CHECK	162 words	status=COMPLETED_INFERRED
PLACEHOLDER_SCREEN_PASS	SECTION J2: THE CONCEDE TEST	177 words	status=COMPLETED_INFERRED
PLACEHOLDER_SCREEN_PASS	SECTION K: CARTEL-RISK SCORING	90 words	status=COMPLETED_INFERRED
PLACEHOLDER_SCREEN_PASS	ARTIFACT 1: TOP 15 CITATION SPINE TABLE	265 words	status=COMPLETED_INFERRED
PLACEHOLDER_SCREEN_PASS	ARTIFACT 2: FOUNDING CLUSTER TABLE	94 words	status=COMPLETED_INFERRED
PLACEHOLDER_SCREEN_PASS	ARTIFACT 3: RECENT 5-YEAR CITATION BEHAVIOR TABLE	116 words	status=COMPLETED_INFERRED
PLACEHOLDER_SCREEN_PASS	ARTIFACT 4: CITATION POLARITY TABLE	111 words	status=COMPLETED_INFERRED
PLACEHOLDER_SCREEN_PASS	ARTIFACT 5: CLAIM MUTATION TABLE	108 words	status=COMPLETED_INFERRED
PLACEHOLDER_SCREEN_PASS	ARTIFACT 6: ADJACENT-LITERATURE NEGLECT TABLE	91 words	status=COMPLETED_INFERRED
PLACEHOLDER_SCREEN_PASS	ARTIFACT 7: CRITIQUE-UPTAKE TABLE	106 words	status=COMPLETED_INFERRED
PLACEHOLDER_SCREEN_PASS	ARTIFACT 8: CARTEL-RISK SCORECARD	146 words	status=COMPLETED_INFERRED
PLACEHOLDER_SCREEN_PASS	ARTIFACT 9: NETWORK MAP	162 words	status=COMPLETED_INFERRED
PLACEHOLDER_SCREEN_PASS	COMPLETION LEDGER	399 words	status=N/A
PLACEHOLDER_SCREEN_PASS	ARTIFACT 10: FINAL VERDICT	257 words	status=COMPLETED_INFERRED
PLACEHOLDER_SCREEN_PASS	FINAL SECTION: STANDARDIZED FINDING TABLE	444 words	status=N/A
STATUS_SUMMARY	N/A=2	PROVISIONAL=0	INCOMPLETE=0	COMPLETED_INFERRED=23	UNMARKED_THIN=0
MANUAL_REVIEW_REQUIRED	All present headings cleared the crude placeholder screen. Substantive adequacy is still unverified.
PASS	All required headings are unique standalone lines in the required order; Completion Ledger claims match actual presence; no silent omission was detected. Manual substantive review remains required.

STDERR
Spreadsheet runtime warmup failed during python startup
Traceback (most recent call last):
  File "/tmp/tmp.yTcnQsZYiA/artifact_tool_v2-2.8.4/artifact_tool/patches/warm_spreadsheet_runtime_on_startup.py", line 26, in warm_spreadsheet_runtime_on_startup
  File "/tmp/tmp.yTcnQsZYiA/artifact_tool_v2-2.8.4/artifact_tool/spreadsheet_warmup.py", line 785, in warm_spreadsheet_runtime
  File "/tmp/tmp.yTcnQsZYiA/artifact_tool_v2-2.8.4/artifact_tool/spreadsheet_warmup.py", line 720, in _warm_feature_flows
  File "/tmp/tmp.yTcnQsZYiA/artifact_tool_v2-2.8.4/artifact_tool/spreadsheet_warmup.py", line 704, in _warm_collaboration_flows
  File "/tmp/tmp.yTcnQsZYiA/artifact_tool_v2-2.8.4/artifact_tool/generated/interface/models.py", line 30820, in hydrate_crdt_from_proto
  File "/tmp/tmp.yTcnQsZYiA/artifact_tool_v2-2.8.4/artifact_tool/rpc/remote.py", line 749, in __call__
  File "/tmp/tmp.yTcnQsZYiA/artifact_tool_v2-2.8.4/artifact_tool/rpc/client.py", line 150, in call
artifact_tool.rpc.client.RemoteError: hydrateCrdtFromProto requires an empty collaborative document.
