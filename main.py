import sqlite3
from datetime import date, timedelta

# ---------- OOP CLASSES ----------

class Book:
    def __init__(self, id, title, author, qty):
        self.id, self.title, self.author, self.qty = id, title, author, qty


class Member:
    def __init__(self, id, name):
        self.id, self.name = id, name


class Student(Member):                         # Inheritance
    def __init__(self, id, name, course, password):
        super().__init__(id, name)
        self.course, self.password = course, password


class Library:
    def __init__(self):
        self.con = sqlite3.connect("library.db")
        self.cur = self.con.cursor()
        self.setup()

    def setup(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS books(
            id INTEGER PRIMARY KEY, title TEXT, author TEXT,
            qty INTEGER, available INTEGER)""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY, name TEXT, course TEXT,
            password TEXT)""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS issues(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER, student_id INTEGER,
            issue_date TEXT, due_date TEXT,
            return_date TEXT, fine INTEGER DEFAULT 0,
            status TEXT)""")

        self.con.commit()

    # ---------- BOOK FUNCTIONS ----------

    def add_book(self):
        try:
            b = Book(int(input("Book ID: ")),
                     input("Title: "),
                     input("Author: "),
                     int(input("Quantity: ")))

            self.cur.execute(
                "INSERT INTO books VALUES(?,?,?,?,?)",
                (b.id, b.title, b.author, b.qty, b.qty))
            self.con.commit()
            print("Book added successfully.")
        except:
            print("Invalid input or Book ID already exists.")

    def books(self):
        self.cur.execute("SELECT * FROM books")
        data = self.cur.fetchall()

        if not data:
            print("No books found.")
            return

        print("\nID | Title | Author | Total | Available")
        for b in data:
            print(b[0], "|", b[1], "|", b[2], "|", b[3], "|", b[4])

    def search(self):
        key = input("Search title/author: ")
        self.cur.execute(
            "SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
            (f"%{key}%", f"%{key}%"))
        data = self.cur.fetchall()

        for b in data:
            print(b[0], "|", b[1], "|", b[2], "| Available:", b[4])

        if not data:
            print("Book not found.")

    # ---------- STUDENT FUNCTIONS ----------

    def register(self):
        try:
            s = Student(int(input("Student ID: ")),
                        input("Name: "),
                        input("Course: "),
                        input("Password: "))

            self.cur.execute(
                "INSERT INTO students VALUES(?,?,?,?)",
                (s.id, s.name, s.course, s.password))
            self.con.commit()
            print("Registration successful.")
        except:
            print("Invalid input or Student ID already exists.")

    def login(self):
        try:
            sid = int(input("Student ID: "))
            password = input("Password: ")

            self.cur.execute(
                "SELECT * FROM students WHERE id=? AND password=?",
                (sid, password))

            if self.cur.fetchone():
                print("Login successful.")
                self.student_menu(sid)
            else:
                print("Invalid login.")
        except:
            print("Invalid input.")

    # ---------- ISSUE / RETURN ----------

    def issue(self, sid):
        try:
            bid = int(input("Book ID: "))

            self.cur.execute("SELECT * FROM books WHERE id=?", (bid,))
            book = self.cur.fetchone()

            if not book:
                print("Book not found.")
                return

            if book[4] == 0:
                print("Book unavailable.")
                return

            self.cur.execute(
                """SELECT * FROM issues
                   WHERE book_id=? AND student_id=? AND status='Issued'""",
                (bid, sid))

            if self.cur.fetchone():
                print("You already have this book.")
                return

            today = date.today()
            due = today + timedelta(days=14)

            self.cur.execute(
                """INSERT INTO issues
                (book_id,student_id,issue_date,due_date,status)
                VALUES(?,?,?,?,?)""",
                (bid, sid, str(today), str(due), "Issued"))

            self.cur.execute(
                "UPDATE books SET available=available-1 WHERE id=?", (bid,))
            self.con.commit()

            print("Book issued.")
            print("Due date:", due)

        except:
            print("Invalid input.")

    def return_book(self, sid):
        try:
            bid = int(input("Book ID: "))

            self.cur.execute(
                """SELECT * FROM issues
                   WHERE book_id=? AND student_id=? AND status='Issued'""",
                (bid, sid))

            record = self.cur.fetchone()

            if not record:
                print("You have not issued this book.")
                return

            due = date.fromisoformat(record[4])
            today = date.today()
            fine = max(0, (today - due).days * 5)

            self.cur.execute(
                """UPDATE issues
                   SET return_date=?, fine=?, status='Returned'
                   WHERE id=?""",
                (str(today), fine, record[0]))

            self.cur.execute(
                "UPDATE books SET available=available+1 WHERE id=?", (bid,))
            self.con.commit()

            print("Book returned.")
            print("Fine: ₹", fine)

        except:
            print("Invalid input.")

    def my_books(self, sid):
        self.cur.execute(
            """SELECT books.title, issues.issue_date, issues.due_date
               FROM issues JOIN books ON issues.book_id=books.id
               WHERE issues.student_id=? AND issues.status='Issued'""",
            (sid,))

        data = self.cur.fetchall()

        if not data:
            print("No books issued.")
        else:
            for b in data:
                print("Book:", b[0], "| Issue:", b[1], "| Due:", b[2])

    # ---------- MENUS ----------

    def admin_menu(self):
        while True:
            print("""
--- ADMIN ---
1. Add Book
2. View Books
3. Search Book
4. Logout
""")
            ch = input("Choice: ")

            if ch == "1": self.add_book()
            elif ch == "2": self.books()
            elif ch == "3": self.search()
            elif ch == "4": break
            else: print("Invalid choice.")

    def student_menu(self, sid):
        while True:
            print("""
--- STUDENT ---
1. View Books
2. Search Book
3. Issue Book
4. Return Book
5. My Books
6. Logout
""")
            ch = input("Choice: ")

            if ch == "1": self.books()
            elif ch == "2": self.search()
            elif ch == "3": self.issue(sid)
            elif ch == "4": self.return_book(sid)
            elif ch == "5": self.my_books(sid)
            elif ch == "6": break
            else: print("Invalid choice.")


# ---------- MAIN PROGRAM ----------

lib = Library()

while True:
    print("""
================================
     LIBRARY MANAGEMENT SYSTEM
================================
1. Admin Login
2. Student Login
3. Student Registration
4. Exit
""")

    choice = input("Enter choice: ")

    if choice == "1":
        u = input("Username: ")
        p = input("Password: ")

        if u == "admin" and p == "admin123":
            lib.admin_menu()
        else:
            print("Invalid admin login.")

    elif choice == "2":
        lib.login()

    elif choice == "3":
        lib.register()

    elif choice == "4":
        print("Thank you!")
        break

    else:
        print("Invalid choice.")