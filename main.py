from fastapi import FastAPI
from routes.comment_classifier import router as comment_classifier_router

# inizializza l'app
app = FastAPI()

app.include_router(comment_classifier_router)