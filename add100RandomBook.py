#!/usr/bin/env python3
import requests
import json
from faker import Faker

APIHOST = "http://library.demo.local"
LOGIN = "cisco"
PASSWORD = "Cisco123!"

def getAuthToken():
    authCreds = (LOGIN, PASSWORD)
    r = requests.post(
        f"{APIHOST}/api/v1/loginViaBasic",
        auth = authCreds
    )
    if r.status_code == 200:
        return r.json()["token"]
    else:
        raise Exception(f"Status code {r.status_code} and text {r.text}, while trying to Auth.")

def addBook(book, apiKey):
    r = requests.post(
        f"{APIHOST}/api/v1/books",
        headers = {
            "Content-type": "application/json",
            "X-API-Key": apiKey
        },
        data = json.dumps(book)
    )
    if r.status_code == 200:
        print(f"Book {book} added.")
    else:
        raise Exception(f"Error code {r.status_code} and text {r.text}, while trying to add book {book}.")

def deleteBook(book_id, apiKey):
    r = requests.delete(
        f"{APIHOST}/api/v1/books/{book_id}",
        headers = {
            "Content-type": "application/json",
            "X-API-Key": apiKey
        }
    )
    if r.status_code == 200:
        print(f"Book with ID {book_id} deleted.")
    else:
        raise Exception(f"Error code {r.status_code} and text {r.text}, while trying to delete book {book_id}.")

def getAllBooks(apiKey):
    r = requests.get(
        f"{APIHOST}/api/v1/books",
        headers = {
            "Content-type": "application/json",
            "X-API-Key": apiKey
        }
    )
    if r.status_code == 200:
        return r.json()
    else:
        raise Exception(f"Error code {r.status_code} and text {r.text}, while trying to get books.")

def add25RandomBooks(apiKey):
    """Add 25 random books with ISBN numbers"""
    print("Adding 25 random books with ISBN numbers...")
    fake = Faker()
    
    for i in range(4, 29):  # This will create 25 books (IDs 4-28)
        fakeTitle = fake.catch_phrase()
        fakeAuthor = fake.name()
        fakeISBN = fake.isbn13()  # Generate ISBN numbers as required
        book = {"id":i, "title": fakeTitle, "author": fakeAuthor, "isbn": fakeISBN}
        # add the new random "fake" book using the API
        addBook(book, apiKey)
    
    print("Successfully added 25 random books!")

def deleteFirstAndLastFiveBooks(apiKey):
    """Delete the first 5 and last 5 books from the library"""
    print("Deleting first 5 and last 5 books...")
    
    # Get all existing books
    all_books = getAllBooks(apiKey)
    
    if len(all_books) < 10:
        print(f"Warning: Only {len(all_books)} books available. Cannot delete 10 books.")
        return
    
    # Sort books by ID to ensure we get the correct first and last books
    sorted_books = sorted(all_books, key=lambda x: x['id'])
    
    # Delete first 5 books
    print("Deleting first 5 books...")
    for i in range(5):
        deleteBook(sorted_books[i]['id'], apiKey)
    
    # Delete last 5 books
    print("Deleting last 5 books...")
    for i in range(len(sorted_books) - 5, len(sorted_books)):
        deleteBook(sorted_books[i]['id'], apiKey)
    
    print("Successfully deleted first 5 and last 5 books!")

def main():
    """Main function to demonstrate both functionalities"""
    try:
        # Get the Auth Token Key
        apiKey = getAuthToken()
        print("Authentication successful!")
        
        # Uncomment the function you want to run:
        
        # To add 25 random books with ISBN numbers:
        add25RandomBooks(apiKey)
        
        # To delete first 5 and last 5 books:
        # deleteFirstAndLastFiveBooks(apiKey)
        
        # You can also run both operations in sequence:
        # add25RandomBooks(apiKey)
        # deleteFirstAndLastFiveBooks(apiKey)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()