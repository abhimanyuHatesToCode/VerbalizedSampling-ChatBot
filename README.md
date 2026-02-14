# VerbalizedSampling-ChatBot

Recently experimented with integrating Verbalized Sampling into a multi-mode LLM interface, and moreover added a little twist to it.

So the idea is instead of generating a single response, the system produces multiple candidate outputs, evaluates them, and selects the strongest one, according to their probability. This approach forces the LLM to generate creative, diverse and unpredictable responses.

The result was noticeably higher response diversity (close to 2× in practical testing) and reduced repetitive patterns — a small but meaningful step toward mitigating early-stage mode collapse.

Built with FastAPI + Gemini + Streamlit, featuring:
* Session-based conversational memory
* Mode-aware behavioral toggles (normal 😊/ reasoning 🤯/ valentine 💝)
* Token-aware context trimming

Since it is Valentine's Day, so couldn't stop myself from adding an intriguing Valentine'S Mode, that prompts a distinct shift in the personality.

I also explored behavioral UX signaling:

* 💙 Aqua glow → Reasoning mode (structured multi-candidate sampling)
* 💘 Pink glow → Valentine mode (stylistic personality shift)
* 😊 Neutral → Standard conversational mode

The glow isn’t decorative — it visually communicates which behavioral mode generated the response, making experimentation transparent and intuitive.

Key takeaway: improving LLM behavior isn’t always about changing the model — sometimes it’s about changing how we sample and structure its reasoning.

