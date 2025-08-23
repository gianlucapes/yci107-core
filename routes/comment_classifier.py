from fastapi import APIRouter
import requests
from typing import List
from config import settings
from models.comment_labels import CommentLabel

router = APIRouter(prefix="/comments", tags=["comments"])

model_name = "yurmin/yc107-comment-classifier"
API_URL = f"https://api-inference.huggingface.co/models/{model_name}"

headers = {
    "Authorization": f"Bearer {settings.HF_TOKEN}"
}

labels = {
    0: CommentLabel.Neutrale,
    1: CommentLabel.Positiva,
    2: CommentLabel.Negativo,
    3: CommentLabel.Discriminatorio,
    4: CommentLabel.Complottismo,
    5: CommentLabel.Allarmismo,
    6: CommentLabel.Disinformazione,
    7: CommentLabel.Estremismi_ideologici
}

@router.post("/classify")
def classify_comments(comments: List[str]) -> List[str]:
    payload = {"inputs": comments}  # invia in batch
    results = []
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        api_result = response.json()
        
        # api_result sarà una lista di liste (uno per ogni commento)
        for comment_result in api_result:
            if isinstance(comment_result, list) and len(comment_result) > 0:
                best_pred = max(comment_result, key=lambda x: x["score"])
                label_index = int(best_pred["label"].split("_")[1])
                predicted_label = labels.get(label_index, CommentLabel.Neutrale)
                results.append(predicted_label.value)
            else:
                results.append(CommentLabel.Neutrale.value)
                
    except Exception as e:
        print(f"Errore API Hugging Face: {e}")
        results = [CommentLabel.Neutrale.value] * len(comments)
    
    return results
