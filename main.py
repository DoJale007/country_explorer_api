from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel
from util import replace_mongo_id
from db import favorites_collection

app = FastAPI()


class CountryModel(BaseModel):
    name: str
    user_notes: str


@app.get("/")
def get_home():
    return {"Message": "Welcome to the countries explorer api"}


@app.get("/countries/{name}")
def get_country_by_name(name: str):
    countries_link = f"https://restcountries.com/v3.1/name/{name}"
    response = requests.get(countries_link)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Country not found")

    data = response.json()[0]  # returns the first match from the ext. api
    country_info = {
        "name": data["name"]["common"],
        "capital": data.get("capital", ["N/A"])[0],
        "population": data.get("population", "N/A"),
        "region": data.get("region", "N/A"),
    }
    return country_info


@app.post("/countries/favorites")
def save_favorite_country(country: CountryModel):
    country_link = f"https://restcountries.com/v3.1/name/{country.name}"
    response = requests.get(country_link)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Country not found")
    data = response.json()[0]
    country_info = {
        "name": data["name"]["common"],
        "capital": data.get("capital", ["N/A"])[0],
        "population": data.get("population", "N/A"),
        "region": data.get("region", "N/A"),
        "user_notes": country.user_notes,
    }

    existing_country = favorites_collection.find_one({"name": country_info["name"]})
    if existing_country:
        raise HTTPException(
            status_code=409, detail=f"{country_info["name"]} is already a favorite"
        )

    favorites_collection.insert_one(country_info)
    return {"Message": f"{country_info["name"]} saved to favorites!"}


@app.get("/favorites")
def get_all_favorites():
    favorite_countries = favorites_collection.find()
    favorites_list = list(favorite_countries)
    return {"data": list(map(replace_mongo_id, favorites_list))}
