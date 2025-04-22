import gradio as gr
from models import predict_category
from pii_masker import PIIMasker

def process_email(email_text):
    category, confidence = predict_category(email_text)
    masker = PIIMasker()
    masked_email, entities = masker.mask(email_text)
    return masked_email, str(entities), f"{category} ({confidence*100:.2f}%)"

iface = gr.Interface(
    fn=process_email,
    inputs=gr.Textbox(lines=10, placeholder="Enter email text here..."),
    outputs=[
        gr.Textbox(label="Masked Email"),
        gr.Textbox(label="Detected Entities"),
        gr.Textbox(label="Predicted Category")
    ],
    title="Email PII Masker and Classifier",
    description="Enter an email to mask PII and predict its category."
)

if __name__ == "__main__":
    iface.launch()
