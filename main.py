from fastapi import FastAPI, HTTPException
import requests
from db import favorites_collection


app = FastAPI()


@app.get("/")
def get_home():
    return {"Message": "Welcome to the countries explorer api"}


@app.get("/countries/{name}")
def get_country_by_name(name: str):
    countries_link = f"https://restcountries.com/v3.1/name/{name}"
    response = requests.get(countries_link)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Country not found")

    data = response.json()[0]  # take the first match
    country_info = {
        "name": data["name"]["common"],
        "capital": data.get("capital", ["N/A"])[0],
        "population": data.get("population", "N/A"),
        "region": data.get("region", "N/A"),
    }
    return country_info
