# Report-bug evals: speaker notes

Six slides for a technical audience, approximately 8–10 minutes including discussion. This final case study follows trigger testing, CI, Promptfoo evaluation techniques, and an introduction to scenarios, mocks, and sandboxes. It sits immediately before Questions. Start at `slides.html#/report-bug-contract`. Press **S** for the embedded speaker view when serving the deck over HTTP.

All results below come from stored upstream artifacts. No fresh eval run is represented. Source links pin the inspected repository snapshot. Baseline directory names identify separate stored runs.

## 1. Evaluating report-bug

We have introduced scenarios, mocks, and sandboxes. Now look at a concrete evaluation of report-bug and ask whether it follows its instructions. This is a useful example because the contract is concrete and we can inspect the result without understanding a new application.

The skill reads project configuration and a bug template, collects supplied facts, and composes a Jira bug. It must preserve the user's content, omit skipped optional sections, and obtain approval before creating the issue. Production output goes to Jira. The eval prompt changes that behavior: it requests a preview file and files describing the proposed create and comment calls, and forbids actual Jira or MCP calls.

That gives us inspectable artifacts. It also defines the boundary of this example: the files let us evaluate composition and proposed parameters. We will return to what they cannot prove. These are recorded repository artifacts, not a fresh run.

Sources: [report-bug/SKILL.md](https://github.com/RHEcosystemAppEng/sdlc-plugins/blob/3903a70384d095e54b4709e33c92d1658a5a69b5/plugins/sdlc-workflow/skills/report-bug/SKILL.md), [evals/report-bug/evals.json](https://github.com/RHEcosystemAppEng/sdlc-plugins/blob/3903a70384d095e54b4709e33c92d1658a5a69b5/evals/report-bug/evals.json). Source checkout: 3903a70384d095e54b4709e33c92d1658a5a69b5.

## 2. Case 2: skipped sections

Case 2 reports duplicate entries across pages in an SBOM list. The fixture supplies the required facts, including steps using at least 50 SBOMs and the RHTPA 1.3.0 environment on OpenShift 4.15. Root Cause and Suggested Fix each contain SKIP. The excerpt on the slide is exact.

The desired behavior is narrow: include the six required template headings and omit the two optional headings. The skill should not leave empty sections or invent a diagnosis. This makes a useful first execution eval because we can explain the input and expected behavior in under a minute.

Notice that the assertion concerns a heading. The output may still mention the words Root Cause in a note explaining which sections it skipped. A broad forbidden-string check would reject that valid output. We need the check to express the intended rule precisely. Next, look at how the repository packages this case.

Sources: [user-input-interactive-partial.md](https://github.com/RHEcosystemAppEng/sdlc-plugins/blob/3903a70384d095e54b4709e33c92d1658a5a69b5/evals/report-bug/files/user-input-interactive-partial.md), [bug-template.md](https://github.com/RHEcosystemAppEng/sdlc-plugins/blob/3903a70384d095e54b4709e33c92d1658a5a69b5/evals/report-bug/files/bug-template.md), [evals.json, case 2](https://github.com/RHEcosystemAppEng/sdlc-plugins/blob/3903a70384d095e54b4709e33c92d1658a5a69b5/evals/report-bug/evals.json). The case prompt says five required sections in one sentence. The template and assertions enumerate six, which this presentation follows.

## 3. Anatomy of an eval

An eval case combines a task prompt, input fixtures, and assertions about observable results. Here the configuration fixture supplies project TC and Bug type ID 10300. The template defines the section headings. The partial-input fixture supplies the user's report and the two SKIP choices.

The prompt also tells the agent to write preview.md, jira-create.md, and jira-comment.md under outputs instead of contacting Jira. The slide shortens that prompt and shows two of the ten assertions. The assertion strings themselves are exact. The expected_output field and the other assertions are omitted from this display.

The runner gives each execution a fresh subagent and explicitly requests the target Skill tool invocation. A separate model grades the resulting files. This tests the behavior of an invoked skill. Automatic skill selection needs its own trigger tests. Also, fresh context and instructions against external calls do not themselves enforce a sandbox. Next we can inspect an output and its grading evidence.

Sources: [evals.json, case 2](https://github.com/RHEcosystemAppEng/sdlc-plugins/blob/3903a70384d095e54b4709e33c92d1658a5a69b5/evals/report-bug/evals.json), [run-evals/SKILL.md, execution and grading instructions](https://github.com/RHEcosystemAppEng/sdlc-plugins/blob/3903a70384d095e54b4709e33c92d1658a5a69b5/plugins/sdlc-workflow/skills/run-evals/SKILL.md).

## 4. Output and grading evidence

The left side shows the six heading lines from the actual preview, with the report body removed for space. The right side reproduces one evidence string from grading.json, split over two lines for display. That assertion passed because the output contains the required Attachments heading.

The grader also passed the two omission checks. Its evidence explicitly distinguishes a section heading from the plain-text skipped-sections note. All ten assertions passed in this stored case. The runner asks a separate LLM grader to read every output file, use binary verdicts, cite concrete evidence, and fail on contradictory evidence.

Those rules make a verdict easier to audit, but we should still inspect the evidence. Heading presence is straightforward to check in code. A model is more useful for questions such as whether rephrasing preserves the user's facts. This repository currently uses the model grader for these assertions. The next slide shows a recorded failure that such a precise check caught.

Sources: [dada325a/eval-2/outputs/preview.md](https://github.com/RHEcosystemAppEng/sdlc-plugins/blob/3903a70384d095e54b4709e33c92d1658a5a69b5/evals/report-bug/baselines/dada325a/eval-2/outputs/preview.md), [dada325a/eval-2/grading.json](https://github.com/RHEcosystemAppEng/sdlc-plugins/blob/3903a70384d095e54b4709e33c92d1658a5a69b5/evals/report-bug/baselines/dada325a/eval-2/grading.json), [run-evals grading rules](https://github.com/RHEcosystemAppEng/sdlc-plugins/blob/3903a70384d095e54b4709e33c92d1658a5a69b5/plugins/sdlc-workflow/skills/run-evals/SKILL.md). dada325a identifies the stored baseline directory.

## 5. A recorded label failure

This is a different stored run and a different case: the complete interactive bug report in baseline 2bbadc8e. The report passed thirteen of fourteen assertions. The failing check required the label ai-generated-jira. The proposed Jira parameters instead contained reported-by-ai, as the output excerpt shows.

Both labels sound reasonable to a person skimming the report. Only one satisfies this skill's contract. That distinction matters wherever downstream filters or automation depend on an exact value. The assertion makes the requirement explicit, and the evidence points directly to the incorrect field.

We can say this stored eval detected a concrete contract violation. Comparing this snapshot with a later passing snapshot does not establish which change caused an improvement, and we have not reproduced the failure today. For the audience, ask which other exact metadata values their own skills must preserve. That leads naturally to deciding what a passing suite actually establishes.

Sources: [2bbadc8e/eval-1/outputs/jira-create.md, line 56](https://github.com/RHEcosystemAppEng/sdlc-plugins/blob/3903a70384d095e54b4709e33c92d1658a5a69b5/evals/report-bug/baselines/2bbadc8e/eval-1/outputs/jira-create.md), [2bbadc8e/eval-1/grading.json](https://github.com/RHEcosystemAppEng/sdlc-plugins/blob/3903a70384d095e54b4709e33c92d1658a5a69b5/evals/report-bug/baselines/2bbadc8e/eval-1/grading.json). The displayed label arrays and output excerpt preserve the recorded values. The verdict sentence summarizes the stored result.

## 6. What a pass establishes

The latest stored report-bug baseline in this checkout passes all 51 assertions across five cases: complete input, skipped optional sections, missing configuration, programmatic input, and adversarial input. That is useful coverage, but the number has a specific denominator: assertions in selected cases.

Most checks inspect structure or proposed metadata. They do not comprehensively verify preservation of source facts. Files describing Jira calls do not demonstrate a successful real API interaction. A preview file does not prove that approval preceded creation. Explicit invocation does not test automatic selection, and one recorded execution per case does not establish repeated-run reliability. The baseline is a stored result, not a comparison against an agent without the skill.

My proposed extension keeps this example small: use code for exact headings and labels, then add a judge rubric for factual fidelity. A useful audience discussion is which missing behavior deserves the next case. Approval sequencing would require a tool trace or controlled integration test with a simulated approval exchange.

Sources: [five cases and 51 assertions](https://github.com/RHEcosystemAppEng/sdlc-plugins/blob/3903a70384d095e54b4709e33c92d1658a5a69b5/evals/report-bug/evals.json), [stored baseline dada325a](https://github.com/RHEcosystemAppEng/sdlc-plugins/tree/3903a70384d095e54b4709e33c92d1658a5a69b5/evals/report-bug/baselines/dada325a), [execution and grading workflow](https://github.com/RHEcosystemAppEng/sdlc-plugins/blob/3903a70384d095e54b4709e33c92d1658a5a69b5/plugins/sdlc-workflow/skills/run-evals/SKILL.md). The code checks and factual-fidelity rubric are proposals, not claims about the upstream implementation.
