
import random
from mode import *
import pymongo
import os
from ausbills.federal_parliment import all_bills, Bill
import json
from update_ballotspecs_db import update_ballotspecs


# Connection String
client = pymongo.MongoClient(mongosettings[URL])
db = client[mongosettings[MONGODB]]
bills_collection = db[mongosettings[BILLSCOLLECTION]]


# dummy function, waiting for votes to be counted on the blockchain.
def get_votes(id):
    return(500 + int(random.random()*1000), 500 + int(random.random()*1000))


# print(all_bills)
for i in range(len(all_bills)):
    print(all_bills[i]["id"])
    url = all_bills[i]["url"]
    bill = Bill(url)
    #  Standed keys
    bill.data["question"] = "Should this bill be passed into law?"
    bill.data["description"] = bill.data.pop("summary")
    if bill.data["chamber"] == "House":
        bill.data["start_date"] = bill.data["intro_house"]
    else:
        bill.data["start_date"] = bill.data["intro_senate"]

    update_ballotspecs(bill.data["id"], bill.data["short_title"], bill.data["question"],
                       bill.data["description"], bill.data["start_date"], bill.data["chamber"], bill.data["sponsor"])

    bills_collection.replace_one({'_id': bill.data["id"]}, {'data': bill.data}, True)
