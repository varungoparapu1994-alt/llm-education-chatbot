"""Real-model test. Requires dependencies and first-run internet access."""
from chatbot import Chatbot

if __name__ == "__main__":
    bot = Chatbot()
    question = "What is supervised learning? Give a short example."
    answer = bot.reply(question, [])
    print("USER:", question)
    print("ASSISTANT:", answer)
    assert answer.strip(), "No response generated"
    followup = bot.reply("Give a business example.", [
        {"role": "user", "content": question},
        {"role": "assistant", "content": answer},
    ])
    print("FOLLOW-UP:", followup)
    assert followup.strip(), "No follow-up generated"
    print("PASS: real model generated two nonempty responses.")
