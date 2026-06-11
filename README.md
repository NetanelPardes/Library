# Library progect

## Project Objective

Our project deals with library management
The program manages the library's books and subscriptions.

## The code for creating a Docker with a connection to SQL

```bash
docker run --name mysql-w7 -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=soldiers_db -p 3306:3306 -d mysql:8
```
## Folder structure
```
library-api/
│
│
├── main.py
├── database/
│ ├── db_connection.py
│ ├── book_db.py
│ └── member_db.py
├── routes/
│ ├── book_routes.py
│ ├── member_routes.py
│ └── report_routes.py
├── logs/
│ └── app.log
│
├── README.md
├── requirements.txt
└── .gitignore
```

## Table structure

### Book table
| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | int | PRIMARY KEY | Book number |
| title | VARCHAR(50) | NOT NULL | Book name | 
| author | VARCHAR(50) | NOT NULL | Author name |
| genre | VARCHAR(50) | ENUM | Book genre |
| is_available | BOOLEAN |NOT NULL | Is the book available for borrowing |
| borrowed_by_member_id | BOOLEAN | NOT NULL | The ID of the member who | borrowed the book |


### Subscription table

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | int | PRIMARY KEY | Subscription number |
| email | VARCHAR(50) | NOT NULL | Subscriber email |
| is_active | BOOLEAN |NOT NULL | Is the subscription active |
| total_borrows | int  | NOT NULL | How many books borrowed |


## System rules

```
1. Creating a book - User submits title,author,genre (System adds — is_available=True, borrowed_by=NULL)
2. genre - Must be any value — Fiction / Non-Fiction / Science / History / Other Other returns an error
3. creating a member - User sends name,email (system adds — is_active=True, total_borrows=0)
4. email uniqueness - Must be unique — if it already exists returns an error
5. Inactive member - if is_active=False you cannot borrow a book
6. Book not available - You cannot borrow a book that is already borrowed (( ) is_available=False )
7. Maximum books - a member cannot hold more than 3 books at a time
8. Returning a book - A book can only be returned if it is lent to the same member who is returning it.
```

## API Endpoints
### Books Endpoints

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| POST | /books | Create a book | {"title": title,"author": author,"genre": genre} |  |
| GET | /books | All books |  | List of book dictionaries | 
| GET | /books/{id} | Book by id |  | book dictionarie |
| PATCH | /books/{id} | Update a book | {"title": title, "author": author, "genre": genre} |  |
| PATCH | /books/{id}/borrow/{member_id} | Loan a book to a member | |{"message": "Book id borrow to a member id"} |
| PATCH | /books/{id}/return/{member_id} | Return a book from a member | |{"message": "Book id returned from member id"}|

### Members Endpoints

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| POST | /members | Create member | {"name": name,"email": email}| |
| GET | /members | All members | | List of Member dictionaries |
| GET | /members/{id} | Member by ID | | Member dictionarie |
| PATCH | /members/{id} | Update member | {"name": name,"email": email}||
| PATCH | /members/{id}/deactivate | Deactivate member | | {"message": "Member id inactive"} |
| PATCH | /members/{id}/activate | Activate member | |{"message": "Member id active"}|


### Reports Endpoints

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| GET | /reports/summary | General Report | | |
| GET | /reports/books-by-genre | Books by Genre | |{"genre": genre , "Books" : {List of books}}|
| GET | /reports/top-member | Most Active Member | |{"message": "Member id Most active"} |


## System Flow
```
**Server Startup:**
   - The server connects to MySQL
   - Creates tables if they don't exist
   - Starts the FastAPI server
```

```
**Creating a Member:**
   - User sends POST request to `/members` with name and email
   - System validates the email is unique
   - System creates member with `is_active=True` and `total_borrows=0`
   - Returns the created member
```
```
**Show all Member:** 
    - Sends a GET request to `/Member`
    - Returns all Member
```

```
**Search for a Member by ID:**
    - Sends a GET request to `/Member/{id}` with the Member number
    - The system checks that the Member exists
    - The system returns the Member
```

```
**Member Update:**
    - Sends a PATCH request to `/Member/{id}` with the Member number
    - The system checks that the Member exists in The system
    - The system updates the Member in the table according to the data from the body
    - The system returns the updated Member
```

```
**Deactivating a member:**
    - Sends a PATCH request to `/members/{id}/deactivate` with the member number
    - The system checks that the member exists in the system
    - The system updates the member with is_active false
    - The system returns the updated member
```

```
**Activate a member:**
    - Sends a PATCH request to `/members/{id}/activate` with the member number
    - The system checks that the member exists in the system
    - The system updates the member with is_active true
    - The system returns the updated member
```

```
**Creating a book:**
    - Sends a POST request to `/books` with author name and genre
    - The system checks that genre is one of Fiction / Non-Fiction / Science / History / Other
    - The system creates a book with is_available=True , borrowed_by=NULL
    - The system returns the created book
```

```
**Show all books:** 
    - Sends a GET request to `/books`
    - Returns all books
```

```
**Search for a book by ID:**
    - Sends a GET request to `/books/{id}` with the book number
    - The system checks that the book exists
    - The system returns the book
```

```
**Book Update:**
    - Sends a PATCH request to `/books/{id}` with the book number
    - The system checks that the book exists in The system
    - The system updates the book in the table according to the data from the body
    - The system returns the updated book
```

```
**Borrowing a Book:**
   - User sends PATCH request to `/books/{id}/borrow/{member_id}`
   - System checks if book exists
   - System checks if member exists and is active
   - System checks if book is available
   - System checks if member has less than 3 books
   - Updates book: `is_available=False`, `borrowed_by_member_id=member_id`
   - Increments member's `total_borrows` by 1
   - Returns success message
```

```
**Returning a book :**
    - Sends a PATCH request to `/books/{id}/return/{member_id}` with the book number and member number
    - The system checks that the book exists in the system
    - The system checks that the member exists in the system
    - The system checks that a book is lent to that member
    - The system updates that the book can be lent
    - The system updates that the member who is lending the book is NONE
    - The system updates that the member who lent one less book
    - The system returns the updated book
```

```
**General Report:**
    - Sends a GET request to `/reports/summary`
    - The system returns a general report
```

```
**Books by Genre:**
    - Sends a GET request to `reports/books-by-genre`
    - The system returns a dictionary of genres and a list of books by that genre
```

```
**Most Active Member:**
    - Sends a GET request to `/reports/top-member`
    - The system returns the member with the most book inquiries
```

## Running the Project

### Option 1
```
Run the main file
```

### Option 2
```bush
uvicorn main:app --reload
```


