#import fastapi
from typing import Annotated
import os
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()
#import fastapi
from fastapi import Depends, FastAPI, Form, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
#instantiate the app
app = FastAPI(
    title="Aller Manger Restaurant",
    version="1.0.0",
    summary=" Aller Manger Restaurant REST API for developers",
    description= "Aller Manger REST API is an API that enables the restaurant expand its services and enable developers to innovate how best they can help us serve our customers. This API exposes core parts of our reservation services and caters for our restaurant booking."
)
#example origins
"""origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]"""

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#imports from internal modules
from config.check_mongodb_connection import check_mongodb_connection
from config.db_config import accounts, tables

#import important functions
from utils.account_module import encrypt_password, get_current_user, authenticate_user, create_access_token
#import models
from models.user_model import User, UserBody
from models.table_model import Table, TableCancel
#check mongodb connection
check_mongodb_connection()

#ENVs
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

#create redirect endpoint
@app.get("/")
def root():
    #return to baseUrl when user hits http://localhost:8000/
    return RedirectResponse(
        url="/api/v1.0/",
        status_code= 307
    )

#define common baseUrl
baseUrl = "/api/aller-manger/v1.0"

#create entry endpoint
@app.get(f"{baseUrl}")
def api_root():
    return {
        "message":"Welcome to the restaurant."
    }

#POST Request - does mostly addition to the database
#Accounts Endpoints
@app.post(f"{baseUrl}/users/create/account")
def create_guest_account(form_submission: Annotated[User,Form()]):
    #get all the user inputs and dump them
    user_dict = form_submission.model_dump()
    user_hashed_password = str(encrypt_password(form_submission.password))
    #replace user_dict password with hashed password
    user_dict["password"] = user_hashed_password

    #check if user already exists and has the same username, phone, email
    query_filter = {
        "$or":[
                {"user_name" : form_submission.user_name},
                {"phone" : form_submission.phone},
                {"email" : form_submission.email}
            ]
        }
    #get user from the db
    similar_users = accounts.count_documents(query_filter)

    #check number
    if similar_users>0:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "A user with the email, username or phone number already exists."
        )
    
    #save the dictionary to mongodb
    saved_result = accounts.insert_one(user_dict)
    #check if the document was saved
    if saved_result.inserted_id:
        raise HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail= "New guest has been added to Aller Manger Restaurant."
        )
    
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail= "Something went wrong during."
    )


@app.post(f"{baseUrl}/users/login")
def login_guest(login_body: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if not login_body.username or not login_body.password:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail = "Username/ email or password missing."
        )
    user  = authenticate_user(login_body.username, login_body.password)

    if not user:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Sorry but your password or email might be wrong."
        )
    #create access token time
    expiry_minutes = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user, expiry_minutes)

    return {
        "access_token": access_token,
        "expiry": expiry_minutes
    }
   

#endpoint to add table preservations
@app.post(f"{baseUrl}/add/reservation")
def reserve_table(
    current_user: Annotated[UserBody, Depends(get_current_user)],
    table_reservation: Annotated[Table, Form()]
):
    
    #TODO: Check for existing tables that have been booked and time
    #Exercise - Hint -use the tables collection to count and use also HTTPException
    ###################### START HERE ################################
    get_exisiting_tables = tables.count_documents({
        "table_no": int(table_reservation.table_no),
        "active":True
        })
    
    if get_exisiting_tables>0:
        return HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = "Table has been already reserved."
        )
    ######################################################################
    #create new reservation
    table_dict = table_reservation.model_dump()
    table_dict["user_id"] = current_user.user_id
    table_dict["user_name"] = current_user.user_name
    new_reservation = tables.insert_one(table_dict)

    #check if reservation was made
    if not new_reservation.inserted_id:
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "An error occurred while creating your reservation, please try again."
        )
    
    raise HTTPException(
        status_code= status.HTTP_201_CREATED,
        detail = f"New reservation: {new_reservation.inserted_id} made successfully for {current_user.first_name}."
    )

