This user guide explains how to integrate and use the two specific code modules you provided: **Menu Data Loading (DataFrame)** and **Customer Input Validation (Regex)**.

---

### 1. Module: Menu Data Loading (DataFrame)
This module uses the `pandas` library to transform static Excel data into a dynamic Python list, which acts as the "brain" for your application's menu.

#### **How to use it:**
* **Requirements:** Ensure you have `pandas` and `openpyxl` installed (`pip install pandas openpyxl`).
* **File Placement:** The code expects an Excel file located at `W:\comp gp project\menu_data.xlsx`.
* **Implementation:** The `create_menu` function reads the spreadsheet, converts the entire table into a list, and stores it in the global `menu` variable.

#### **Understanding the Data Flow:**


* **Why use this?** By using a `DataFrame`, you can easily manipulate large amounts of menu data (prices, descriptions, categories) in Excel, which is much faster than hard-coding items into your Python script.

---

### 2. Module: Customer Input Validation (Regex)
This module uses the `re` (Regular Expression) library to ensure that data entered by the customer during the checkout process is valid before it is submitted to the system.

#### **How to use it:**
* **Triggering:** The validation occurs inside the `checkout(self)` function.
* **Logic:** It specifically checks the `phone_entry` field.
* **The Pattern:** `r'^\d{8}$'`
    * `^` : Starts the check at the very beginning of the string.
    * `\d{8}` : Ensures the user has typed **exactly 8 digits**.
    * `$` : Ensures the check ends at the end of the string (preventing extra characters).

#### **Regex Pattern Visualized:**


* **Why use this?** This prevents "dirty data" from entering your system. By forcing an 8-digit format, you ensure that order records remain clean and that the contact information is consistently formatted for administrative use.

---

### Summary Table for Implementation

| Feature | Library | Function | Purpose |
| :--- | :--- | :--- | :--- |
| **Menu Loading** | `pandas` | `create_menu` | Converts Excel database into an application-ready list. |
| **Input Validation** | `re` | `checkout` | Ensures user phone number is exactly 8 digits. |

### **Integration Tip**
To use these together in your main application, ensure:
1.  **Imports are at the top:** Include `import pandas as pd` and `import re` at the very beginning of your main script.
2.  **Global Scope:** Keep `menu`, `cart`, and `orders` as global variables so that the menu loaded by the `DataFrame` module remains accessible to the `checkout` module when it processes orders.
