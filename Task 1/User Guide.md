# Restaurant Ordering System

This guide is designed to walk you through the process of installing and using the **Restaurant Ordering System**, a Python-based GUI application for managing restaurant orders with real-time menu updates and administrative tracking.

---

## 1. Prerequisites

Before running the application, ensure you have **Python 3** installed. You will also need to install several third-party libraries used for data handling and time zone management.

Open your terminal or command prompt and run:

```bash
pip install pandas openpyxl pytz
```

* **pandas**: Used to read and process menu data from Excel.
* **openpyxl**: Required by pandas for parsing `.xlsx` files.
* **pytz**: Handles Hong Kong time zones for the dynamic menu timer.

---

## 2. Files Preparation

To ensure the application works properly, prepare the following files:

* **Script File**: Save the Python code as `Latest..py`.
* **Excel Database**: The system expects a file named `menu_data.xlsx` located at:
    `W:\comp gp project\menu_data.xlsx`
    
> [!IMPORTANT]
> If your Excel file is stored in a different location, you **must** update the file path. Open `Latest..py`, go to **Line 318**, and change the path string to match your local directory.

---

## 3. Program Launching

1.  Open your terminal or a preferred IDE (such as **VS Code** or **PyCharm**).
2.  Navigate (Change Directory) to the folder where you saved `Latest..py`.
3.  Run the application using the following command:

```bash
python "Latest..py"
```

---

## 4. Initial Setup Steps

Upon launching the app, you must complete three configuration screens:

1.  **Language Selection**: Choose between **Traditional Chinese (繁體中文)**, **Simplified Chinese (简体中文)**, or **English**.
2.  **Student Status**: Choose **Yes** or **No**. Selecting "Yes" applies an automatic **10% discount** to eligible items.
3.  **Order Type**: Select **Dine In** or **Take Away**. 
    * *Note: If you select **Dine In**, you will be prompted to enter a **Table Number** before proceeding.*

---

## 5. App Features

### 🕒 Time-Based Menu
The menu automatically synchronizes with Hong Kong local time. The available items change dynamically:
* **Breakfast**: 06:00 – 10:59
* **Lunch**: 11:00 – 13:59
* *And so on for Afternoon Tea and Dinner.*

### 🔍 Search & Filtering
* **Search Bar**: Type keywords to find specific dishes.
* **Category Icons**: Quickly filter items by categories like *Main Course*, *Appetizer*, *Beverage*, etc.

### ⭐ Favorites Feature
* Click the **star icon** next to any dish to save it to your personal favorites.
* Toggle the **"★ Favorites"** button to filter the menu and show only your saved items.

### 🎫 Coupon Codes
Apply discounts in the **Cart** tab using these codes:
* `WELCOME10`: $10 fixed discount.
* `STUDENT20`: $20 fixed discount.
* `SAVE15`: 15% off your total.

### 🔐 Admin Panel
Access the management backend by clicking the **"Admin"** button. 
* **Password**: `admin123`
* **Capabilities**: View real-time sales statistics, top 10 popular items, and update order statuses (Pending, Preparing, Ready, Completed).

---

## Technical Implementation Details

For developers interested in the architecture:
* **Data Structure**: Uses **Hash Sets** for $O(1)$ favorite lookups and **DataFrames** for initial Excel parsing.
* **Algorithm**: Employs **Regular Expression (Regex)** pattern matching for phone number validation (`r'^\d{8}$'`) and **Greedy Logic** for coupon calculations and top-item sorting.