#Extra Work - Session One
#Create an endpoint that will be able to reset all previous reservations made in the last 24HRS inactive
#HINT: all tables have an 'active' field in the document, make the active false for all reservations made using pymongo
#Instruction: After finishing make sure you run the pytest - instruction for running the test is provided in the README.md file
#Write code here
############# START HERE #######################


############# FINISH HERE ######################

#get all user orders
@app.get(f"{baseUrl}/user/reservations")
def get_customer_active_reservations(
    current_user: Annotated[UserBody, Depends(get_current_user)],
):
    
    #get customer reservations count
    reservations_count = tables.count_documents(
        {"$and":[
            {"user_id":current_user.user_id},
            {"active":True}
        ]}
        )
    
    if reservations_count == 0:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = "No reservations found."
        )
    #get customer reservations
    reservations = tables.find(
        {
            "$and":[
                {"user_id":current_user.user_id},
                {"active":True}
            ]
        }, {"_id":0}
        ).to_list()
    
    

    return reservations

#update table reservation (cancel a reservation)
#PUT
@app.put(f"{baseUrl}/user/reservations/cancel")
def update_customer_reservations(
    current_user: Annotated[UserBody, Depends(get_current_user)],
    table_no: Annotated[TableCancel, Form()]
):
    #cancelling the reservation by making it inactive
    update_filter = {"user_id":current_user.user_id, "table_no":table_no.table_no, "active":True}
    #update query
    update_query = {
        "$set":{"active":False}
    }

    cancellation_result = tables.update_one(update_filter,update_query)

    if not cancellation_result:
        return HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Oops! An error occurred while cancelling your order."
        )
    
    raise HTTPException(
        status_code= status.HTTP_201_CREATED,
        detail= "Reservation cancelled, we will miss you."
    )

#Delete reservation
#DELETE
@app.delete(f"{baseUrl}/user/reservations/delete/"+"{rsv_id}")
def update_customer_reservations(
    current_user: Annotated[UserBody, Depends(get_current_user)],
    rsv_id: str
):
    #search for reservation that belongs to current user
    rsv_result = tables.delete_one({"reservation_id":rsv_id,"user_id":current_user.user_id})

    if not rsv_result:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = "Reservation does not exist"
        )
    
    raise HTTPException(
        status_code= status.HTTP_201_CREATED,
        detail= f"Your reservation: {rsv_id}, has been deleted successfully."
    )

#Final Work
#Create two routes:
#1. For deleting a user
#2. Another to update the user_name of the user
@app.put(f"{baseUrl}/user/reservations/cancel") 
def update_customer_reservations( 
    current_user: Annotated[UserBody, Depends(get_current_user)], 
    table_no: Annotated[TableCancel, Form()] 
): 
    #cancelling the reservation by making it inactive 

    update_filter = {"user_id":current_user.user_id, "table_no":table_no.table_no, 
"active":True} 

    #update query 

    update_query = { 
        "$set":{"active":False} 
    } 

    cancellation_result = tables.update_one(update_filter,update_query) 

    if not cancellation_result: 
        return HTTPException( 
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail = "Oops! An error occurred while cancelling your order." 
        ) 

    raise HTTPException( 
        status_code= status.HTTP_201_CREATED, 
        detail= "Reservation cancelled, we will miss you." 
    ) 

#Delete reservation 

@app.delete(f"{baseUrl}/user/reservations/delete/"+"{rsv_id}") 
def update_customer_reservations( 
    current_user: Annotated[UserBody, Depends(get_current_user)], 
    rsv_id: str 
): 
    #search for reservation that belongs to current user 

    rsv_result = tables.delete_one({"reservation_id":rsv_id,"user_id":current_user.user_id}) 

    if not rsv_result: 
        raise HTTPException( 
            status_code= status.HTTP_404_NOT_FOUND, 
            detail = "Reservation does not exist" 
        ) 

    raise HTTPException( 
        status_code= status.HTTP_201_CREATED, 
        detail= f"Your reservation: {rsv_id}, has been deleted successfully." 
    ) 

#Final Work 

#Create two routes: 

#1. For deleting a user 

#2. Another to update the user_name of the user 
