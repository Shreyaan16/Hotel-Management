import numpy as np
import pandas as pd
import joblib
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from configuration.paths_config import (MODEL_OUTPUT_PATH, LABEL_ENCODER_PATH, SKEWED_COLUMNS_PATH, FEATURE_COLUMNS_PATH)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

model = joblib.load(MODEL_OUTPUT_PATH)
label_encoders = joblib.load(LABEL_ENCODER_PATH)
skewed_columns = joblib.load(SKEWED_COLUMNS_PATH)
feature_columns = joblib.load(FEATURE_COLUMNS_PATH)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "prediction": None})


@app.post("/", response_class=HTMLResponse)
async def predict(
    request: Request,
    lead_time: int = Form(...),
    no_of_special_request: int = Form(...),
    avg_price_per_room: float = Form(...),
    arrival_year: int = Form(...),
    arrival_month: int = Form(...),
    arrival_date: int = Form(...),
    market_segment_type: str = Form(...),
    no_of_week_nights: int = Form(...),
    no_of_weekend_nights: int = Form(...),
    type_of_meal_plan: str = Form(...),
    room_type_reserved: str = Form(...),
):
    input_data = {
        "lead_time": lead_time,
        "no_of_special_requests": no_of_special_request,
        "avg_price_per_room": avg_price_per_room,
        "arrival_year": arrival_year,
        "arrival_month": arrival_month,
        "arrival_date": arrival_date,
        "market_segment_type": market_segment_type,
        "no_of_week_nights": no_of_week_nights,
        "no_of_weekend_nights": no_of_weekend_nights,
        "type_of_meal_plan": type_of_meal_plan,
        "room_type_reserved": room_type_reserved,
    }

    # Apply label encoding to categorical columns
    cat_cols = ["type_of_meal_plan", "room_type_reserved", "market_segment_type", "arrival_year", "arrival_month"]
    for col in cat_cols:
        if col in label_encoders and col in input_data:
            le = label_encoders[col]
            input_data[col] = int(le.transform([input_data[col]])[0])

    # Apply log1p to skewed numerical columns
    for col in skewed_columns:
        if col in input_data:
            input_data[col] = np.log1p(input_data[col])

    # Build DataFrame with the exact column order the model was trained on
    df = pd.DataFrame([input_data])
    df = df.reindex(columns=feature_columns, fill_value=0)

    prediction = int(model.predict(df)[0])

    return templates.TemplateResponse("index.html", {"request": request, "prediction": prediction})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
