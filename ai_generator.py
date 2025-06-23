import requests
import os

HF_TOKEN = os.getenv("HF_TOKEN")

def generate_mcq(subject, language):
    if language == "Hindi":
        prompt = f"{subject} विषय पर एक हिंदी MCQ बनाइए जिसमें 4 विकल्प हों, उत्तर का index (0-3) और explanation हो।"
    else:
        prompt = f"Create one English MCQ for the subject {subject} with 4 options, correct answer index (0-3), and explanation."

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }

    data = {
        "inputs": prompt
    }

    response = requests.post(
        "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1",
        headers=headers,
        json=data
    )

    try:
        return response.json()[0]["generated_text"]
    except Exception:
        return None
