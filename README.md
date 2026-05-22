# Library-management-system
CREATORS: Jane, Lynn, Susan, Paul, Morgan, Muscan


A modern, responsive, and lightweight Library Management System built with a **Flask (Python)** backend, a **MySQL** database, and a vanilla **HTML5 / CSS3 / JavaScript** frontend. 

This system provides a seamless experience for library users to browse books, register accounts, and borrow titles dynamically, alongside an intuitive interface for administrators to add new books to the database.

---

## 🚀 Features

### 👤 User Authentication & Management
* **Secure Signup:** Registers first name, last name, unique admission/library ID, and email. Passwords are securely hashed before database storage using `bcrypt`.
* **Secure Login:** Authenticates users via email and verified cryptographically hashed passwords.
* **Persistent Sessions:** Tracks logged-in users using HTML5 `localStorage` to personalize the application experience.

### 📖 Book Catalog & Inventory Control
* **Dynamic Catalog:** Fetches and displays a responsive grid of available books in real time.
* **Inventory Tracking:** Displays real-time stock counts. Elements dynamically adjust badge color notifications (`status-available` vs. `no-copies`) based on quantity fields.
* **Smart Action Toggles:** Automatically disables transaction elements when copies reach zero, preventing inventory deficits.

### 🔄 Borrowing System Logs
* **Automated Verification:** Validates copy availability server-side before approving logs.
* **Log Book Automation:** Automatically deducts one unit from the available inventory and creates an entry inside the tracking ledger, auto-stamping it with the transaction issue date.

### 📱 Responsive User Interface
* **Unified UI Views:** Uses responsive CSS media queries to smoothly transition between a clean desktop grid environment and an optimized mobile navigation drawer (Hamburger Sidebar).
* **Dynamic View Switcher:** Swaps transaction forms inline instantly with animated left-pointing back arrows without forcing browser screen refreshes.

---

## 🛠️ Tech Stack & Architecture

The application implements a decoupled client-server architecture:

* **Frontend:** HTML5, CSS3 (including CSS Variables, Flexbox, Custom Keyframes), and Vanilla JavaScript (ES6+ Async/Await Fetch API).
* **Backend:** Python 3, Flask RESTful Routing, Flask-CORS (Cross-Origin Resource Sharing).
* **Database:** MySQL Server (relational schema design utilizing `FOREIGN KEY` constraints, `AUTO_INCREMENT` primaries, and index optimization mapping).
* **Security:** `bcrypt` password salting and hashing, environment variable isolation.

---

## 📁 Project Structure

```text
├── app.py              # Flask REST API Server & Static Routing Configuration
├── schema.sql          # MySQL Relational Database Layout & Tables Setup
├── index.html          # Dynamic Library Book Catalog & Main Dashboard Portal
├── Dashboard.html      # Multi-panel Administrative Panel (Add Book & Borrow System)
├── script.js           # Catalog Filtering, Search, and Pagination Controller
├── .env                # Local Environment Database Configuration Secrets (Ignored)
└── README.md           # Project Documentation & System Setup Instructions
