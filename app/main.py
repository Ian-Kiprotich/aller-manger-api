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




#imports from internal modules

#import important functions

#import models

#check mongodb connection


#ENVs
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

#create redirect endpoint


#define common baseUrl
baseUrl = "/api/aller-manger/v1.0"

#create entry endpoint


#POST Request - does mostly addition to the database
#Accounts Endpoints
@app.post(f"{baseUrl}/users/create/account")
def create_guest_account(form_submission: Annotated[User,Form()]):
    #get all the user inputs and dump them
   
    #replace user_dict password with hashed password
    

    #check if user already exists and has the same username, phone, email
   
    #get user from the db
    

    #check number
   
    #save the dictionary to mongodb
    
    #check if the document was saved
   
    
   yield


@app.post(f"{baseUrl}/users/login")
def login_guest(login_body: Annotated[OAuth2PasswordRequestForm, Depends()]):
   
    #create access token time
    
   yield

#endpoint to add table preservations
@app.post(f"{baseUrl}/add/reservation")
def reserve_table(
    current_user: Annotated[UserBody, Depends(get_current_user)],
    table_reservation: Annotated[Table, Form()]
):
    
    #TODO: Check for existing tables that have been booked and time
    #Exercise - Hint -use the tables collection to count and use also HTTPException
    ###################### START HERE ################################
   
    ######################################################################
    #create new reservation
   

    #check if reservation was made
    
    yield

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
   
    #get customer reservations
    yield

#update table reservation (cancel a reservation)
#PUT
@app.put(f"{baseUrl}/user/reservations/cancel")
def update_customer_reservations(
    current_user: Annotated[UserBody, Depends(get_current_user)],
    table_no: Annotated[TableCancel, Form()]
):
    #cancelling the reservation by making it inactive
    
    #update query
    

    yield

#Delete reservation
#DELETE
@app.delete(f"{baseUrl}/user/reservations/delete/"+"{rsv_id}")
def update_customer_reservations(
    current_user: Annotated[UserBody, Depends(get_current_user)],
    rsv_id: str
):
    #search for reservation that belongs to current user
   
   yield

#Final Work
#Create two routes:
#1. For deleting a user
#2. Another to update the user_name of the user