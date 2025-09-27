from fastapi import FastAPI,Body

# App object
app = FastAPI()

Books = [
    {
        "author_name": "Abraham Silberschatz",
        "title": "Operating System Concepts",
        "genre": "Computer Science"
    },
    {
        "author_name": "Thomas H. Cormen",
        "title": "Introduction to Algorithms",
        "genre": "Algorithms"
    },
    {
        "author_name": "James F. Kurose",
        "title": "Computer Networking: A Top-Down Approach",
        "genre": "Networking"
    },
    {
        "author_name": "Ian Goodfellow",
        "title": "Deep Learning",
        "genre": "Artificial Intelligence"
    },
    {
        "author_name": "Mark Lutz",
        "title": "Learning Python",
        "genre": "Programming"
    },
    {
        "author_name": "Jennifer Niederst Robbins",
        "title": "Learning Web Design",
        "genre": "Web Development"
    },
    {
        "author_name": "Elmasri & Navathe",
        "title": "Fundamentals of Database Systems",
        "genre": "Databases"
    },
    {
        "author_name": "E. Balagurusamy",
        "title": "Programming in ANSI C",
        "genre": "Programming"
    },
    {
        "author_name": "Stuart Russell",
        "title": "Artificial Intelligence: A Modern Approach",
        "genre": "Artificial Intelligence"
    },
    {
        "author_name": "Robert C. Martin",
        "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
        "genre": "Software Engineering"
    }
]

# Base or home Url
@app.get("/")
def home():
    return "Welcome to FastAPI!!"

# A Normal Get Request
@app.get("/books")
def read_all_books():
    """Reading all the books"""
    return Books

# GET request with path paramters
@app.get("/books/{author_name}")
def get_book_by_author(author_name: str):
    """Getting books by author name"""
    books = []
    for book in Books:
        if book['author_name'].casefold() == author_name.casefold():
            books.append(book)
        
    return books if len(books)>0 else {"message": f"No Book found for the author : {author_name}"}

# GET request with query paramters
@app.get("/books/")
def get_book_by_genre(genre: str):
    """Getting books by genre"""
    books = []
    for book in Books:
        if book['genre'].casefold() == genre.casefold():
            books.append(book)
        
    return books if len(books)>0 else {"message": f"No Book found for the genre : {genre}"}

# POST request to add the books
@app.post("/books/add_book")
def add_book(new_book=Body()):
    """Adding a new book in the existing book collections"""
    
    old_len = len(Books)
    if ("title" in new_book) and ("author_name" in new_book) and ("genre" in new_book):
        Books.append(new_book)
        
    new_len = len(Books)
    response = {"message" : "Succesfully added a new book" if new_len>old_len else "Unable to add new book"}
    return response

# PUT Request to edit/update a book by title
@app.put("/books/update_book")
def update_book(title:str, updated_book=Body()):
    """Updating a book by the title name"""
    changed_index = -1
    for i in range(0,len(Books)):
        if Books[i]['title'].casefold()==title.casefold():
            Books[i] = updated_book
            changed_index = i
            
    response = {"message":f"Book Updated succesfully : {Books[changed_index]}" if Books[changed_index]==updated_book else f"Failed to update the book for the title {title}"}
    
    return response

# DELETE Request to delete a book by title 
@app.delete("/books/delete_book/{title}")
def book_delete_by_title(title:str):
    """Deleting a book by its title name"""
    
    old_len = len(Books)
    
    for i in range(0,old_len):
        if Books[i]['title'].casefold() == title.casefold():
            deleted_book = Books[i] 
            del Books[i] # or Books.pop(i)
            break
    new_len = len(Books)
    
    response = {"message":f"Book deleted successfully : \n {deleted_book}" if new_len<old_len else f"Unable to delete book {title}"}
    return response
