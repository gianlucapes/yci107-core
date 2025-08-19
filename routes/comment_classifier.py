from fastapi import APIRouter
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from models.comment_labels import CommentLabel

router = APIRouter(prefix="/comments", tags=["comments"])

model_name = "yurmin/yc107-comment-classifier"

# Carica direttamente dal Hub
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)


@router.get("/classify")
def classification_comment(comments: list[str]):
    lables = {
        0: CommentLabel.Neutrale,
        1: CommentLabel.Positiva,
        2: CommentLabel.Negativo,
        3: CommentLabel.Discriminatorio,
        4: CommentLabel.Complottismo,
        5: CommentLabel.Allarmismo,
        6: CommentLabel.Disinformazione,
        7: CommentLabel.Estremismi_ideologici
    }

    inputs = tokenizer(comments, padding=True, truncation=True, return_tensors="pt")
    outputs = model(**inputs)
    predictions = outputs.logits.argmax(dim=-1)
    pred_labels = [lables[i.item()] for i in predictions]

    return pred_labels
