# Test Cases

## Failure-response rule

A failing run does not automatically prove the prompt is wrong.

Before patching a prompt:

1. inspect the case packet for unintended structural features;
2. verify the expected-result oracle against the packet;
3. check whether the run identified a genuine feature the designer failed to
   anticipate;
4. distinguish prompt failure, model failure, checker failure, and fixture failure.

If the case or oracle is wrong, repair the fixture rather than training the prompt
to ignore valid evidence.

## Paired citation-network correctness fixture

Cases 12 and 13 are paired substantive tests.

They hold surface cartel indicators broadly constant while reversing the
evidentiary path structure. They must be scored together; a default-acquit or
default-convict system fails the pair.
