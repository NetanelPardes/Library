# Library progect

## Project Objective

Our project deals with library management
The program manages the library's books and subscriptions.

## The code for creating a Docker with a connection to SQL

```powershell
docker run --name mysql-w7 -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=soldiers_db -p 3306:3306 -d mysql:8
```
## Folder structure
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

## Table structure

### Book table
Book number - id
Book name - title
Author name - author
Book genre - genre
Is the book available for borrowing - is_available
The ID of the member who borrowed the book - borrowed_by_member_id

### Subscription table
Subscription number - id
Subscriber email - email
Is the subscription active - is_active
How many books borrowed - total_borrows