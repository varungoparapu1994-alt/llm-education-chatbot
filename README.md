# AI & HCI Study Assistant

A local educational LLM chatbot implementing the accompanying design: Python,
Gradio, Transformers, PyTorch, and Qwen2.5-0.5B-Instruct. No OpenAI API,
paid inference, fine-tuning, or document retrieval is used.

## Setup and run

Use Python 3.11 or 3.12. Allow several GB of free disk and memory; an 8 GB RAM
laptop is a reasonable target, but hardware performance must be checked.
The model downloads from Hugging Face on the first question (about 1 GB).

```bash
python -m venv .venv
```

Activate the environment:

Windows PowerShell: `.venv\Scripts\Activate.ps1`

macOS/Linux: `source .venv/bin/activate`

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:7860. Ask a question, wait for the download/response,
then ask a follow-up. The trash icon clears the chat history. Stop with Ctrl+C.

For CPU-only PyTorch on Windows/Linux, you can first run:

```bash
python -m pip install torch==2.9.0 --index-url https://download.pytorch.org/whl/cpu
```

Then install requirements normally. After a successful model download, cached
weights support offline use; set `HF_HUB_OFFLINE=1` if you want to enforce it.
Do not commit downloaded weights, environment folders, tokens, or private chats.

## Verification

```bash
python -m unittest -v
python smoke_test.py
```

The unit tests cover empty and long input, prompt construction, history limits,
follow-up context, and history immutability. The smoke test uses the actual model
and verifies two nonempty answers. It does not prove factual accuracy.
See TEST_RESULTS.md for the checks actually performed during preparation.

## Architecture and scope

- `app.py`: browser interface, examples, progress feedback, and visible errors.
- `chatbot.py`: validation, bounded recent history, system prompt, lazy model
  loading, token budgeting, CPU inference, and response decoding.
- `test_chatbot.py`: standard-library logic tests.
- `smoke_test.py`: real-model question and follow-up.

Only recent conversation turns are passed to the model. Requests are serialized
to avoid overlapping CPU model generations. Greedy decoding and a 192-token
answer limit keep the prototype simple. Responses may be inaccurate or ignore
instructions. This app cannot access current policies or course documents.
Chats are not intentionally stored in an application database. The first model
download contacts Hugging Face; this is not a claim of absolute privacy.

## GitHub and instructor submission

Repository: https://github.com/varungoparapu1994-alt/llm-education-chatbot

The repository is private. Before submission, invite the instructor's verified
GitHub username through Settings → Collaborators → Add people and ensure the
invitation is accepted. The URL alone does not grant access.

Submit the repository URL and source ZIP in the assignment portal. Run both test
commands and a browser interaction on the target laptop before submission.
Record actual runtime, answer quality, and usability findings in the results paper.

## Credits and AI assistance

The project-specific code was generated with ChatGPT assistance. Review and
understand it, and disclose assistance according to your course policy. The model
loading/chat-template/decoding pattern follows the Qwen model card. The interface
uses the documented Gradio ChatInterface API. This implementation extends those
patterns with an educational system prompt, validation, bounded history and
token budget, a CPU execution path, error handling, and verification scripts.

- Qwen Team. Qwen2.5-0.5B-Instruct model card (Apache 2.0 model license):
  https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct
- Gradio ChatInterface documentation:
  https://www.gradio.app/docs/gradio/chatinterface
- Transformers documentation: https://huggingface.co/docs/transformers/index
- PyTorch documentation: https://pytorch.org/docs/stable/index.html

Third-party software and weights remain subject to their respective licenses.
