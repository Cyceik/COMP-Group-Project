This guide is meant to walk you through the process of installing and using the Restaurant Ordering System

1. Prerequisites
Make sure that you have Python 3 installed. In addition, you will have to download the following third party packages using the terminal or the command line interface:
pandas: To read the menu data from Excel.
openpyxl: Package that is required by pandas for parsing `.xlsx` files.
pytz: To handle the time zones used in the menu timer in Hong Kong.

2. Files Preparation
These files are required by the application in order to work properly:
Script File: Make sure you save the Python code file as `Latest..py`.
Excel Database: The menu database should be stored in the form of an Excel file called `menu_data.xlsx` in `W:\comp gp project\menu_data.xlsx`. 
Note: The path should be updated in case the Excel file is stored at a different location. Look for Line 318 in the script.


3. Program Launching
Open your terminal or IDE (such as VS Code or PyCharm).
Change directory into where you saved `Latest..py`.
Use this command to launch the application:


4. Initial Setup Steps
After launching the app, there are three required screens you need to complete:

1.Language selection window. Pick between the following options: Traditional Chinese (繁體中文), Simplified Chinese (简体中文), or English.
2.Student status selection window. Choose either "Yes" or "No" option. If the option "Yes" is picked, a 10% discount is applied on relevant items.

3.Order type window. Pick whether you would like to dine "In restaurant" or make "Take Away" order.（If you select Dine In, you must enter a Table Number before confirming.）


5. App Features
Time-Based Menu: The menu changes according to the time in Hong Kong (e.g. Breakfast menu is shown from 06:00-10:59, and lunch menu appears at 11:00-13:59).
 
Search & Filtering: Use the search bar or choose from category icons (such as Main Course, Appetizer, etc.) to filter out items from the list.

Favorites Feature: Press the star icon near each item in order to save your favorite
dishes, and access them by pressing the "★ Favorites" button.
Coupon Codes: Enter the following coupon codes in the "Cart" tab: `WELCOME10` $10 off; `STUDENT20` - $20 off.

Admin Panel: Press the "Admin" button and provide the password `admin123` in order to access sales statistics information.
