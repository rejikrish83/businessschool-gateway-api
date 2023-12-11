
from fastapi import APIRouter
from fastapi import FastAPI, HTTPException, status,Path
from datetime import datetime
from bson.json_util import dumps
from utility.QueryBuilder import QueryBuilder
import json
from database.DatabaseUtility import DatabaseUtility
from bson import ObjectId
import httpx


# Read configuration from JSON file
with open("config.json", "r") as config_file:
    config = json.load(config_file)

module_endpoint_uri = config["otherConfig"]["moduleEndpointUrl"]
DATE_FORMAT = "%Y-%m-%d"
router = APIRouter()
queryBuilder = QueryBuilder()







@router.get("/user/{username}")
def get_user_by_username(username):
    user_document = "hello"
    if user_document:
        return user_document
    else:
        raise HTTPException(status_code=404, detail=f"User with username {username} not found")

async def callToGetUser(userName):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(module_endpoint_uri+"v1/user/"+userName)

        response.raise_for_status()
        return response.json()

    except httpx.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Error calling user endpoint")

async def getModuleByUserId(userId):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(module_endpoint_uri+"v1/get_modules_and_assignments/"+userId)

        response.raise_for_status()
        return response.json()

    except httpx.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Error calling Module endpoint")


@router.get("/courseModule/{username}")
async def get_courseModule_by_username(username):
    userRespsonse = await callToGetUser(username)
    print(userRespsonse)

    # userData = userRespsonse["value"]

    # Call the second endpoint with data from the first response
    moduleDetails = await getModuleByUserId(userRespsonse['_id'])

    # Combine the responses
    combined_response = {
        "user": userRespsonse,
        "module": moduleDetails,
    }



    if combined_response:
        return combined_response
    else:
        raise HTTPException(status_code=404, detail=f"User with username {username} not found")

@router.get("/getKpiData")
async def getKpiData(userId: str, date_str: str, role:str, dataType:str, moduleId:str):
    params = {"userId": userId, "date_str": date_str,"role":role, "dataType":dataType, "moduleId":moduleId }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(module_endpoint_uri+"v1/get_kpi_data",params=params)

        response.raise_for_status()
        return response.json()

    except httpx.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Error calling Module endpoint")

    if response:
        return response
    else:
        raise HTTPException(status_code=404, detail=f"User with username {username} not found")

@router.get("/getUniqueKpi")
async def getKpiData(moduleId:str):
    params = {"moduleId":moduleId }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(module_endpoint_uri+"v1/unique_data_types",params=params)

        response.raise_for_status()
        print(response)
        return response.json()

    except httpx.HTTPError as e:
        print(e)
        raise HTTPException(status_code=e.response.status_code, detail="Error calling Module endpoint")

    if response:
        return response
    else:
        raise HTTPException(status_code=404, detail=f"User with username {username} not found")