"""Local educational Qwen chatbot; no external inference service."""
import threading

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"
MAX_CHARS = 2000
MAX_HISTORY = 6
SYSTEM_PROMPT = (
    "You are a friendly study assistant for introductory AI and human-computer "
    "interaction. Explain concepts clearly with short practical examples. "
    "Ask a clarifying question when a request is ambiguous. Admit uncertainty. "
    "Do not invent university policies or citations. Encourage learning rather "
    "than completing graded assignments for the student."
)


def prepare_messages(message, history):
    """Validate input and retain only recent complete conversational turns."""
    if not isinstance(message, str) or not message.strip():
        raise ValueError("Please enter a question.")
    message = message.strip()
    if len(message) > MAX_CHARS:
        raise ValueError(f"Please limit your question to {MAX_CHARS} characters.")
    valid = []
    for item in history or []:
        if (isinstance(item, dict) and item.get("role") in ("user", "assistant")
                and isinstance(item.get("content"), str)):
            valid.append({"role": item["role"], "content": item["content"][:MAX_CHARS]})
    # Start with a user turn, and discard an incomplete final user turn.
    recent = valid[-2 * MAX_HISTORY:]
    while recent and recent[0]["role"] != "user":
        recent.pop(0)
    if recent and recent[-1]["role"] == "user":
        recent.pop()
    return [{"role": "system", "content": SYSTEM_PROMPT}, *recent,
            {"role": "user", "content": message}]


class Chatbot:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.lock = threading.Lock()

    def _load(self):
        if self.model is not None:
            return
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        # Excessive CPU threads can slow down small-model token generation.
        torch.set_num_threads(4)
        tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID, dtype=torch.float32, use_safetensors=True,
        )
        model.eval()
        self.tokenizer, self.model = tokenizer, model

    def reply(self, message, history):
        messages = prepare_messages(message, history)
        with self.lock:
            self._load()
            import torch
            # Budget the actual tokens without cutting the system instruction.
            while True:
                prompt = self.tokenizer.apply_chat_template(
                    messages, tokenize=False, add_generation_prompt=True,
                )
                inputs = self.tokenizer(prompt, return_tensors="pt")
                if inputs["input_ids"].shape[1] <= 4096:
                    break
                if len(messages) <= 2:
                    raise ValueError("Question exceeds the token limit; please shorten it.")
                del messages[1:3]
            with torch.inference_mode():
                output = self.model.generate(
                    **inputs, max_new_tokens=192, do_sample=False,
                    temperature=None, top_p=None, top_k=None,
                    pad_token_id=self.tokenizer.eos_token_id,
                )
            answer = self.tokenizer.decode(
                output[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True,
            ).strip()
            if not answer:
                raise RuntimeError("The model returned no text. Please rephrase your question.")
            return answer
