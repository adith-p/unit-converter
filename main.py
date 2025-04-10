from enum import Enum

from fastapi import FastAPI, HTTPException

from pydantic import BaseModel
from typing import Literal


app = FastAPI()


class WeightEnum(str, Enum):
    milligram = "mili"
    gram = "gram"
    kilogram = "kg"
    ounce = "ounce"
    pound = "pound"


from enum import Enum


class LengthEnum(str, Enum):
    millimeter = "millimeter"
    centimeter = "centimeter"
    meter = "meter"
    inch = "inch"
    foot = "foot"
    yard = "yard"
    mile = "mile"


class Req(BaseModel):
    message: str


class temp(BaseModel):
    temp: float
    convert_from: Literal["celsius", "fahrenheit", "kelvin"]
    convert_to: Literal["celsius", "fahrenheit", "kelvin"]


class weight(BaseModel):
    weight: float
    convert_from: WeightEnum
    convert_to: WeightEnum


class length(BaseModel):
    length: float
    convert_from: LengthEnum
    convert_to: LengthEnum


@app.post("/data")
async def calculate(data: Req):
    print(data)
    return {"message": "post method"}


@app.get("/")
async def hello():
    return {"message": "hello world"}


# temprature converting


def convert_temp(from_temp: str, to_temp: str, temp: float):
    to_celsius = {
        "celsius": lambda t: t,
        "fahrenheit": lambda t: (t - 32) * 5 / 9,
        "kelvin": lambda t: t - 273.15,
    }
    from_celsius = {
        "celsius": lambda t: t,
        "fahrenheit": lambda t: (t * 9 / 5) + 32,
        "kelvin": lambda t: t + 273.15,
    }
    to_cel = to_celsius[from_temp](temp)
    return from_celsius[to_temp](to_cel)


def convert_weigth(from_weight: str, to_weight: str, weight: float):
    to_gram = {
        "mili": lambda x: x / 1000,
        "gram": lambda x: x,
        "kg": lambda x: x * 1000,
        "ounce": lambda x: x * 28349.5,
        "pound": lambda x: x * 453592,
    }
    from_gram = {
        "mili": lambda x: x * 1000,
        "gram": lambda x: x,
        "kg": lambda x: x / 1000,
        "ounce": lambda x: x / 28349.5,
        "pound": lambda x: x / 453592,
    }
    to_gr = to_gram[from_weight](weight)
    return from_gram[to_weight](to_gr)


def convert_lenght(from_length: str, to_length: str, length: float):
    to_metre = {
        "millimeter": lambda x: x / 1000,
        "centimeter": lambda x: x / 100,
        "meter": lambda x: x,
        "kilometer": lambda x: x * 1000,
        "inch": lambda x: x / 39.37,
        "foot": lambda x: x / 3.281,
        "yard": lambda x: x / 1.094,
        "mile": lambda x: x * 1609,
    }
    from_metre = {
        "millimeter": lambda x: x * 1000,
        "centimeter": lambda x: x * 100,
        "meter": lambda x: x,
        "kilometer": lambda x: x / 1000,
        "inch": lambda x: x * 39.37,
        "foot": lambda x: x * 3.281,
        "yard": lambda x: x * 1.094,
        "mile": lambda x: x / 1609,
    }
    to_len = to_metre[from_length](length)
    return from_metre[to_length](to_len)


@app.post("/temp")
async def temp_convert(request: temp):
    if request.convert_from == request.convert_to:
        raise HTTPException(
            status_code=400, detail="The convert type can't be the same"
        )
    return {
        "converted_temp": convert_temp(
            temp=request.temp,
            to_temp=request.convert_to,
            from_temp=request.convert_from,
        )
    }


@app.post("/weight")
async def weight_convert(request: weight):
    if request.convert_from == request.convert_to:
        raise HTTPException(status_code=400, detail="The convert type can't be same")
    return {
        "converted_weight": convert_weigth(
            weight=request.weight,
            from_weight=request.convert_from,
            to_weight=request.convert_to,
        )
    }


@app.post("/length")
async def weight_convert(request: length):
    if request.convert_from == request.convert_to:
        raise HTTPException(status_code=400, detail="The convert type can't be same")
    return {
        "converted_weight": convert_lenght(
            length=request.length,
            from_length=request.convert_from,
            to_length=request.convert_to,
        )
    }
