## This module contains the user interface for the library system. 
# It allows users to search for books, borrow books, and return books.

## Import the necessary functions from the admin module. 
# Replace "function_name1" with the actual function names you want to import.

from admin import (
    load_library,
    save_library,
    find_book
)



## Search books by category.
## This function should return book IDs that match the given category.
def books_in_category(
    books,
    category
):
    result = []
    cat = category.strip().lower()
    for book_id, book in books.items():
        if book["category"].lower() == cat:
            result.append(book_id)
    return result

    


## Search books by full or partial title.
## This function should return book IDs that match the given title or part of the title.
def search_by_title(
    books,
    search_text
):
    result = []
    s = search_text.strip().lower()
    for book_id, book in books.items():
        if s in book["title"].lower():
            result.append(book_id)
    return result
    


## Create logic to let users borrow books.
## The function should check if the book is available or on loan, or if the borrower name is provided.
## If the book is not found, then return "BOOK_NOT_FOUND"
## If the borrower name is empty, then return "EMPTY_NAME"
## If the book is not available, then return "NOT_AVAILABLE"
## If the book is successfully borrowed, then return "OK"
def borrow_book(
    books,
    loans,
    search_text,
    borrower
):
    # check empty name
    if borrower.strip() == "":
        return "EMPTY_NAME"

    book_id = find_book(books, search_text)

    if book_id is None:
        return "BOOK_NOT_FOUND"

    if books[book_id]["available"] == False:
        return "NOT_AVAILABLE"

    books[book_id]["available"] = False
    loans.append({"book_id": book_id, "borrower": borrower})
    return "OK"

    


## Create logic to let users return books.
## The function should check if the book is on loan, or if the borrower name is provided
## If the book is not found, then return "BOOK_NOT_FOUND"
## If the borrower name is empty, then return "EMPTY_NAME"
## If the book is not on loan, then return "NOT_ON_LOAN"
## If the book is successfully returned, then return "OK"

def return_book(
    books,
    loans,
    book_title,
    borrower
):
    # check empty name
    if borrower.strip() == "":
        return "EMPTY_NAME"

    book_id = find_book(books, book_title)

    if book_id is None:
        return "BOOK_NOT_FOUND"

    # check if it is actually on loan
    found = None
    for i in range(len(loans)):
        if loans[i]["book_id"] == book_id:
            found = i
            break

    if found is None:
        return "NOT_ON_LOAN"

    books[book_id]["available"] = True
    loans.pop(found)
    return "OK"



## The main function that runs the user interface for the library system.
## The function must first load the library data from a JSON file, then display a menu for the user to select options.
## The options include searching for books by title or category, borrowing a book, returning a book, and exiting the program.
## When the user selects an option, the corresponding function is called to perform the action.
## The program continues to display the menu until the user chooses to exit, at which point the library data is saved back to the JSON file.
## The main function should also handle invalid selections by displaying an error message and prompting the user to select again.
def main():
    data = load_library("library.json")
    books = data["books"]
    loans = data["loans"]

    print("LIBRARY USER SYSTEM")
    print("------------------------------------------------------------")

    while True:
        print("1. Search by title")
        print("2. Search by category")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            t = input("Enter title to search: ")
            res = search_by_title(books, t)
            print("Found books: " + str(res))

        elif choice == "2":
            c = input("Enter category: ")
            res = books_in_category(books, c)
            print("Found books: " + str(res))

        elif choice == "3":
            bid = input("Enter book id or title: ")
            name = input("Enter your name: ")
            r = borrow_book(books, loans, bid, name)
            print("Result: " + r)

        elif choice == "4":
            bid = input("Enter book id or title: ")
            name = input("Enter your name: ")
            r = return_book(books, loans, bid, name)
            print("Result: " + r)

        elif choice == "5":
            save_library(data, "library.json")
            print("Goodbye!")
            break

        else:
            print("Invalid option, please try again.")

    return


if __name__ == "__main__":
    main()
