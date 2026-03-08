[README.md](https://github.com/user-attachments/files/25821881/README.md)
# 🍽️ Restaurant Multi-language Ordering System

An interactive GUI-based ordering system developed in Python. This project fulfills the requirements for the **COMP2090SEF** course, focusing on a user-friendly interface, automated discount logic, and dynamic content management.

## 📋 Project Requirements Checklist

Based on the official project specifications, this application implements:


* **Multi-language Support**: Fully localized in English, Traditional Chinese, and Simplified Chinese.



* **Dynamic Menus**: Time-dependent menu availability (Breakfast, Lunch, Tea, Dinner).



* **Automated Discounting**: Integrated 10% discount for students.



* **Smart Cart Logic**: Automatic "Buy one get one free" (BOGO) beverage offers for main courses.



* **Robust Validation**: Input validation for quantities and 8-digit phone numbers.



## ⭐ Key Features

### 1. Intelligent Time-Based Filtering

The system automatically detects the current **Hong Kong Time (HKT)** and presents the appropriate menu:
| Period | Menu Type | Logic |
| :--- | :--- | :--- |
| **06:00 - 11:00** | Breakfast | Standard morning offerings. |
| **11:00 - 14:00** | Lunch | Mid-day specials. |
| **14:00 - 18:00** | Afternoon Tea | Includes a mix of Tea and Lunch menus. |
| **18:00 - 22:00** | Dinner | Evening menu. |


### 2. Discount & Promotion Engine

* **Student Benefit**: Users can select their status at startup. If "Student" is chosen, a $10\%$ discount is applied to all applicable items, with totals rounded to the nearest integer.


* **Free Beverage Offer**: Adding a `main_course` or `combo` triggers a pop-up window allowing the user to select one free beverage from the current menu.



### 3. Data-Driven Architecture

The application separates logic from data. All dish information, pricing, and category tags are managed via `menu_data.xlsx`, allowing for easy menu updates without touching the Python code.

## 🛠️ Installation & Setup

### Prerequisites

* **Python 3.x**
* Required Libraries:
```bash
pip install pandas openpyxl pytz

```



### Running the Application

1. Ensure `menu_data.xlsx` is in the same directory as the script.


2. Execute the script:
```bash
python COMP_Project_Coding.py

```



## 📁 File Structure


* `COMP_Project_Coding.py`: The main application logic and Tkinter GUI implementation.



* `menu_data.xlsx`: The database containing item IDs, multilingual names, prices, and time-slots.



## 📝 User Instructions

 
1. **Language Selection**: Choose your preferred language on the splash screen.



2. **Verify Status**: Identify as a student to unlock specific discounts.


3. **Ordering**: Browse the scrollable menu. Adjust quantities and add items to your cart.



4. **Checkout**: Enter your name and an **8-digit phone number** to generate a final receipt.
