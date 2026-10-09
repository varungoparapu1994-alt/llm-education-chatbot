"""Run with python app.py; open http://127.0.0.1:7860."""
from chatbot import Chatbot


def build_app():
    import gradio as gr
    bot = Chatbot()

    def respond(message, history):
        try:
            return bot.reply(message, history)
        except ValueError as error:
            raise gr.Error(str(error)) from error
        except Exception as error:
            # Do not show raw paths or private prompt data in the browser.
            raise gr.Error(
                "The model could not complete the request. Check the model download, "
                "available memory, and installed dependencies, then try again."
            ) from error

    with gr.Blocks(title="AI & HCI Study Assistant") as demo:
        gr.Markdown(
            "# AI & HCI Study Assistant\n"
            "Ask about introductory AI and human-computer interaction. "
            "Answers are AI-generated and may be inaccurate; verify with course materials.\n\n"
            "**First response:** downloads the free Qwen model (about 1 GB); "
            "later responses run locally on the CPU. Avoid entering personal information. "
            "Use the trash icon to clear the conversation."
        )
        gr.ChatInterface(
            fn=respond, type="messages",
            chatbot=gr.Chatbot(type="messages", label="Conversation", height=420),
            textbox=gr.Textbox(placeholder="Ask a question…", label="Your question", max_lines=6),
            examples=["Explain supervised and unsupervised learning with an example.",
                      "What makes a chatbot interface easy to use?",
                      "How are adaptive interfaces different from static interfaces?"],
        )
    return demo.queue(default_concurrency_limit=1)


if __name__ == "__main__":
    build_app().launch(server_name="127.0.0.1", server_port=7860, share=False)
