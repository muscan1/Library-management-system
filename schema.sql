-- First, create the database (like creating a new folder)
CREATE DATABASE library_db;

-- Tell MySQL to use this database
USE library_db;


-- TABLE 1: users
-- Stores everyone who signs up
CREATE TABLE users (
    id          INT AUTO_INCREMENT PRIMARY KEY,  -- a unique number for each person (1, 2, 3...)
    first_name  VARCHAR(100),                    -- their first name
    last_name   VARCHAR(100),                    -- their last name
    admission   VARCHAR(50) UNIQUE,              -- their school/library ID (no duplicates)
    email       VARCHAR(255) UNIQUE,             -- their email (no duplicates)
    password    VARCHAR(255),                    -- their password (stored scrambled for safety)
    joined_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- the date they signed up
);


-- TABLE 2: books
-- Stores every book in the library
CREATE TABLE books (
    id        INT AUTO_INCREMENT PRIMARY KEY,  -- a unique number for each book
    title     VARCHAR(255),                   -- the book's title
    author    VARCHAR(255),                   -- who wrote it
    isbn      VARCHAR(20) UNIQUE,             -- the book's unique barcode number
    category  VARCHAR(100),                   -- e.g. Fiction, Science, History
    copies    INT DEFAULT 1,                  -- how many copies the library has
    added_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- when the book was added
);


-- TABLE 3: borrow_logs
-- Records every time someone borrows a book
CREATE TABLE borrow_logs (
    id          INT AUTO_INCREMENT PRIMARY KEY,  -- a unique number for each borrow record
    book_id     INT,                             -- which book was borrowed (links to books table)
    user_id     INT,                             -- who borrowed it (links to users table)
    issue_date  DATE,                            -- the day they borrowed it
    status      VARCHAR(20) DEFAULT 'Active',    -- Active, Returned, or Overdue

    -- These two lines connect borrow_logs to the other two tables
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);