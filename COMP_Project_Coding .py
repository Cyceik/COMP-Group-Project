# pip3 install pandas
# pip3 install openpyxl
import tkinter as tk # GUI
from tkinter import ttk, messagebox, simpledialog # message # error # input
import pandas as pd # data 
import datetime # time
import re # allow different district change time
import pytz # allow change the time

# Variable
text = {}  # store language
is_student = False  # student id 
menu = []  
cart = []  
orders = []  # order history
order_number = 0  # order number
current_menu_type = ""  # menu type breakfast lunch tea dinner
secondary_menu_type = ""  # 
current_language = "en"  # current language eng
free_beverage_map = {}  # free drink

class RestaurantApp:
    def __init__(self, master):
        self.master = master
        self.master.configure(bg="#f0f0f0")
        
        # choose of language
        self.select_language()
        
        # student identify
        self.select_student_status()
        
        # data of menu
        if not self.create_menu():
            messagebox.showerror("Error", "Failed to load menu data")
            self.master.destroy()
            return
        
        # get the time
        self.update_current_menu()
        
        # GUI
        self.create_widgets()
        self.update_menu_display()
        
    def select_language(self):
        """選擇語言"""
        global text, current_language
        
        # GUI language
        language_window = tk.Toplevel(self.master)
        language_window.title("Select Language / 選擇語言 / 选择语言")
        language_window.geometry("500x250")  # size of GUI
        language_window.transient(self.master)
        language_window.grab_set()
        language_window.protocol("WM_DELETE_WINDOW", lambda: None)
        
        label = tk.Label(language_window, text="Please select your preferred language:\n請選擇您的首選語言:\n请选择您的首选语言:", 
                        font=("Arial", 14))  # size of words
        label.pack(pady=20)  
        
        # language button
        btn_frame = tk.Frame(language_window)
        btn_frame.pack(pady=30)  
        
        def set_language(lang):
            global text, current_language
            current_language = lang
            if lang == "tc": # traditional chinese
                self.load_traditional_chinese()
            elif lang == "sc": # simplified chinese
                self.load_simplified_chinese()
            else: # default english
                self.load_english()
            language_window.destroy()
        
        tc_btn = tk.Button(btn_frame, text="繁體中文", width=15, height=2,  # szie of button
                        font=("Arial", 12),  # size of words
                        command=lambda: set_language("tc"))
        tc_btn.grid(row=0, column=0, padx=15)  # distance
        
        sc_btn = tk.Button(btn_frame, text="简体中文", width=15, height=2,  
                        font=("Arial", 12),  
                        command=lambda: set_language("sc"))
        sc_btn.grid(row=0, column=1, padx=15)  
        
        en_btn = tk.Button(btn_frame, text="English", width=15, height=2,  
                        font=("Arial", 12),  
                        command=lambda: set_language("en"))
        en_btn.grid(row=0, column=2, padx=15)  
        
        # middle
        self.center_window(language_window)
        
        self.master.wait_window(language_window)
    
    def center_window(self, window):
        """將窗口居中顯示"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    def load_traditional_chinese(self):
        """加載繁體中文"""
        global text
        text = {
            "welcome": "歡迎光臨餐廳點餐系統",
            "menu": "菜單",
            "cart": "購物車",
            "orders": "訂單",
            "student": "學生",
            "non_student": "非學生",
            "student_discount": "學生可享有9折優惠",
            "student_status": "學生狀態",
            "current_time": "當前時間",
            "breakfast_menu": "早餐菜單",
            "lunch_menu": "午餐菜單",
            "afternoon_tea_menu": "下午茶菜單",
            "dinner_menu": "晚餐菜單",
            "main_course": "主食",
            "side_dish": "配菜",
            "beverage": "飲品",
            "dessert": "甜品",
            "combo": "套餐",
            "appetizer": "前菜",
            "view_menu": "查看菜單",
            "view_cart": "查看購物車",
            "view_orders": "查看訂單",
            "add_to_cart": "加入購物車",
            "quantity": "數量",
            "quantity_error": "數量必須大於0",
            "added": "已加入購物車",
            "cart_empty": "購物車為空",
            "delete_item": "刪除商品",
            "modify_quantity": "修改數量",
            "edit_customization": "編輯定制選項",
            "enter_quantity": "請輸入數量：",
            "updated": "已更新",
            "deleted": "已刪除",
            "total": "總計",
            "checkout": "結帳",
            "enter_name": "請輸入姓名：",
            "enter_phone": "請輸入電話號碼：",
            "invalid_phone": "無效的電話號碼，請輸入8位數字",
            "order_success": "訂單成功！",
            "order_number": "訂單編號",
            "customer_name": "客戶姓名",
            "customer": "客戶",
            "contact_phone": "聯絡電話",
            "phone": "電話",
            "order_items": "訂單商品",
            "order_total": "訂單總計",
            "status": "狀態",
            "pending": "處理中",
            "payment_instruction": "請到櫃檯付款並領取您的訂單",
            "no_orders": "沒有訂單記錄",
            "order_history": "訂單歷史",
            "student_question": "您是學生嗎？",
            "yes": "是",
            "no": "否",
            "customize_item": "定制商品",
            "customize_prompt": "您想要定制這個商品嗎?",
            "sweet": "甜度",
            "ice": "冰量",
            "spicy": "辣度",
            "full": "全",
            "half": "半",
            "less": "少",
            "no_ice": "走冰",
            "hot": "熱",
            "normal": "正常",
            "mild": "微辣",
            "medium": "中辣",
            "extra_spicy": "特辣",
            "original_price": "原價",
            "discount_price": "折扣價",
            "excel_load_error": "無法加載菜單數據",
            "free_beverage": "免費飲料",
            "select_beverage": "請選擇一款免費飲料",
            "select": "選擇",
            "cancel": "取消",
            "free_item": "免費",
            "confirm": "確認",
            "free_with_main": "與主餐一起贈送"
        }
    
    def load_simplified_chinese(self):
        """加载简体中文文本"""
        global text
        text = {
            "welcome": "欢迎光临餐厅点餐系统",
            "menu": "菜单",
            "cart": "购物车",
            "orders": "订单",
            "student": "学生",
            "non_student": "非学生",
            "student_discount": "学生可享有9折优惠",
            "student_status": "学生状态",
            "current_time": "当前时间",
            "breakfast_menu": "早餐菜单",
            "lunch_menu": "午餐菜单",
            "afternoon_tea_menu": "下午茶菜单",
            "dinner_menu": "晚餐菜单",
            "main_course": "主食",
            "side_dish": "配菜",
            "beverage": "饮品",
            "dessert": "甜品",
            "combo": "套餐",
            "appetizer": "前菜",
            "view_menu": "查看菜单",
            "view_cart": "查看购物车",
            "view_orders": "查看订单",
            "add_to_cart": "加入购物车",
            "quantity": "数量",
            "quantity_error": "数量必须大于0",
            "added": "已加入购物车",
            "cart_empty": "购物车为空",
            "delete_item": "删除商品",
            "modify_quantity": "修改数量",
            "edit_customization": "编辑定制选项",
            "enter_quantity": "请输入数量：",
            "updated": "已更新",
            "deleted": "已删除",
            "total": "总计",
            "checkout": "结账",
            "enter_name": "请输入姓名：",
            "enter_phone": "请输入电话号码：",
            "invalid_phone": "无效的电话号码，请输入8位数字",
            "order_success": "订单成功！",
            "order_number": "订单编号",
            "customer_name": "客户姓名",
            "customer": "客户",
            "contact_phone": "联系电话",
            "phone": "电话",
            "order_items": "订单商品",
            "order_total": "订单总计",
            "status": "状态",
            "pending": "处理中",
            "payment_instruction": "请到柜台付款并领取您的订单",
            "no_orders": "没有订单记录",
            "order_history": "订单历史",
            "student_question": "您是学生吗？",
            "yes": "是",
            "no": "否",
            "customize_item": "定制商品",
            "customize_prompt": "您想要定制这个商品吗?",
            "sweet": "甜度",
            "ice": "冰量",
            "spicy": "辣度",
            "full": "全",
            "half": "半",
            "less": "少",
            "no_ice": "走冰",
            "hot": "热",
            "normal": "正常",
            "mild": "微辣",
            "medium": "中辣",
            "extra_spicy": "特辣",
            "original_price": "原价",
            "discount_price": "折扣价",
            "excel_load_error": "无法加载菜单数据",
            "free_beverage": "免费饮料",
            "select_beverage": "请选择一款免费饮料",
            "select": "选择",
            "cancel": "取消",
            "free_item": "免费",
            "confirm": "确认",
            "free_with_main": "与主餐一起赠送"
        }
    
    def load_english(self):
        """Load English text"""
        global text
        text = {
            "welcome": "Welcome to Restaurant Ordering System",
            "menu": "Menu",
            "cart": "Cart",
            "orders": "Orders",
            "student": "Student",
            "non_student": "Non-student",
            "student_discount": "Students receive a 10% discount",
            "student_status": "Student Status",
            "current_time": "Current Time",
            "breakfast_menu": "Breakfast Menu",
            "lunch_menu": "Lunch Menu",
            "afternoon_tea_menu": "Afternoon Tea Menu",
            "dinner_menu": "Dinner Menu",
            "main_course": "Main Course",
            "side_dish": "Side Dish",
            "beverage": "Beverage",
            "dessert": "Dessert",
            "combo": "Combo",
            "appetizer": "Appetizer",
            "view_menu": "View Menu",
            "view_cart": "View Cart",
            "view_orders": "View Orders",
            "add_to_cart": "Add to Cart",
            "quantity": "Quantity",
            "quantity_error": "Quantity must be greater than 0",
            "added": "Added to Cart",
            "cart_empty": "Your cart is empty",
            "delete_item": "Delete Item",
            "modify_quantity": "Modify Quantity",
            "edit_customization": "Edit Customization",
            "enter_quantity": "Enter quantity:",
            "updated": "Updated",
            "deleted": "Deleted",
            "total": "Total",
            "checkout": "Checkout",
            "enter_name": "Enter your name:",
            "enter_phone": "Enter your phone number:",
            "invalid_phone": "Invalid phone number. Please enter 8 digits",
            "order_success": "Order Success!",
            "order_number": "Order Number",
            "customer_name": "Customer Name",
            "customer": "Customer",
            "contact_phone": "Contact Phone",
            "phone": "Phone",
            "order_items": "Order Items",
            "order_total": "Order Total",
            "status": "Status",
            "pending": "Pending",
            "payment_instruction": "Please proceed to the counter to pay and pick up your order",
            "no_orders": "No order history",
            "order_history": "Order History",
            "student_question": "Are you a student?",
            "yes": "Yes",
            "no": "No",
            "customize_item": "Customize Item",
            "customize_prompt": "Would you like to customize this item?",
            "sweet": "Sweetness",
            "ice": "Ice",
            "spicy": "Spiciness",
            "full": "Full",
            "half": "Half",
            "less": "Less",
            "no_ice": "No Ice",
            "hot": "Hot",
            "normal": "Normal",
            "mild": "Mild",
            "medium": "Medium",
            "extra_spicy": "Extra Spicy",
            "original_price": "Original Price",
            "discount_price": "Discount Price",
            "excel_load_error": "Failed to load menu data",
            "free_beverage": "Free Beverage",
            "select_beverage": "Please select a free beverage",
            "select": "Select",
            "cancel": "Cancel",
            "free_item": "Free",
            "confirm": "Confirm",
            "free_with_main": "Free with main course"
        }
    
    def select_student_status(self):
        """選擇學生狀態"""  # student discount
        global is_student
        
        # window size
        student_window = tk.Toplevel(self.master)
        student_window.title(text.get("student_question", "Are you a student?"))
        student_window.geometry("400x200")  
        student_window.transient(self.master)
        student_window.grab_set()
        student_window.protocol("WM_DELETE_WINDOW", lambda: None)
        
        label = tk.Label(student_window, text=text.get("student_question", "Are you a student?"), 
                        font=("Arial", 14)) 
        label.pack(pady=20)  
        
        btn_frame = tk.Frame(student_window)
        btn_frame.pack(pady=30)  
        
        yes_btn = tk.Button(btn_frame, text=text.get("yes", "Yes"), width=12, height=2,  
                          font=("Arial", 12),  
                          command=lambda: self.set_student_status(True, student_window))
        yes_btn.grid(row=0, column=0, padx=20)  
        
        no_btn = tk.Button(btn_frame, text=text.get("no", "No"), width=12, height=2, 
                         font=("Arial", 12),  
                         command=lambda: self.set_student_status(False, student_window))
        no_btn.grid(row=0, column=1, padx=20)  
        
        # keep middle
        self.center_window(student_window)
        
        self.master.wait_window(student_window)
    
    def set_student_status(self, status, window):
        """設置學生狀態並關閉窗口"""
        global is_student
        is_student = status
        window.destroy()
    
    def create_menu(self):
        """從Excel創建菜單"""
        global menu
        try:
            df = pd.read_excel("menu_data.xlsx")
            menu = df.values.tolist()
            return True
        except Exception as e:
            print(f"Error loading menu: {e}")
            messagebox.showerror("Error", text.get("excel_load_error", "Failed to load menu data"))
            return False
    
    def update_current_menu(self):
        """Change the menu following by the current time"""
        global current_menu_type, secondary_menu_type
        
        now = self.get_hk_time()
        hour = now.hour

        # open hour
        if 6 <= hour < 11:
            current_menu_type = "breakfast"
            secondary_menu_type = ""
        elif 11 <= hour < 14:
            current_menu_type = "lunch"
            secondary_menu_type = ""
        elif 14 <= hour < 18:
            current_menu_type = "afternoon_tea"
            secondary_menu_type = "lunch"  
        elif 18 <= hour < 22:
            current_menu_type = "dinner"
            secondary_menu_type = ""
        else:
            current_menu_type = "dinner"
            secondary_menu_type = ""
    
    def get_hk_time(self):
        """Hong Kong current time"""
        hk_tz = pytz.timezone('Asia/Hong_Kong')
        return datetime.datetime.now(hk_tz)
    
    def get_current_menu_name(self):
        """獲取當前菜單類型的名稱""" # breakfast lunch tea dinnner
        if current_menu_type == "breakfast":
            return text.get("breakfast_menu", "Breakfast Menu")
        elif current_menu_type == "lunch":
            return text.get("lunch_menu", "Lunch Menu")
        elif current_menu_type == "afternoon_tea":
            return text.get("afternoon_tea_menu", "Afternoon Tea Menu")
        elif current_menu_type == "dinner":
            return text.get("dinner_menu", "Dinner Menu")
        return ""
    
    def get_category_name(self, item_type):
        """獲取菜品類別名稱"""
        if item_type == "main_course":
            return text.get("main_course", "Main Course")
        elif item_type == "side_dish":
            return text.get("side_dish", "Side Dish")
        elif item_type == "beverage":
            return text.get("beverage", "Beverage")
        elif item_type == "dessert":
            return text.get("dessert", "Dessert")
        elif item_type == "combo":
            return text.get("combo", "Combo")
        elif item_type == "appetizer":
            return text.get("appetizer", "Appetizer")
        return item_type
    
    def get_item_name(self, item):
        """根據當前語言獲取菜品名稱"""
        global current_language
        
        if current_language == "tc":  # traditional chinese
            return item[1]
        elif current_language == "sc":  # simplified chinese
            return item[2]
        else:  # eng
            return item[3]
    
    def get_price(self, original_price):
        """根據學生狀態""" # student discount
        if is_student:
            student_discount = 0.9
            return round(original_price * student_discount)  # 10% out round off 4out5in
        return original_price
    
    def create_widgets(self):
        """創建主界面"""
        # board GUI
        info_frame = tk.Frame(self.master, bg="#e0e0e0", padx=10, pady=10)
        info_frame.pack(fill=tk.X, pady=10)
        
        # showing welcome
        welcome_label = tk.Label(info_frame, text=text.get('welcome', 'Welcome'), 
                              font=("Arial", 16, "bold"), bg="#e0e0e0")
        welcome_label.pack()
        
        # current1time student y/n
        now = self.get_hk_time()
        time_label = tk.Label(info_frame, 
                           text=f"{text.get('current_time', 'Current Time')}: {now.strftime('%Y-%m-%d %H:%M')}", 
                           bg="#e0e0e0")
        time_label.pack()
        
        student_status = text.get('student', 'Student') if is_student else text.get('non_student', 'Non-student')
        status_label = tk.Label(info_frame, 
                             text=f"{text.get('student_status', 'Student Status')}: {student_status}", 
                             bg="#e0e0e0")
        status_label.pack()
        
        if is_student:
            discount_label = tk.Label(info_frame, 
                                   text=text.get('student_discount', 'Students receive a 10% discount'), 
                                   bg="#e0e0e0", fg="#e74c3c")
            discount_label.pack()
        
        tab_control = ttk.Notebook(self.master)
        
        # tab
        self.menu_tab = ttk.Frame(tab_control)
        self.cart_tab = ttk.Frame(tab_control)
        self.orders_tab = ttk.Frame(tab_control)
        tab_control.add(self.menu_tab, text=text.get('view_menu', 'View Menu'))
        tab_control.add(self.cart_tab, text=text.get('view_cart', 'View Cart'))
        tab_control.add(self.orders_tab, text=text.get('view_orders', 'View Orders'))
        tab_control.pack(expand=1, fill="both")
        self.setup_menu_tab()
        self.setup_cart_tab()
        self.setup_orders_tab()
    
    def setup_menu_tab(self):
        """設置菜單選項"""
        self.menu_type_label = tk.Label(self.menu_tab, text=self.get_current_menu_name(), 
                                    font=("Arial", 14, "bold"))
        self.menu_type_label.pack(pady=10)
        menu_frame = tk.Frame(self.menu_tab)
        menu_frame.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(menu_frame)
        scrollbar = ttk.Scrollbar(menu_frame, orient="vertical", command=canvas.yview)
        self.scrollable_menu = ttk.Frame(canvas)
        
        self.scrollable_menu.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_menu, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def setup_cart_tab(self):
        """設置購物車"""
        # scroll
        cart_frame = tk.Frame(self.cart_tab)
        cart_frame.pack(fill="both", expand=True, padx=20, pady=10)
        cart_title = tk.Label(cart_frame, text=text.get('cart', 'Cart'), font=("Arial", 14, "bold"))
        cart_title.pack(anchor="w", pady=(0, 10))
        
        canvas = tk.Canvas(cart_frame)
        scrollbar = ttk.Scrollbar(cart_frame, orient="vertical", command=canvas.yview)
        self.scrollable_cart = ttk.Frame(canvas)
        self.scrollable_cart.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_cart, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.total_label = tk.Label(self.cart_tab, 
                                text=f"{text.get('total', 'Total')}: $0", 
                                font=("Arial", 12, "bold"))
        self.total_label.pack(anchor="e", padx=20, pady=10)
        
        # checkout
        checkout_frame = tk.Frame(self.cart_tab)
        checkout_frame.pack(fill="x", padx=20, pady=10)
        
        name_label = tk.Label(checkout_frame, text=text.get('enter_name', 'Enter your name:'))
        name_label.grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = tk.Entry(checkout_frame, width=30)
        self.name_entry.grid(row=0, column=1, sticky="w", pady=5)
        
        phone_label = tk.Label(checkout_frame, text=text.get('enter_phone', 'Enter your phone number:'))
        phone_label.grid(row=1, column=0, sticky="w", pady=5)
        self.phone_entry = tk.Entry(checkout_frame, width=30)
        self.phone_entry.grid(row=1, column=1, sticky="w", pady=5)
        
        checkout_btn = tk.Button(checkout_frame, text=text.get('checkout', 'Checkout'),
                              command=self.checkout, bg="#e74c3c", fg="white",
                              padx=20, pady=10)
        checkout_btn.grid(row=2, column=0, columnspan=2, pady=15)
    
    def setup_orders_tab(self):
        """設置訂單"""
        orders_frame = tk.Frame(self.orders_tab)
        orders_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        orders_title = tk.Label(orders_frame, text=text.get('order_history', 'Order History'), 
                             font=("Arial", 14, "bold"))
        orders_title.pack(anchor="w", pady=(0, 10))
        
        canvas = tk.Canvas(orders_frame)
        scrollbar = ttk.Scrollbar(orders_frame, orient="vertical", command=canvas.yview)
        self.scrollable_orders = ttk.Frame(canvas)
        
        self.scrollable_orders.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_orders, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def update_menu_display(self):
        """更新菜單"""
        # clean out current
        for widget in self.scrollable_menu.winfo_children():
            widget.destroy()
        
        # update current menu
        self.menu_type_label.config(text=self.get_current_menu_name())
        
        # get current menu
        filtered_menu = [item for item in menu if item[8] == current_menu_type]
        
        # show lunch during tea time
        if secondary_menu_type == "lunch" and current_menu_type == "afternoon_tea":
            # tea menu
            menu_section_label = ttk.Label(self.scrollable_menu, 
                                         text=text.get('afternoon_tea_menu', 'Afternoon Tea Menu'),
                                         font=("Arial", 12, "bold"))
            menu_section_label.pack(anchor="w", padx=10, pady=5)
            
            self.display_menu_section(filtered_menu)
            
            # add lunch
            separator = ttk.Separator(self.scrollable_menu, orient='horizontal')
            separator.pack(fill='x', padx=10, pady=10)
            
            menu_section_label = ttk.Label(self.scrollable_menu, 
                                         text=text.get('lunch_menu', 'Lunch Menu'),
                                         font=("Arial", 12, "bold"))
            menu_section_label.pack(anchor="w", padx=10, pady=5)
            
            lunch_menu = [item for item in menu if item[8] == "lunch"]
            self.display_menu_section(lunch_menu)
        else:
            self.display_menu_section(filtered_menu)
    
    def display_menu_section(self, menu_items):
        """顯示指定菜單"""
        current_category = ""
        
        for item in menu_items:
            category = self.get_category_name(item[9])
            
            if category != current_category:
                current_category = category
                category_label = ttk.Label(self.scrollable_menu, 
                                         text=f"【{current_category}】",
                                         font=("Arial", 11, "bold"))
                category_label.pack(anchor="w", padx=10, pady=(15, 5))
            
            item_frame = ttk.Frame(self.scrollable_menu)
            item_frame.pack(fill="x", padx=20, pady=2)
            
            # product information
            info_frame = ttk.Frame(item_frame)
            info_frame.pack(side="left")
            
            item_id = item[0]
            name = self.get_item_name(item)
            original_price = item[4]
            price = self.get_price(original_price)
            
            name_label = ttk.Label(info_frame, text=f"{item_id}. {name}")
            name_label.pack(anchor="w")
            
            # show price
            if is_student:
                price_label = ttk.Label(info_frame, 
                                      text=f"{text.get('original_price', 'Original Price')}: ${original_price:.0f} / {text.get('discount_price', 'Discount Price')}: ${price:.0f}")
            else:
                price_label = ttk.Label(info_frame, text=f"${original_price:.0f}")
            
            price_label.pack(anchor="w")
            
            # add to cart
            action_frame = ttk.Frame(item_frame)
            action_frame.pack(side="right")
            
            # quantity
            qty_frame = ttk.Frame(action_frame)
            qty_frame.pack(side="left", padx=5)
            
            qty_var = tk.IntVar(value=1)
            qty_entry = ttk.Entry(qty_frame, textvariable=qty_var, width=3)
            qty_entry.pack(side="left")
            
            # add button
            add_btn = ttk.Button(action_frame, text="+", width=2,
                                command=lambda i=item, q=qty_var: self.add_to_cart(i, q))
            add_btn.pack(side="left")
    
    def add_to_cart(self, item, qty_var):
        """添加商品到購物車"""
        global free_beverage_map # cannot move to checkout if there is nothing in the cart
        
        try:
            quantity = qty_var.get()
            if quantity <= 0:
                messagebox.showerror(text.get('quantity_error', 'Quantity Error'), 
                                 text.get('quantity_error', 'Quantity must be greater than 0'))
                return
        except:
            messagebox.showerror(text.get('quantity_error', 'Quantity Error'), 
                             text.get('quantity_error', 'Quantity must be greater than 0'))
            return
        
        # use discount
        original_price = item[4]
        price = self.get_price(original_price)
        name = self.get_item_name(item)
        
        cart_item = {
            "id": item[0],
            "name": name,
            "price": price,
            "original_price": original_price,
            "quantity": quantity,
            "is_main": item[9] == "main_course" or item[9] == "combo",
            "type": item[9]  
        }
        
        # check cart if there any duplicate
        found = False
        for i, existing_item in enumerate(cart):
            if existing_item["id"] == item[0]:
                cart[i]["quantity"] += quantity
                found = True
                
                # add free drink base on the amount of main course
                if cart[i]["is_main"]:
                    self.offer_free_beverage_for_quantity(i, quantity)
                
                break
        
        if not found:
            # add new things to cart
            cart.append(cart_item)
            
            # if the order is main course， provide free drink
            if cart_item["is_main"]:
                cart_idx = len(cart) - 1
                self.offer_free_beverage(item, cart_idx)
        
        messagebox.showinfo(text.get('added', 'Added'), 
                         f"{text.get('added', 'Added to Cart')}: {name} x {quantity}")
        
        # update cart
        self.update_cart_display()
    
    def offer_free_beverage_for_quantity(self, main_course_index, added_quantity):
        """根據增加主餐數量提供相應免費飲料"""
        global free_beverage_map
        
        if main_course_index in free_beverage_map:
            beverage_index = free_beverage_map[main_course_index]
            # add free drink 
            cart[beverage_index]["quantity"] += added_quantity
            self.update_cart_display()
    
    def offer_free_beverage(self, main_item, main_course_index):
        """提供免費飲料選擇"""
        beverages = [item for item in menu if item[9] == "beverage" and item[8] == main_item[8]]
        
        if not beverages:
            return
        
        # window
        beverage_window = tk.Toplevel(self.master)
        beverage_window.title(text.get("free_beverage", "Free Beverage"))
        beverage_window.geometry("600x600")  
        beverage_window.transient(self.master)
        beverage_window.grab_set()
        
        main_course_name = self.get_item_name(main_item)
        
        label = tk.Label(beverage_window, 
                       text=f"{text.get('select_beverage', 'Please select a free beverage')} ({main_course_name} x{cart[main_course_index]['quantity']})", 
                       font=("Arial", 14, "bold"),  
                       wraplength=550)  
        label.pack(pady=20)  
        
        frame = tk.Frame(beverage_window)
        frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        selected_beverage = tk.IntVar(value=-1)
        
        # drink
        for i, beverage in enumerate(beverages):
            beverage_name = self.get_item_name(beverage)
            beverage_price = beverage[4]
            
            # click button
            option_frame = tk.Frame(scrollable_frame)
            option_frame.pack(fill="x", pady=5)
            
            radio = tk.Radiobutton(option_frame, 
                                 text=f"{beverage[0]}. {beverage_name} (${beverage_price:.0f})",
                                 variable=selected_beverage, 
                                 value=i,
                                 font=("Arial", 12))  
            radio.pack(anchor="w", padx=10, fill="x")
        
        btn_frame = tk.Frame(beverage_window)
        btn_frame.pack(pady=20)  
        
        def on_select():
            selected = selected_beverage.get()
            if selected >= 0:
                global free_beverage_map
                
                # add free drink to cart
                selected_item = beverages[selected]
                main_qty = cart[main_course_index]["quantity"]  
                
                free_beverage = {
                    "id": selected_item[0],
                    "name": f"{self.get_item_name(selected_item)} ({text.get('free_item', 'Free')})",
                    "price": 0,  # free
                    "original_price": selected_item[4],
                    "quantity": main_qty,  # same as main course
                    "is_free": True,
                    "linked_to_main": main_course_index,  # link to main course
                    "type": "beverage"
                }
                
                cart.append(free_beverage)
                free_beverage_map[main_course_index] = len(cart) - 1
                
                self.update_cart_display()
                beverage_window.destroy()
            else:
                messagebox.showinfo("Error", text.get("select_beverage", "Please select a beverage"))
        
        select_btn = tk.Button(btn_frame, text=text.get("select", "Select"), 
                             command=on_select, 
                             padx=30, pady=10,  
                             font=("Arial", 12),  
                             bg="#4CAF50", fg="white")
        select_btn.grid(row=0, column=0, padx=20)  
        
        cancel_btn = tk.Button(btn_frame, text=text.get("cancel", "Cancel"), 
                             command=beverage_window.destroy, 
                             padx=30, pady=10,  
                             font=("Arial", 12), 
                             bg="#f44336", fg="white")
        cancel_btn.grid(row=0, column=1, padx=20)  
        
        self.center_window(beverage_window)
    
    def update_cart_display(self):
        """更新購物車顯示"""
        for widget in self.scrollable_cart.winfo_children():
            widget.destroy()
        
        if not cart:
            empty_label = ttk.Label(self.scrollable_cart, text=text.get('cart_empty', 'Your cart is empty'),
                                  font=("Arial", 12)) 
            empty_label.pack(pady=20)
            self.total_label.config(text=f"{text.get('total', 'Total')}: $0")
            return
        
        total = 0
        
        for i, item in enumerate(cart):
            item_frame = ttk.Frame(self.scrollable_cart)
            item_frame.pack(fill="x", padx=5, pady=8)  
            subtotal = item["price"] * item["quantity"]
            total += subtotal
            
            if item.get("is_free", False):
                # show free drink
                linked_main = item.get("linked_to_main")
                if linked_main is not None and 0 <= linked_main < len(cart):
                    main_name = cart[linked_main]["name"]
                    free_label_text = f"{i+1}. {item['name']} x {item['quantity']} ({text.get('free_with_main', 'Free with main course')}: {main_name})"
                else:
                    free_label_text = f"{i+1}. {item['name']} x {item['quantity']}"
                
                item_label = ttk.Label(item_frame, text=free_label_text, 
                                     wraplength=450,  
                                     font=("Arial", 11))  
            else:
                item_label = ttk.Label(item_frame, 
                                     text=f"{i+1}. {item['name']} x {item['quantity']} = ${subtotal:.0f}",
                                     font=("Arial", 11)) 
            
                if is_student:
                    original_subtotal = item["original_price"] * item["quantity"]
                    original_label = ttk.Label(item_frame, 
                                          text=f"   ({text.get('original_price', 'Original Price')}: ${original_subtotal:.0f})",
                                          font=("Arial", 10))  
                    original_label.pack(anchor="w")
            
            item_label.pack(anchor="w")
            
            # only non free item could be change
            if not item.get("is_free", False):
                action_frame = ttk.Frame(item_frame)
                action_frame.pack(anchor="e", side="right")
                
                edit_btn = ttk.Button(action_frame, text=text.get('modify_quantity', 'Modify Quantity'),
                                   command=lambda idx=i: self.modify_quantity(idx),
                                   width=15)  
                edit_btn.pack(side="left", padx=5)  
                
                delete_btn = ttk.Button(action_frame, text=text.get('delete_item', 'Delete Item'),
                                     command=lambda idx=i: self.delete_item(idx),
                                     width=12)  
                delete_btn.pack(side="left", padx=5)  
        
        self.total_label.config(text=f"{text.get('total', 'Total')}: ${total:.0f}")
    
    def modify_quantity(self, item_index):
        """修改购物车商品数量"""
        global free_beverage_map
        
        item = cart[item_index]
        old_quantity = item["quantity"]
        
        # customize chatting block
        qty_window = tk.Toplevel(self.master)
        qty_window.title(text.get('modify_quantity', 'Modify Quantity'))
        qty_window.geometry("400x200")  
        qty_window.transient(self.master)
        qty_window.grab_set()
        
        name_label = tk.Label(qty_window, text=item["name"], 
                           font=("Arial", 12, "bold"),
                           wraplength=380) 
        name_label.pack(pady=(20, 10))  
        
        qty_frame = tk.Frame(qty_window)
        qty_frame.pack(pady=10)
        
        qty_label = tk.Label(qty_frame, text=text.get('enter_quantity', 'Enter quantity:'),
                          font=("Arial", 12))  
        qty_label.pack(side="left", padx=5)
        qty_var = tk.IntVar(value=item["quantity"])
        qty_entry = tk.Entry(qty_frame, textvariable=qty_var, width=5,
                          font=("Arial", 12))  
        qty_entry.pack(side="left", padx=5)
        btn_frame = tk.Frame(qty_window)
        btn_frame.pack(pady=20)
        
        def on_confirm():
            try:
                qty = qty_var.get()
                if qty <= 0:
                    messagebox.showerror(text.get('quantity_error', 'Quantity Error'), 
                                     text.get('quantity_error', 'Quantity must be greater than 0'))
                    return
                
                cart[item_index]["quantity"] = qty
                
                if item_index in free_beverage_map:
                    beverage_index = free_beverage_map[item_index]
                    cart[beverage_index]["quantity"] = qty
                
                self.update_cart_display()
                messagebox.showinfo(text.get('updated', 'Updated'), text.get('updated', 'Updated'))
                qty_window.destroy()
            except:
                messagebox.showerror(text.get('quantity_error', 'Quantity Error'), 
                                 text.get('quantity_error', 'Quantity must be greater than 0'))
        
        confirm_btn = tk.Button(btn_frame, text=text.get("confirm", "Confirm"), 
                              command=on_confirm,
                              padx=20, pady=5,  
                              font=("Arial", 11), 
                              bg="#4CAF50", fg="white")
        confirm_btn.grid(row=0, column=0, padx=10)  
        
        cancel_btn = tk.Button(btn_frame, text=text.get("cancel", "Cancel"), 
                             command=qty_window.destroy,
                             padx=20, pady=5,  
                             font=("Arial", 11),  
                             bg="#f44336", fg="white")
        cancel_btn.grid(row=0, column=1, padx=10)  
        
        self.center_window(qty_window)
    
    def delete_item(self, item_index):
        """從購物車刪除"""
        global free_beverage_map
        
        # if delete  main course， also delete the free drink
        if item_index in free_beverage_map:
            beverage_index = free_beverage_map[item_index]
            if beverage_index > item_index:
                cart.pop(beverage_index)
                cart.pop(item_index)
            else:
                cart.pop(item_index)
                cart.pop(beverage_index)
            
            del free_beverage_map[item_index]
            
            new_map = {}
            for main_idx, bev_idx in free_beverage_map.items():
                new_main_idx = main_idx if main_idx < item_index else main_idx - 1
                new_bev_idx = bev_idx
                
                if bev_idx > item_index:
                    new_bev_idx -= 1
                
                if beverage_index < bev_idx and beverage_index > item_index:
                    new_bev_idx -= 1
                
                new_map[new_main_idx] = new_bev_idx
            
            free_beverage_map = new_map
        
        # if delete free drink
        else:
            linked_main = None
            for main_idx, bev_idx in free_beverage_map.items():
                if bev_idx == item_index:
                    linked_main = main_idx
                    break
            
            if linked_main is not None:
                del free_beverage_map[linked_main]

                new_map = {}
                for main_idx, bev_idx in free_beverage_map.items():
                    new_bev_idx = bev_idx if bev_idx < item_index else bev_idx - 1
                    new_main_idx = main_idx
                    new_map[new_main_idx] = new_bev_idx
                
                free_beverage_map = new_map
            
            # delete item
            cart.pop(item_index)
        
        self.update_cart_display()
        messagebox.showinfo(text.get('deleted', 'Deleted'), text.get('deleted', 'Deleted'))
    
    def checkout(self):
        """結帳處理"""
        global cart, orders, order_number, free_beverage_map
        
        if not cart:
            messagebox.showinfo(text.get('cart_empty', 'Cart Empty'), 
                             text.get('cart_empty', 'Your cart is empty'))
            return
        
        # customer information
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        
        if not name:
            messagebox.showerror("Error", text.get('enter_name', 'Please enter your name'))
            return
        
        # phone number 
        if not re.match(r'^\d{8}$', phone): # must be 8
            messagebox.showerror("Error", text.get('invalid_phone', 'Invalid phone number. Please enter 8 digits'))
            return
        
        # total price
        total = sum(item["price"] * item["quantity"] for item in cart)
        
        # crate the final order
        order_number += 1
        order = {
            "number": order_number,
            "name": name,
            "phone": phone,
            "items": cart.copy(),
            "total": total,
            "status": text.get('pending', 'Pending'),
            "is_student": is_student
        }
        
        orders.append(order)
        
        # show order information
        self.show_order_success(order)
        
        # clean all the information in cart after finish the order
        cart.clear()
        free_beverage_map.clear()
        
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
    
        self.update_cart_display()
        self.update_orders_display()
    
    def show_order_success(self, order):
        """顯示訂單成功"""
        order_window = tk.Toplevel(self.master)
        order_window.title(text.get('order_success', 'Order Success!'))
        order_window.geometry("600x700")  
        order_window.transient(self.master)
        order_window.grab_set()
        
        frame = tk.Frame(order_window)
        frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        ttk.Label(scrollable_frame, text=text.get('order_success', 'Order Success!'),
                font=("Arial", 18, "bold")).pack(pady=15)  
        
        ttk.Label(scrollable_frame, 
                text=f"{text.get('order_number', 'Order Number')}: {order['number']}",
                font=("Arial", 14)).pack(anchor="w", pady=5)  
        
        ttk.Label(scrollable_frame, 
                text=f"{text.get('customer_name', 'Customer Name')}: {order['name']}",
                font=("Arial", 14)).pack(anchor="w", pady=5)  
        
        ttk.Label(scrollable_frame, 
                text=f"{text.get('contact_phone', 'Contact Phone')}: {order['phone']}",
                font=("Arial", 14)).pack(anchor="w", pady=5)  #
        
        student_status = text.get('student', 'Student') if order['is_student'] else text.get('non_student', 'Non-student')
        ttk.Label(scrollable_frame, 
                text=f"{text.get('student_status', 'Student Status')}: {student_status}",
                font=("Arial", 14)).pack(anchor="w", pady=5)  
        
        # ----------
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=15)  
        
        ttk.Label(scrollable_frame, 
                text=f"{text.get('order_items', 'Order Items')}:", 
                font=("Arial", 16, "bold")).pack(anchor="w", pady=10)  

        for item in order['items']:
            if item.get("is_free", False):
                ttk.Label(scrollable_frame, 
                        text=f"- {item['name']} x {item['quantity']}",
                        font=("Arial", 12),  
                        wraplength=500).pack(anchor="w", pady=5)  
            else:
                subtotal = item["price"] * item["quantity"]
                ttk.Label(scrollable_frame, 
                        text=f"- {item['name']} x {item['quantity']} = ${subtotal:.0f}",
                        font=("Arial", 12), 
                        wraplength=500).pack(anchor="w", pady=5)  
                
                if order['is_student']:
                    original_subtotal = item["original_price"] * item["quantity"]
                    ttk.Label(scrollable_frame, 
                            text=f"  ({text.get('original_price', 'Original Price')}: ${original_subtotal:.0f})",
                            font=("Arial", 11)).pack(anchor="w")  
        
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=15)  
        
        ttk.Label(scrollable_frame, 
                text=f"{text.get('order_total', 'Order Total')}: ${order['total']:.0f}", 
                font=("Arial", 16, "bold")).pack(anchor="w", pady=5) 
        
        ttk.Label(scrollable_frame, 
                text=f"{text.get('status', 'Status')}: {order['status']}",
                font=("Arial", 14)).pack(anchor="w", pady=5)  
        
        ttk.Label(scrollable_frame, 
                text=text.get('payment_instruction', 'Please proceed to the counter to pay and pick up your order'),
                wraplength=500,  
                font=("Arial", 12)).pack(pady=15) 
       
        tk.Button(order_window, text=text.get('confirm', 'Confirm'), 
               command=order_window.destroy, 
               padx=40, pady=10,  
               font=("Arial", 12),  
               bg="#4CAF50", fg="white").pack(pady=20)  
        
        self.center_window(order_window)
    
    def update_orders_display(self):
        """更新訂單歷史顯示"""
        
        for widget in self.scrollable_orders.winfo_children():
            widget.destroy()
        
        if not orders:
            ttk.Label(self.scrollable_orders, 
                    text=text.get('no_orders', 'No order history'),
                    font=("Arial", 12)).pack(pady=20)  
            return
        
        for order in orders:
            order_frame = ttk.Frame(self.scrollable_orders, relief="ridge", borderwidth=1)
            order_frame.pack(fill="x", padx=10, pady=10, ipady=10)  
            
            ttk.Label(order_frame, 
                    text=f"{text.get('order_number', 'Order Number')}: {order['number']}",
                    font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=3) 
            
            ttk.Label(order_frame, 
                    text=f"{text.get('customer_name', 'Customer Name')}: {order['name']}",
                    font=("Arial", 11)).pack(anchor="w", padx=10, pady=2) 
            
            ttk.Label(order_frame, 
                    text=f"{text.get('contact_phone', 'Contact Phone')}: {order['phone']}",
                    font=("Arial", 11)).pack(anchor="w", padx=10, pady=2)  
            
            ttk.Label(order_frame, 
                    text=f"{text.get('order_total', 'Order Total')}: ${order['total']:.0f}",
                    font=("Arial", 11)).pack(anchor="w", padx=10, pady=2)  
            
            ttk.Label(order_frame, 
                    text=f"{text.get('status', 'Status')}: {order['status']}",
                    font=("Arial", 11)).pack(anchor="w", padx=10, pady=2)  

def main():
    root = tk.Tk()
    root.title("Restaurant Ordering System")
    root.geometry("1000x700")
    
    app = RestaurantApp(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()