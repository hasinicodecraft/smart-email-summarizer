import gradio as gr
from summarizer import (
    summarize_email,
    extract_keywords,
    detect_sentiment,
    detect_action_items
)

def analyze_email(email_text):
    if not email_text.strip():
        return "Please paste an email.", "", "", ""
    summary   = summarize_email(email_text)
    keywords  = ", ".join(extract_keywords(email_text))
    sentiment = detect_sentiment(email_text)
    actions   = detect_action_items(email_text)
    return summary, keywords, sentiment, actions


css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

body, .gradio-container {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e) !important;
    min-height: 100vh;
}

.main-title {
    text-align: center;
    padding: 30px 0 10px 0;
}

.main-title h1 {
    font-size: 2.8em;
    font-weight: 700;
    background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
}

.main-title p {
    color: #94a3b8;
    font-size: 1.1em;
}

.input-card {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(167,139,250,0.3) !important;
    border-radius: 16px !important;
    padding: 20px !important;
    backdrop-filter: blur(10px);
}

.output-card {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(96,165,250,0.3) !important;
    border-radius: 16px !important;
    padding: 16px !important;
    backdrop-filter: blur(10px);
}

label span {
    color: #a78bfa !important;
    font-weight: 600 !important;
    font-size: 0.95em !important;
    letter-spacing: 0.5px;
}

textarea, input {
    background: rgba(15,12,41,0.6) !important;
    border: 1px solid rgba(167,139,250,0.2) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-size: 0.95em !important;
}

textarea:focus {
    border-color: #a78bfa !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,0.15) !important;
}

.analyze-btn {
    background: linear-gradient(90deg, #a78bfa, #60a5fa) !important;
    border: none !important;
    border-radius: 12px !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 1.1em !important;
    padding: 14px !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
    letter-spacing: 0.5px;
}

.analyze-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(167,139,250,0.4) !important;
}

.section-label {
    color: #60a5fa !important;
    font-weight: 700 !important;
    font-size: 0.8em !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    margin-bottom: 12px !important;
}

footer { display: none !important; }
"""

with gr.Blocks(title="Smart Email Summarizer") as app:

    gr.HTML("""
        <div class="main-title">
            <h1>✉️ Smart Email Summarizer</h1>
            <p>Powered by BART · DistilBERT · KeyBERT — Turn long emails into instant insights</p>
        </div>
    """)

    with gr.Row():
        with gr.Column(scale=1):
            gr.HTML('<p class="section-label">📩 Input</p>')
            email_input = gr.Textbox(
                label="Paste Your Email Here",
                placeholder="Paste a long email or article and click Analyze...",
                lines=14,
                elem_classes="input-card"
            )
            analyze_btn = gr.Button(
                "🚀 Analyze Email",
                elem_classes="analyze-btn"
            )

        with gr.Column(scale=1):
            gr.HTML('<p class="section-label">📊 Results</p>')
            summary_out = gr.Textbox(
                label="📝 Summary",
                lines=5,
                elem_classes="output-card"
            )
            with gr.Row():
                keywords_out = gr.Textbox(
                    label="🔑 Keywords",
                    lines=2,
                    elem_classes="output-card"
                )
                sentiment_out = gr.Textbox(
                    label="💬 Sentiment",
                    lines=2,
                    elem_classes="output-card"
                )
            actions_out = gr.Textbox(
                label="✅ Action Items",
                lines=4,
                elem_classes="output-card"
            )

    analyze_btn.click(
        fn=analyze_email,
        inputs=[email_input],
        outputs=[summary_out, keywords_out, sentiment_out, actions_out]
    )

app.launch(css=css)