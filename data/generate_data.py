# -*- coding: utf-8 -*-

"""Generate retail data."""

import os
from datetime import date, timedelta
from random import sample

import numpy as np
import pandas as pd

# Parameters.
AVERAGE_STORE_GROWTH_RATE = 0.02
BETA_FOR_QUANTITY_EXPONENTIAL = 2
NUMBER_OF_PRODUCTS = 200
NUMBER_OF_STORES = 50
NUMBER_OF_YEARS = 3
PROBABILITY_IS_MEMBER = 0.42
SALES_PER_STORE_PER_DAY = {"small": 5000, "medium": 10000, "large": 15000}
START_YEAR = 2017

# Columns.
CATEGORY = "category"
CUSTOMER = "customer"
DATE = "date"
GROWTH = "growth_rate"
MEMBER = "member"
PRICE = "unit_price"
PRODUCT = "product_id"
QUANTITY = "quantity"
STORE = "store_id"
STORE_TYPE = "store_type"

# Constants.
DAYS_IN_YEAR = 365
INPUT_DATA_PATH = "data/input/supermarket_sales.csv"
OUTPUT_DATA_PATH = "data/output"

# Read data.
df = pd.read_csv(INPUT_DATA_PATH)

# Preprocess data.
COLUMNS_TO_KEEP = {
    "Product line": CATEGORY,
    "Unit price": PRICE,
}
df_filtered = df[COLUMNS_TO_KEEP]
df_renamed = df_filtered.rename(columns=COLUMNS_TO_KEEP)

# Generate dimensions.
PRICES = df_renamed[PRICE].unique()
PRODUCT_CATEGORIES = list(df_renamed[CATEGORY].unique())
PRODUCT_CATEGORIES.append("Fresh food")
PRODUCTS = []
for category in PRODUCT_CATEGORIES:
    for i in range(NUMBER_OF_PRODUCTS):
        PRODUCTS.append(
            {PRODUCT: i, CATEGORY: category, PRICE: sample(list(PRICES), 1)[0]}
        )
STORES = []
for i in range(NUMBER_OF_STORES):
    STORES.append(
        {
            STORE: i,
            STORE_TYPE: sample(list(SALES_PER_STORE_PER_DAY), 1)[0],
            GROWTH: np.random.normal(
                loc=AVERAGE_STORE_GROWTH_RATE, scale=AVERAGE_STORE_GROWTH_RATE, size=1
            )[0],
        }
    )

# Year 1.
SALES = []
for date_ in (date(START_YEAR, 1, 1) + timedelta(n) for n in range(DAYS_IN_YEAR)):
    print(date_)
    for store in STORES:
        daily_sales = SALES_PER_STORE_PER_DAY[store[STORE_TYPE]]
        product_sales = max(
            round(daily_sales / (len(PRODUCTS)) * np.random.normal(1, 0.2, 1)[0]), 1
        )
        for product in PRODUCTS:
            SALES.extend(
                [
                    (
                        date_,
                        store[STORE],
                        product[CATEGORY],
                        product[PRODUCT],
                        product[PRICE],
                    )
                ]
                * product_sales
            )

# Turn into DF.
COLUMNS = [
    DATE,
    STORE,
    CATEGORY,
    PRODUCT,
    PRICE,
]
year1 = pd.DataFrame.from_records(SALES, columns=COLUMNS)

# Add stochastic fields.
year1[QUANTITY] = np.random.exponential(
    scale=BETA_FOR_QUANTITY_EXPONENTIAL, size=year1.shape[0]
)
year1[QUANTITY] = year1[QUANTITY].round(decimals=0)
year1.loc[year1[QUANTITY] < 1, QUANTITY] = 1
year1[CUSTOMER] = np.random.binomial(n=1, p=PROBABILITY_IS_MEMBER, size=year1.shape[0])

# Write year 1.
os.makedirs(f"{OUTPUT_DATA_PATH}", exist_ok=True)
year1.to_parquet(f"{OUTPUT_DATA_PATH}/year={START_YEAR}.parquet", index=False)

# Generate next years.
for i in range(1, NUMBER_OF_YEARS + 1):
    year = START_YEAR + i
    SALES = []
    for date_ in (date(year, 1, 1) + timedelta(n) for n in range(DAYS_IN_YEAR)):
        print(date_)
        for store in STORES:
            compounded_growth_rate = (1 + store[GROWTH]) ** i - 1
            daily_sales = (
                SALES_PER_STORE_PER_DAY[store[STORE_TYPE]] * compounded_growth_rate
            )
            product_sales = max(
                round(daily_sales / (len(PRODUCTS)) * np.random.normal(1, 0.2, 1)[0]), 1
            )
            for product in PRODUCTS:
                SALES.extend(
                    [
                        (
                            date_,
                            store[STORE],
                            product[CATEGORY],
                            product[PRODUCT],
                            product[PRICE],
                        )
                    ]
                    * product_sales
                )

    # Write to disk.
    this_year = pd.DataFrame.from_records(SALES, columns=COLUMNS)
    this_year[QUANTITY] = np.random.exponential(
        scale=BETA_FOR_QUANTITY_EXPONENTIAL, size=this_year.shape[0]
    )
    this_year[QUANTITY] = this_year[QUANTITY].round(decimals=0)
    this_year.loc[this_year[QUANTITY] < 1, QUANTITY] = 1
    this_year[CUSTOMER] = np.random.binomial(
        n=1, p=PROBABILITY_IS_MEMBER, size=this_year.shape[0]
    )
    next_year = year1.copy()
    next_year[DATE] = next_year.date + timedelta(days=365 * i)
    next_year = next_year.append(this_year)
    os.makedirs(f"{OUTPUT_DATA_PATH}", exist_ok=True)
    next_year.to_parquet(f"{OUTPUT_DATA_PATH}/year={year}.parquet", index=False)
