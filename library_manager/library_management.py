class Book:
    def __init__(self, title: str, author: str, isbn: str, status: str = 'available'):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status.lower() 

    def get_details(self) -> str:
        return f"'{self.title}' by {self.author} (ISBN: {self.isbn}) - Status: {self.status.capitalize()}"

    def __repr__(self):
        return f"Book('{self.title}', '{self.author}', '{self.isbn}', '{self.status}')"

    def to_csv_line(self) -> str:
        return f"{self.title},{self.author},{self.isbn},{self.status}\n"

    def issue(self):
        if self.is_available():
            self.status = 'issued'
            return True
        return False
    
    def return_book(self):
        if self.status == 'issued':
            self.status = 'available'
            return True
        return False
    
    def is_available(self) -> bool:
        return self.status == 'available'

class LibraryInventory:
    FILE_NAME = "catalog.csv" 

    def __init__(self):
        self.books = []
        load_message = self.load_catalog()
        print(load_message)

    def add_book(self, book: Book):
        self.books.append(book)
        return f"Added book: {book.title}"

    def search_by_title(self, title: str) -> list[Book]:
        results = [book for book in self.books if title.lower() in book.title.lower()]
        return results

    def search_by_isbn(self, isbn: str) -> Book | None:
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def display_all(self):
        if not self.books:
            return ["The inventory is empty."]
        return [book.get_details() for book in self.books] 

    def save_catalog(self):
        file_handle = None
        try:
            file_handle = open(self.FILE_NAME, 'w')
            file_handle.write("Title,Author,ISBN,Status\n") 
            for book in self.books:
                file_handle.write(book.to_csv_line())
            print(f"INFO: Successfully saved {len(self.books)} books to {self.FILE_NAME}.")
            return True
        except IOError as e:
            print(f"ERROR: Could not save catalog to {self.FILE_NAME}. {e}")
            return False
        finally:
            if file_handle:
                file_handle.close()

    def load_catalog(self):
        file_handle = None
        lines = []
        try:
            file_handle = open(self.FILE_NAME, 'r')
            lines = file_handle.readlines()
        except FileNotFoundError:
            return f"INFO: {self.FILE_NAME} not found. Starting with an empty inventory."
        except IOError as e:
            return f"ERROR: An I/O error occurred during file load. {e}"
        finally:
            if file_handle:
                file_handle.close()

        try:
            if not lines:
                return f"INFO: File {self.FILE_NAME} is empty. Starting with an empty inventory."
            
            data_lines = lines[1:] if lines[0].strip().lower() == "title,author,isbn,status" else lines

            books_loaded = 0
            for line in data_lines:
                parts = line.strip().split(',')
                if len(parts) == 4:
                    title, author, isbn, status = parts
                    book = Book(title, author, isbn, status)
                    self.books.append(book)
                    books_loaded += 1
                else:
                    print(f"WARNING: Skipping corrupted line in CSV: {line.strip()}")
            
            return f"INFO: Successfully loaded {books_loaded} books from {self.FILE_NAME}."
        except Exception as e:
            return f"ERROR: Data corruption found in {self.FILE_NAME}. Starting with an empty inventory. Details: {e}"

def display_menu():
    print("\n" + "="*40)
    print("LIBRARY INVENTORY MANAGER MENU")
    print("="*40)
    print("1. Add New Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All Books")
    print("5. Search Book")
    print("6. Exit & Save")
    print("-" * 40)

def add_book_cli(inventory: LibraryInventory):
    print("\n--- Add New Book ---")
    
    while True:
        try:
            title = input("Enter Title: ").strip()
            if not title:
                raise ValueError("Title cannot be empty.")
            break
        except Exception as e:
            print(f"Input Error: {e} Please try again.")

    author = input("Enter Author: ").strip()
    
    while True:
        try:
            isbn = input("Enter ISBN (e.g., 978-0123456789): ").strip()
            if not isbn or (len(isbn.replace('-', '')) < 10):
                raise ValueError("Invalid ISBN format/length.")
            break
        except Exception as e:
            print(f"Input Error: {e} Please try again.")

    new_book = Book(title=title, author=author, isbn=isbn) 
    result = inventory.add_book(new_book)
    print(f"\nSUCCESS: {result}")

