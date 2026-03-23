# Local Inventory CRM Dashboard

A lightweight, database-free inventory management dashboard built with Python and Flet. Instead of relying on SQL, this application uses a simple, flat text file (`.txt`) to store all your product records. It's perfect for quick, portable tracking without any complex setup.

## Features
* **Create Records:** Add new products with their respective quantities and prices.
* **Read Data:** View all inventory items in a structured, dynamically updating data table.
* **Delete Records:** Remove items from your inventory with a single click using the built-in trash icon.
* **Flat-File Storage:** All data is safely written to a local `inventory.txt` file using pipe-separated values, making it incredibly easy to open and read even without the app.
* **Input Validation:** Prevents the submission of empty fields or invalid text in numeric columns.

## Requirements
* Python 3.x
* Flet library

## How to Run

Install the required Flet library:
 pip install flet
