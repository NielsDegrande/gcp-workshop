# -*- coding: utf-8 -*-

"""REST API for GCP Workshop."""

from datetime import datetime
from pathlib import Path

import pandas as pd
import uvicorn
import xgboost as xgb
from fastapi import FastAPI
from pydantic import BaseModel, Field

from server.dao import Predictions, Session

# Create app.
app = FastAPI()

# Load model.
path_ = Path("model/my-xgb-model.model")
model = xgb.XGBRegressor()
model.load_model(path_)


class QuantityRequest(BaseModel):
    """ Payload to be send to request a price """

    year: int = Field(..., example=2020, ge=2021)
    dayofyear: int = Field(..., example=1, ge=1, le=366)
    store_id: int = Field(..., example=1)
    product_id: int = Field(..., example=1)


@app.post("/quantity")
async def quantify(request: QuantityRequest) -> dict:
    """Quantify a product for a given store and day.

    :return: JSON object holding a quantity
    """
    features = pd.DataFrame.from_dict(
        {
            "year_": [request.year] * 2,
            "dayofyear_": [request.dayofyear] * 2,
            "store_id": [request.store_id] * 2,
            "product_id": [request.product_id] * 2,
            # Quantify for both member and non-member.
            "customer": [0, 1],
        }
    )
    results = round(sum(model.predict(features)))

    with Session() as session:
        session.add(
            Predictions(
                request_time=datetime.now(), request=str(request), quantity=results
            )
        )

    return {"quantity": results}


def main():
    """Start the server."""
    uvicorn.run("server.__main__:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
