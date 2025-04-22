from fastapi import FastAPI
from pydantic import BaseModel
from models import predict_category
from pii_masker import PIIMasker

app = FastAPI()
masker = PIIMasker()

class EmailRequest(BaseModel):
    email_body: str

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

@app.post("/classify-email")
async def classify_email(request: EmailRequest):
    original_email = request.email_body

    masked_email, entities = masker.mask(original_email)
    category, confidence = predict_category(original_email)
    token_count = len(original_email.split())

    return {
        "input_email_body": original_email,
        "list_of_masked_entities": entities,
        "masked_email": masked_email,
        "category_of_the_email": category,
        "category_confidence": confidence,
        "token_count": token_count,
        "model_type": "logistic"
    }
