# Verification record

Prepared October 9, 2026, using Python 3.12 on Linux with CPU inference.

## Passed checks

- `python -m unittest -v`: 6 tests passed.
- `python -m compileall -q .`: all Python files compiled.
- `python -m pip check`: no broken requirements found.
- `python smoke_test.py`: actual Qwen weights downloaded and loaded; a question
  and context-dependent follow-up generated nonempty responses, exit code 0.
- `build_app()`: Gradio interface constructed successfully.
- Gradio launch: local server started successfully. Requests made in the same
  execution environment to `/` and `/config` both returned HTTP 200. Configuration
  title was `AI & HCI Study Assistant`; server shut down cleanly after the check.

The final model test used the committed four-thread CPU setting and generation
parameters. A SOCKS proxy dependency found during testing was added to requirements.
The interface check used `NO_PROXY=127.0.0.1,localhost` and disabled Gradio analytics
for this environment. Typical laptops do not need those environment settings.

## Sample actual model output

Question: What is supervised learning? Give a short example.

Response excerpt: "Supervised learning is a type of machine learning where we train
a model on labeled data, meaning that each input has an associated output label."

The model continued with a cat/dog image classification example. A follow-up asking
for a business example produced a retail customer-review example.

## Limits of verification

The 192-token response limit truncated the end of the business example. Generated
text is not guaranteed correct. The response examples are not evidence of a formal
usability study. Keyboard navigation, clear-chat behavior, visual accessibility,
and Windows/macOS execution require evaluation on the target laptop. No complete
browser interaction was performed; backend generation and HTTP startup were tested.
No laptop latency benchmark was recorded.

## GitHub submission status

Repository: https://github.com/varungoparapu1994-alt/llm-education-chatbot

The repository was created as private. Instructor access remains pending until
an invitation is sent to the instructor's verified GitHub username and accepted.
The ZIP alone does not fulfill the repository-access requirement.