def issue_return_book_cli(inventory: LibraryInventory, action: str):
    action_verb = "Issue" if action == 'issue' else "Return"
    print(f"\n--- {action_verb} Book ---")
    
    try:
        isbn = input(f"Enter ISBN of the book to {action}: ").strip()
        
        if not isbn:
            raise ValueError("ISBN cannot be empty.")

        book = inventory.search_by_isbn(isbn)
        
        if book is None:
            print(f"ERROR: Book with ISBN '{isbn}' not found.")
            return

        print(f"Found book: {book.get_details()}")
        
        if action == 'issue':
            if book.issue():
                print(f"SUCCESS: Successfully **issued** '{book.title}'. Status is now 'Issued'.")
            else:
                print(f"WARNING: Cannot issue '{book.title}'. It is already issued.")
        elif action == 'return':
            if book.return_book():
                print(f"SUCCESS: Successfully **returned** '{book.title}'. Status is now 'Available'.")
            else:
                print(f"WARNING: Cannot return '{book.title}'. It is already available.")
                
    except Exception as e:
        print(f"Operation failed due to an error: {e}")

def view_all_cli(inventory: LibraryInventory):
    print("\n" + "="*50)
    print("CURRENT LIBRARY CATALOG")
    print("="*50)
    
    results = inventory.display_all()
    if results[0] == "The inventory is empty.":
        print(results[0])
    else:
        for i, detail in enumerate(results, 1):
            print(f"{i}. {detail}")
    print("="*50)

def search_book_cli(inventory: LibraryInventory):
    print("\n--- Search Book ---")
    
    try:
        print("Search by: (1) Title | (2) ISBN")
        choice = input("Enter choice (1/2): ").strip()
        
        if choice == '1':
            query = input("Enter part of the Title to search: ").strip()
            if not query:
                raise ValueError("Search query cannot be empty.")
            
            results = inventory.search_by_title(query)
            
            if results:
                print(f"\nFound {len(results)} book(s) matching '{query}':")
                for i, book in enumerate(results, 1):
                    print(f"{i}. {book.get_details()}")
            else:
                print(f"ERROR: No books found matching title '{query}'.")
                
        elif choice == '2':
            query = input("Enter the full ISBN: ").strip()
            if not query:
                raise ValueError("ISBN query cannot be empty.")
                
            book = inventory.search_by_isbn(query)
            
            if book:
                print("\nFound book:")
                print(book.get_details())
            else:
                print(f"ERROR: No book found with ISBN '{query}'.")
                
        else:
            print("ERROR: Invalid search choice.")
            
    except Exception as e:
        print(f"Search operation failed: {e}")

def main():
    inventory = LibraryInventory()
    
    running = True
    while running:
        display_menu()
        
        try:
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == '1':
                add_book_cli(inventory)
            elif choice == '2':
                issue_return_book_cli(inventory, 'issue')
            elif choice == '3':
                issue_return_book_cli(inventory, 'return')
            elif choice == '4':
                view_all_cli(inventory)
            elif choice == '5':
                search_book_cli(inventory)
            elif choice == '6':
                print("\nSaving catalog and exiting...")
                inventory.save_catalog()
                print("Goodbye!")
                running = False 
            else:
                print("\nWARNING: Invalid choice. Please enter a number between 1 and 6.")
        
        except KeyboardInterrupt:
            print("\n\nProgram interrupted. Saving catalog and exiting...")
            inventory.save_catalog()
            running = False
        except Exception as e:
            print(f"\n\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Fatal error before main execution: {e}")




    
        
    