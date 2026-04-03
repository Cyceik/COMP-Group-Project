# pip3 install pandas openpyxl pytz
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import datetime
import re
import pytz

# ============================================================
# 全局變量 Global Variables
# ============================================================
text = {}
is_student = False
menu = []
cart = []
orders = []
order_number = 0
current_menu_type = ""
secondary_menu_type = ""
current_language = "en"
free_beverage_map = {}

# ── 新增全局變量 ──────────────────────────────────────────────
favorites       = set()       # 收藏商品 ID 集合
order_type      = "dine_in"   # dine_in | takeaway
table_number    = ""
coupon_discount = 0
current_coupon  = ""
search_query    = ""

# 優惠碼 {code: (type, value)}  type: "fixed"=$折扣 | "percent"=%折扣
COUPONS = {
    "WELCOME10": ("fixed",   10),
    "STUDENT20": ("fixed",   20),
    "SAVE15":    ("percent", 15),
}

ADMIN_PASSWORD = "admin123"

STATUS_COLORS = {
    "pending":   "#FFC107",
    "preparing": "#2196F3",
    "ready":     "#4CAF50",
    "completed": "#9E9E9E",
}


# ============================================================
class RestaurantApp:
# ============================================================
    def __init__(self, master):
        self.master = master
        self.master.configure(bg="#f0f0f0")
        self.master.resizable(True, True)

        # 初始化步驟
        self.select_language()
        self.select_student_status()
        self.select_order_type()           # 新增：堂食/外帶

        if not self.create_menu():
            messagebox.showerror("Error", "Failed to load menu data")
            self.master.destroy()
            return

        self.update_current_menu()
        self.create_widgets()
        self.update_menu_display()
        self.update_clock()                # 新增：即時時鐘

    # ──────────────────────────────────────────────────────────
    # 語言選擇
    # ──────────────────────────────────────────────────────────
    def select_language(self):
        global text, current_language

        win = tk.Toplevel(self.master)
        win.title("Select Language / 選擇語言 / 选择语言")
        win.geometry("500x250")
        win.transient(self.master)
        win.grab_set()
        win.protocol("WM_DELETE_WINDOW", lambda: None)

        tk.Label(win,
                 text="Please select your preferred language:\n請選擇您的首選語言:\n请选择您的首选语言:",
                 font=("Arial", 14)).pack(pady=20)

        bf = tk.Frame(win)
        bf.pack(pady=30)

        def set_lang(lang):
            global current_language
            current_language = lang
            {"tc": self.load_traditional_chinese,
             "sc": self.load_simplified_chinese,
             "en": self.load_english}[lang]()
            win.destroy()

        for col, (code, label) in enumerate(
                [("tc", "繁體中文"), ("sc", "简体中文"), ("en", "English")]):
            tk.Button(bf, text=label, width=15, height=2, font=("Arial", 12),
                      command=lambda c=code: set_lang(c)).grid(row=0, column=col, padx=15)

        self.center_window(win)
        self.master.wait_window(win)

    def center_window(self, window):
        window.update_idletasks()
        w, h = window.winfo_width(), window.winfo_height()
        x = (window.winfo_screenwidth()  // 2) - (w // 2)
        y = (window.winfo_screenheight() // 2) - (h // 2)
        window.geometry(f'{w}x{h}+{x}+{y}')

    # ──────────────────────────────────────────────────────────
    # 語言文本
    # ──────────────────────────────────────────────────────────
    def _common_keys(self):
        """所有語言共用的新增鍵，子方法按語言覆蓋"""
        return {
            "dine_in": "Dine In", "takeaway": "Takeaway",
            "order_type": "Order Type",
            "order_type_question": "Select Order Type",
            "table_number": "Table #", "enter_table": "Enter table number:",
            "coupon_code": "Coupon", "apply_coupon": "Apply",
            "coupon_applied": "Coupon Applied!", "coupon_invalid": "Invalid Coupon",
            "coupon_discount": "Coupon Discount",
            "export_receipt": "Export Receipt", "receipt_saved": "Receipt saved!",
            "favorites": "Favorites", "all_items": "All",
            "show_favorites": "★ Favorites", "search": "Search menu...",
            "admin": "Admin", "admin_panel": "Admin Panel",
            "admin_password": "Enter admin password:",
            "wrong_password": "Incorrect password",
            "update_status": "Update Status", "statistics": "Statistics",
            "total_revenue": "Revenue", "total_orders": "Total Orders",
            "popular_items": "Popular Items", "reorder": "Reorder",
            "note": "Note", "item_detail": "Item Details",
            "category": "Category", "menu_period": "Period",
            "time_remaining": "Time Left",
            "breakfast": "Breakfast", "lunch": "Lunch",
            "afternoon_tea": "Afternoon Tea", "dinner": "Dinner",
            "closed": "Closed", "subtotal": "Subtotal",
            "preparing": "Preparing", "ready": "Ready", "completed": "Completed",
            "full": "Full Sugar", "half": "Half Sugar",
            "less": "Less Sugar", "no_sugar": "No Sugar",
            "full_ice": "Normal Ice", "less_ice": "Less Ice",
            "no_ice": "No Ice", "hot": "Hot",
        }

    def load_traditional_chinese(self):
        global text
        text = {
            "welcome": "歡迎光臨餐廳點餐系統",
            "menu": "菜單", "cart": "購物車", "orders": "訂單",
            "student": "學生", "non_student": "非學生",
            "student_discount": "學生可享9折優惠",
            "student_status": "學生身份", "current_time": "當前時間",
            "breakfast_menu": "早餐菜單", "lunch_menu": "午餐菜單",
            "afternoon_tea_menu": "下午茶菜單", "dinner_menu": "晚餐菜單",
            "main_course": "主食", "side_dish": "配菜", "beverage": "飲品",
            "dessert": "甜品", "combo": "套餐", "appetizer": "前菜",
            "view_menu": "菜單", "view_cart": "購物車", "view_orders": "訂單",
            "add_to_cart": "加入購物車",
            "quantity": "數量", "quantity_error": "數量必須大於0",
            "added": "已加入購物車", "cart_empty": "購物車為空",
            "delete_item": "刪除", "modify_quantity": "改數量",
            "enter_quantity": "請輸入數量：",
            "updated": "已更新", "deleted": "已刪除",
            "total": "總計", "checkout": "結帳",
            "enter_name": "姓名：", "enter_phone": "電話號碼：",
            "invalid_phone": "無效電話，請輸入8位數字",
            "order_success": "訂單成功！",
            "order_number": "訂單編號", "customer_name": "客戶姓名",
            "customer": "客戶", "contact_phone": "聯絡電話", "phone": "電話",
            "order_items": "訂單商品", "order_total": "訂單總計",
            "status": "狀態", "pending": "處理中",
            "payment_instruction": "請到櫃檯付款並領取訂單",
            "no_orders": "沒有訂單記錄", "order_history": "訂單歷史",
            "student_question": "您是學生嗎？", "yes": "是", "no": "否",
            "customize_item": "定制商品",
            "customize_prompt": "請選擇您的偏好：",
            "sweet": "甜度", "ice": "冰量", "spicy": "辣度",
            "normal": "正常", "mild": "微辣", "medium": "中辣",
            "extra_spicy": "特辣",
            "original_price": "原價", "discount_price": "折扣價",
            "excel_load_error": "無法加載菜單數據",
            "free_beverage": "免費飲料", "select_beverage": "請選擇免費飲料",
            "select": "確定", "cancel": "取消",
            "free_item": "免費", "confirm": "確認",
            "free_with_main": "與主餐贈送",
            # 新增鍵
            "dine_in": "堂食", "takeaway": "外帶",
            "order_type": "用餐方式",
            "order_type_question": "請選擇用餐方式",
            "table_number": "桌號", "enter_table": "請輸入桌號：",
            "coupon_code": "優惠碼", "apply_coupon": "套用",
            "coupon_applied": "優惠碼已套用！", "coupon_invalid": "無效優惠碼",
            "coupon_discount": "優惠折扣",
            "export_receipt": "匯出收據", "receipt_saved": "收據已儲存",
            "favorites": "收藏", "all_items": "全部",
            "show_favorites": "★ 收藏", "search": "搜尋菜單...",
            "admin": "管理員", "admin_panel": "管理面板",
            "admin_password": "請輸入管理員密碼：",
            "wrong_password": "密碼錯誤",
            "update_status": "更新狀態", "statistics": "統計數據",
            "total_revenue": "總收入", "total_orders": "總訂單數",
            "popular_items": "熱門商品", "reorder": "重新訂購",
            "note": "備註", "item_detail": "商品詳情",
            "category": "類別", "menu_period": "供應時段",
            "time_remaining": "剩餘時間",
            "breakfast": "早餐", "lunch": "午餐",
            "afternoon_tea": "下午茶", "dinner": "晚餐",
            "closed": "休息中", "subtotal": "小計",
            "preparing": "準備中", "ready": "已備好", "completed": "已取餐",
            "full": "全糖", "half": "半糖", "less": "少糖", "no_sugar": "無糖",
            "full_ice": "正常冰", "less_ice": "少冰", "no_ice": "走冰", "hot": "熱",
        }

    def load_simplified_chinese(self):
        global text
        text = {
            "welcome": "欢迎光临餐厅点餐系统",
            "menu": "菜单", "cart": "购物车", "orders": "订单",
            "student": "学生", "non_student": "非学生",
            "student_discount": "学生可享9折优惠",
            "student_status": "学生身份", "current_time": "当前时间",
            "breakfast_menu": "早餐菜单", "lunch_menu": "午餐菜单",
            "afternoon_tea_menu": "下午茶菜单", "dinner_menu": "晚餐菜单",
            "main_course": "主食", "side_dish": "配菜", "beverage": "饮品",
            "dessert": "甜品", "combo": "套餐", "appetizer": "前菜",
            "view_menu": "菜单", "view_cart": "购物车", "view_orders": "订单",
            "add_to_cart": "加入购物车",
            "quantity": "数量", "quantity_error": "数量必须大于0",
            "added": "已加入购物车", "cart_empty": "购物车为空",
            "delete_item": "删除", "modify_quantity": "改数量",
            "enter_quantity": "请输入数量：",
            "updated": "已更新", "deleted": "已删除",
            "total": "总计", "checkout": "结账",
            "enter_name": "姓名：", "enter_phone": "电话号码：",
            "invalid_phone": "无效电话，请输入8位数字",
            "order_success": "订单成功！",
            "order_number": "订单编号", "customer_name": "客户姓名",
            "customer": "客户", "contact_phone": "联系电话", "phone": "电话",
            "order_items": "订单商品", "order_total": "订单总计",
            "status": "状态", "pending": "处理中",
            "payment_instruction": "请到柜台付款并领取订单",
            "no_orders": "没有订单记录", "order_history": "订单历史",
            "student_question": "您是学生吗？", "yes": "是", "no": "否",
            "customize_item": "定制商品",
            "customize_prompt": "请选择您的偏好：",
            "sweet": "甜度", "ice": "冰量", "spicy": "辣度",
            "normal": "正常", "mild": "微辣", "medium": "中辣",
            "extra_spicy": "特辣",
            "original_price": "原价", "discount_price": "折扣价",
            "excel_load_error": "无法加载菜单数据",
            "free_beverage": "免费饮料", "select_beverage": "请选择免费饮料",
            "select": "确定", "cancel": "取消",
            "free_item": "免费", "confirm": "确认",
            "free_with_main": "与主餐赠送",
            # 新增键
            "dine_in": "堂食", "takeaway": "外带",
            "order_type": "用餐方式",
            "order_type_question": "请选择用餐方式",
            "table_number": "桌号", "enter_table": "请输入桌号：",
            "coupon_code": "优惠码", "apply_coupon": "套用",
            "coupon_applied": "优惠码已套用！", "coupon_invalid": "无效优惠码",
            "coupon_discount": "优惠折扣",
            "export_receipt": "导出收据", "receipt_saved": "收据已保存",
            "favorites": "收藏", "all_items": "全部",
            "show_favorites": "★ 收藏", "search": "搜索菜单...",
            "admin": "管理员", "admin_panel": "管理面板",
            "admin_password": "请输入管理员密码：",
            "wrong_password": "密码错误",
            "update_status": "更新状态", "statistics": "统计数据",
            "total_revenue": "总收入", "total_orders": "总订单数",
            "popular_items": "热门商品", "reorder": "重新订购",
            "note": "备注", "item_detail": "商品详情",
            "category": "类别", "menu_period": "供应时段",
            "time_remaining": "剩余时间",
            "breakfast": "早餐", "lunch": "午餐",
            "afternoon_tea": "下午茶", "dinner": "晚餐",
            "closed": "休息中", "subtotal": "小计",
            "preparing": "准备中", "ready": "已备好", "completed": "已取餐",
            "full": "全糖", "half": "半糖", "less": "少糖", "no_sugar": "无糖",
            "full_ice": "正常冰", "less_ice": "少冰", "no_ice": "走冰", "hot": "热",
        }

    def load_english(self):
        global text
        text = {
            "welcome": "Welcome to Restaurant Ordering System",
            "menu": "Menu", "cart": "Cart", "orders": "Orders",
            "student": "Student", "non_student": "Non-student",
            "student_discount": "Students receive a 10% discount",
            "student_status": "Student Status", "current_time": "Current Time",
            "breakfast_menu": "Breakfast Menu", "lunch_menu": "Lunch Menu",
            "afternoon_tea_menu": "Afternoon Tea Menu", "dinner_menu": "Dinner Menu",
            "main_course": "Main Course", "side_dish": "Side Dish",
            "beverage": "Beverage", "dessert": "Dessert",
            "combo": "Combo", "appetizer": "Appetizer",
            "view_menu": "Menu", "view_cart": "Cart", "view_orders": "Orders",
            "add_to_cart": "Add to Cart",
            "quantity": "Quantity", "quantity_error": "Quantity must be greater than 0",
            "added": "Added to Cart", "cart_empty": "Your cart is empty",
            "delete_item": "Delete", "modify_quantity": "Edit Qty",
            "enter_quantity": "Enter quantity:",
            "updated": "Updated", "deleted": "Deleted",
            "total": "Total", "checkout": "Checkout",
            "enter_name": "Name:", "enter_phone": "Phone:",
            "invalid_phone": "Invalid phone. Please enter 8 digits",
            "order_success": "Order Success!",
            "order_number": "Order #", "customer_name": "Customer",
            "customer": "Customer", "contact_phone": "Phone", "phone": "Phone",
            "order_items": "Items", "order_total": "Total",
            "status": "Status", "pending": "Pending",
            "payment_instruction": "Please go to the counter to pay and collect your order",
            "no_orders": "No order history", "order_history": "Order History",
            "student_question": "Are you a student?", "yes": "Yes", "no": "No",
            "customize_item": "Customize Item",
            "customize_prompt": "Select your preferences:",
            "sweet": "Sweetness", "ice": "Ice Level", "spicy": "Spiciness",
            "normal": "Normal", "mild": "Mild", "medium": "Medium",
            "extra_spicy": "Extra Spicy",
            "original_price": "Original", "discount_price": "Discounted",
            "excel_load_error": "Failed to load menu data",
            "free_beverage": "Free Beverage",
            "select_beverage": "Select a free beverage",
            "select": "Select", "cancel": "Cancel",
            "free_item": "Free", "confirm": "Confirm",
            "free_with_main": "Free w/ main",
            # New keys
            "dine_in": "Dine In", "takeaway": "Takeaway",
            "order_type": "Order Type",
            "order_type_question": "Select Order Type",
            "table_number": "Table #", "enter_table": "Enter table number:",
            "coupon_code": "Coupon", "apply_coupon": "Apply",
            "coupon_applied": "Coupon Applied!", "coupon_invalid": "Invalid Coupon",
            "coupon_discount": "Coupon Discount",
            "export_receipt": "Export Receipt", "receipt_saved": "Receipt saved!",
            "favorites": "Favorites", "all_items": "All",
            "show_favorites": "★ Favorites", "search": "Search menu...",
            "admin": "Admin", "admin_panel": "Admin Panel",
            "admin_password": "Enter admin password:",
            "wrong_password": "Incorrect password",
            "update_status": "Update Status", "statistics": "Statistics",
            "total_revenue": "Revenue", "total_orders": "Total Orders",
            "popular_items": "Popular Items", "reorder": "Reorder",
            "note": "Note", "item_detail": "Item Details",
            "category": "Category", "menu_period": "Period",
            "time_remaining": "Time Left",
            "breakfast": "Breakfast", "lunch": "Lunch",
            "afternoon_tea": "Afternoon Tea", "dinner": "Dinner",
            "closed": "Closed", "subtotal": "Subtotal",
            "preparing": "Preparing", "ready": "Ready", "completed": "Completed",
            "full": "Full Sugar", "half": "Half Sugar",
            "less": "Less Sugar", "no_sugar": "No Sugar",
            "full_ice": "Normal Ice", "less_ice": "Less Ice",
            "no_ice": "No Ice", "hot": "Hot",
        }

    # ──────────────────────────────────────────────────────────
    # 學生狀態
    # ──────────────────────────────────────────────────────────
    def select_student_status(self):
        global is_student

        win = tk.Toplevel(self.master)
        win.title(text.get("student_question", "Are you a student?"))
        win.geometry("400x200")
        win.transient(self.master)
        win.grab_set()
        win.protocol("WM_DELETE_WINDOW", lambda: None)

        tk.Label(win, text=text.get("student_question", "Are you a student?"),
                 font=("Arial", 14)).pack(pady=20)

        bf = tk.Frame(win)
        bf.pack(pady=30)

        tk.Button(bf, text=text.get("yes", "Yes"), width=12, height=2,
                  font=("Arial", 12),
                  command=lambda: self.set_student_status(True, win)).grid(row=0, column=0, padx=20)
        tk.Button(bf, text=text.get("no", "No"), width=12, height=2,
                  font=("Arial", 12),
                  command=lambda: self.set_student_status(False, win)).grid(row=0, column=1, padx=20)

        self.center_window(win)
        self.master.wait_window(win)

    def set_student_status(self, status, window):
        global is_student
        is_student = status
        window.destroy()

    # ──────────────────────────────────────────────────────────
    # 新增：堂食 / 外帶選擇
    # ──────────────────────────────────────────────────────────
    def select_order_type(self):
        global order_type, table_number

        win = tk.Toplevel(self.master)
        win.title(text.get("order_type_question", "Select Order Type"))
        win.geometry("420x280")
        win.transient(self.master)
        win.grab_set()
        win.protocol("WM_DELETE_WINDOW", lambda: None)

        tk.Label(win, text=text.get("order_type_question", "Select Order Type"),
                 font=("Arial", 14)).pack(pady=15)

        selected_type = tk.StringVar(value="dine_in")

        bf = tk.Frame(win)
        bf.pack(pady=10)

        dine_btn = tk.Button(bf,
                             text=f"🍽  {text.get('dine_in', 'Dine In')}",
                             width=15, height=2, font=("Arial", 12),
                             bg="#3498db", fg="white",
                             command=lambda: _select("dine_in"))
        dine_btn.grid(row=0, column=0, padx=15)

        take_btn = tk.Button(bf,
                             text=f"🥡  {text.get('takeaway', 'Takeaway')}",
                             width=15, height=2, font=("Arial", 12),
                             bg="#95a5a6", fg="white",
                             command=lambda: _select("takeaway"))
        take_btn.grid(row=0, column=1, padx=15)

        # 桌號輸入區（預設顯示）
        table_frame = tk.Frame(win)
        table_var = tk.StringVar()
        tk.Label(table_frame,
                 text=text.get("enter_table", "Enter table number:"),
                 font=("Arial", 12)).pack(side="left", padx=5)
        tk.Entry(table_frame, textvariable=table_var, width=6,
                 font=("Arial", 12)).pack(side="left", padx=5)
        table_frame.pack(pady=5)

        def _select(ot):
            selected_type.set(ot)
            if ot == "dine_in":
                dine_btn.config(bg="#3498db")
                take_btn.config(bg="#95a5a6")
                table_frame.pack(pady=5)
            else:
                dine_btn.config(bg="#95a5a6")
                take_btn.config(bg="#3498db")
                table_frame.pack_forget()

        def on_confirm():
            global order_type, table_number
            ot = selected_type.get()
            if ot == "dine_in":
                t = table_var.get().strip()
                if not t:
                    messagebox.showerror(
                        "Error", text.get("enter_table", "Please enter table number"))
                    return
                table_number = t
            else:
                table_number = ""
            order_type = ot
            win.destroy()

        tk.Button(win, text=f"✓  {text.get('confirm', 'Confirm')}",
                  command=on_confirm, bg="#4CAF50", fg="white",
                  font=("Arial", 12), padx=25, pady=8).pack(pady=10)

        self.center_window(win)
        self.master.wait_window(win)

    # ──────────────────────────────────────────────────────────
    # 菜單數據
    # ──────────────────────────────────────────────────────────
    def create_menu(self):
        global menu
        try:
            df = pd.read_excel("menu_data.xlsx")
            menu = df.values.tolist()
            return True
        except Exception as e:
            print(f"Error loading menu: {e}")
            messagebox.showerror("Error", text.get("excel_load_error", "Failed to load menu"))
            return False

    def update_current_menu(self):
        global current_menu_type, secondary_menu_type
        h = self.get_hk_time().hour
        if   6 <= h < 11: current_menu_type, secondary_menu_type = "breakfast",    ""
        elif 11 <= h < 14: current_menu_type, secondary_menu_type = "lunch",        ""
        elif 14 <= h < 18: current_menu_type, secondary_menu_type = "afternoon_tea","lunch"
        elif 18 <= h < 22: current_menu_type, secondary_menu_type = "dinner",       ""
        else:              current_menu_type, secondary_menu_type = "dinner",       ""

    def get_hk_time(self):
        return datetime.datetime.now(pytz.timezone('Asia/Hong_Kong'))

    def get_current_menu_name(self):
        return {
            "breakfast":    text.get("breakfast_menu",    "Breakfast Menu"),
            "lunch":        text.get("lunch_menu",        "Lunch Menu"),
            "afternoon_tea":text.get("afternoon_tea_menu","Afternoon Tea Menu"),
            "dinner":       text.get("dinner_menu",       "Dinner Menu"),
        }.get(current_menu_type, "")

    def get_category_name(self, item_type):
        return {
            "main_course": text.get("main_course", "Main Course"),
            "side_dish":   text.get("side_dish",   "Side Dish"),
            "beverage":    text.get("beverage",    "Beverage"),
            "dessert":     text.get("dessert",     "Dessert"),
            "combo":       text.get("combo",       "Combo"),
            "appetizer":   text.get("appetizer",   "Appetizer"),
        }.get(item_type, item_type)

    def get_item_name(self, item):
        if current_language == "tc": return item[1]
        if current_language == "sc": return item[2]
        return item[3]

    def get_price(self, original_price):
        return round(original_price * 0.9) if is_student else original_price

    # ──────────────────────────────────────────────────────────
    # 新增：菜單時段計時器
    # ──────────────────────────────────────────────────────────
    def get_menu_period_info(self):
        h = self.get_hk_time().hour
        for start, end, name_key in [
            (6,  11, "breakfast"),
            (11, 14, "lunch"),
            (14, 18, "afternoon_tea"),
            (18, 22, "dinner"),
        ]:
            if start <= h < end:
                return text.get(name_key, name_key), end
        return text.get("closed", "Closed"), 6

    def get_time_remaining(self):
        now = self.get_hk_time()
        h   = now.hour
        if   6  <= h < 11: end_h = 11
        elif 11 <= h < 14: end_h = 14
        elif 14 <= h < 18: end_h = 18
        elif 18 <= h < 22: end_h = 22
        else:
            next_open = now.replace(hour=6, minute=0, second=0, microsecond=0)
            if h >= 22:
                next_open += datetime.timedelta(days=1)
            diff = int((next_open - now).total_seconds())
            return f"{diff // 3600:02d}:{(diff % 3600) // 60:02d}"
        end  = now.replace(hour=end_h, minute=0, second=0, microsecond=0)
        diff = int((end - now).total_seconds())
        return f"{diff // 3600:02d}:{(diff % 3600) // 60:02d}"

    # ──────────────────────────────────────────────────────────
    # 主界面佈局
    # ──────────────────────────────────────────────────────────
    def create_widgets(self):
        # ── 頂部深色欄 ────────────────────────────────────────
        top = tk.Frame(self.master, bg="#2c3e50", pady=8)
        top.pack(fill="x")

        left = tk.Frame(top, bg="#2c3e50")
        left.pack(side="left", fill="y", padx=12)

        tk.Label(left, text=text.get("welcome", "Welcome"),
                 font=("Arial", 14, "bold"), bg="#2c3e50", fg="white").pack(anchor="w")

        ot_str = text.get(order_type, order_type)
        if order_type == "dine_in" and table_number:
            ot_str += f"  |  {text.get('table_number','Table')}: {table_number}"
        tk.Label(left, text=f"{text.get('order_type','Type')}: {ot_str}",
                 bg="#2c3e50", fg="#bdc3c7", font=("Arial", 10)).pack(anchor="w")

        s_status = text.get("student","Student") if is_student else text.get("non_student","Non-student")
        tk.Label(left, text=f"{text.get('student_status','Status')}: {s_status}",
                 bg="#2c3e50", fg="#bdc3c7", font=("Arial", 10)).pack(anchor="w")
        if is_student:
            tk.Label(left, text=text.get("student_discount","10% off"),
                     bg="#2c3e50", fg="#f39c12", font=("Arial", 10, "italic")).pack(anchor="w")

        right = tk.Frame(top, bg="#2c3e50")
        right.pack(side="right", padx=12)

        now = self.get_hk_time()
        self.clock_label = tk.Label(right,
                                    text=now.strftime('%Y-%m-%d  %H:%M:%S'),
                                    bg="#2c3e50", fg="white",
                                    font=("Arial", 13, "bold"))
        self.clock_label.pack(anchor="e")

        period_name, _ = self.get_menu_period_info()
        self.timer_label = tk.Label(right,
                                    text=f"⏱  {period_name}  |  {text.get('time_remaining','Left')}: {self.get_time_remaining()}",
                                    bg="#2c3e50", fg="#1abc9c", font=("Arial", 10))
        self.timer_label.pack(anchor="e")

        tk.Button(right, text=f"⚙  {text.get('admin','Admin')}",
                  command=self.open_admin_panel,
                  bg="#7f8c8d", fg="white", font=("Arial", 10),
                  relief="flat", padx=8, pady=2).pack(anchor="e", pady=(4, 0))

        # ── Notebook ─────────────────────────────────────────
        self.tab_control = ttk.Notebook(self.master)
        self.menu_tab   = ttk.Frame(self.tab_control)
        self.cart_tab   = ttk.Frame(self.tab_control)
        self.orders_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.menu_tab,   text=f"  {text.get('view_menu','Menu')}  ")
        self.tab_control.add(self.cart_tab,   text=f"  {text.get('view_cart','Cart')} (0)  ")
        self.tab_control.add(self.orders_tab, text=f"  {text.get('view_orders','Orders')}  ")
        self.tab_control.pack(expand=1, fill="both")

        self.setup_menu_tab()
        self.setup_cart_tab()
        self.setup_orders_tab()

    # ──────────────────────────────────────────────────────────
    # 新增：即時時鐘更新
    # ──────────────────────────────────────────────────────────
    def update_clock(self):
        now = self.get_hk_time()
        self.clock_label.config(text=now.strftime('%Y-%m-%d  %H:%M:%S'))
        period_name, _ = self.get_menu_period_info()
        self.timer_label.config(
            text=f"⏱  {period_name}  |  {text.get('time_remaining','Left')}: {self.get_time_remaining()}")
        self.master.after(1000, self.update_clock)

    # ──────────────────────────────────────────────────────────
    # 菜單 Tab
    # ──────────────────────────────────────────────────────────
    def setup_menu_tab(self):
        # 標題列
        hdr = tk.Frame(self.menu_tab, bg="#ecf0f1", pady=6)
        hdr.pack(fill="x")

        self.menu_type_label = tk.Label(hdr, text=self.get_current_menu_name(),
                                        font=("Arial", 14, "bold"), bg="#ecf0f1")
        self.menu_type_label.pack(side="left", padx=15)

        # 新增：收藏篩選按鈕
        self.show_fav = False
        self.fav_btn  = tk.Button(hdr,
                                  text=text.get("show_favorites", "★ Favorites"),
                                  command=self.toggle_favorites_filter,
                                  bg="#f39c12", fg="white",
                                  font=("Arial", 10), relief="flat", padx=10, pady=3)
        self.fav_btn.pack(side="right", padx=10)

        # 新增：搜尋欄
        search_bar = tk.Frame(self.menu_tab, bg="#f5f5f5", pady=5)
        search_bar.pack(fill="x", padx=10)

        tk.Label(search_bar, text="🔍", bg="#f5f5f5",
                 font=("Arial", 12)).pack(side="left", padx=(5, 2))

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search_change)
        self.search_entry = tk.Entry(search_bar, textvariable=self.search_var,
                                     font=("Arial", 12), relief="solid", bd=1)
        self.search_entry.pack(side="left", padx=5, ipady=4, fill="x", expand=True)

        placeholder = text.get("search", "Search menu...")
        self.search_entry.insert(0, placeholder)
        self.search_entry.config(fg="grey")
        self.search_entry.bind("<FocusIn>",  lambda e: self._clear_ph())
        self.search_entry.bind("<FocusOut>", lambda e: self._restore_ph())

        # 新增：分類篩選按鈕列
        cat_bar = tk.Frame(self.menu_tab, bg="#f5f5f5", pady=4)
        cat_bar.pack(fill="x", padx=10)

        self.cat_filter  = "all"
        self.cat_buttons = {}
        for cat_key, cat_label in [
            ("all",         text.get("all_items",  "All")),
            ("main_course", text.get("main_course","Main")),
            ("appetizer",   text.get("appetizer",  "Appetizer")),
            ("beverage",    text.get("beverage",   "Beverage")),
            ("dessert",     text.get("dessert",    "Dessert")),
        ]:
            btn = tk.Button(cat_bar, text=cat_label,
                            command=lambda k=cat_key: self.set_category_filter(k),
                            bg="#3498db" if cat_key == "all" else "#bdc3c7",
                            fg="white", font=("Arial", 9, "bold"),
                            relief="flat", padx=10, pady=4)
            btn.pack(side="left", padx=3)
            self.cat_buttons[cat_key] = btn

        # 可滾動菜單區
        area = tk.Frame(self.menu_tab)
        area.pack(fill="both", expand=True)

        canvas = tk.Canvas(area, bg="#f8f8f8")
        sb     = ttk.Scrollbar(area, orient="vertical", command=canvas.yview)
        self.scrollable_menu = ttk.Frame(canvas)
        self.scrollable_menu.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_menu, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        canvas.bind("<MouseWheel>",
                    lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    # 搜尋 placeholder 輔助
    def _clear_ph(self):
        if self.search_entry.get() == text.get("search", "Search menu..."):
            self.search_var.set("")
            self.search_entry.config(fg="black")

    def _restore_ph(self):
        if not self.search_entry.get():
            self.search_entry.insert(0, text.get("search", "Search menu..."))
            self.search_entry.config(fg="grey")

    def on_search_change(self, *args):
        global search_query
        query = self.search_var.get()
        search_query = "" if query == text.get("search", "Search menu...") else query.lower()
        if hasattr(self, "scrollable_menu"):
            self.update_menu_display()

    def toggle_favorites_filter(self):
        self.show_fav = not self.show_fav
        if self.show_fav:
            self.fav_btn.config(bg="#e74c3c",
                                text=f"✕ {text.get('favorites','Favorites')}")
        else:
            self.fav_btn.config(bg="#f39c12",
                                text=text.get("show_favorites", "★ Favorites"))
        self.update_menu_display()

    def set_category_filter(self, category):
        self.cat_filter = category
        for k, btn in self.cat_buttons.items():
            btn.config(bg="#3498db" if k == category else "#bdc3c7")
        self.update_menu_display()

    # ──────────────────────────────────────────────────────────
    # 購物車 Tab
    # ──────────────────────────────────────────────────────────
    def setup_cart_tab(self):
        cart_area = tk.Frame(self.cart_tab)
        cart_area.pack(fill="both", expand=True, padx=10, pady=5)

        tk.Label(cart_area, text=text.get("cart", "Cart"),
                 font=("Arial", 14, "bold")).pack(anchor="w", pady=(5, 3))

        canvas = tk.Canvas(cart_area)
        sb     = ttk.Scrollbar(cart_area, orient="vertical", command=canvas.yview)
        self.scrollable_cart = ttk.Frame(canvas)
        self.scrollable_cart.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_cart, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        canvas.bind("<MouseWheel>",
                    lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        # 底部：優惠碼 + 合計 + 結帳表單
        bottom = tk.Frame(self.cart_tab, bg="#f9f9f9", pady=8)
        bottom.pack(fill="x", side="bottom")

        # 優惠碼列
        coupon_row = tk.Frame(bottom, bg="#f9f9f9")
        coupon_row.pack(fill="x", padx=15, pady=3)

        tk.Label(coupon_row, text=f"🎟  {text.get('coupon_code','Coupon')}:",
                 bg="#f9f9f9", font=("Arial", 11)).pack(side="left", padx=(0, 5))
        self.coupon_entry = tk.Entry(coupon_row, width=14, font=("Arial", 11))
        self.coupon_entry.pack(side="left", padx=(0, 5), ipady=3)
        tk.Button(coupon_row, text=text.get("apply_coupon", "Apply"),
                  command=self.apply_coupon, bg="#9b59b6", fg="white",
                  font=("Arial", 10, "bold"), relief="flat", padx=10).pack(side="left")
        self.coupon_msg = tk.Label(coupon_row, text="", bg="#f9f9f9",
                                   font=("Arial", 10), fg="#27ae60")
        self.coupon_msg.pack(side="left", padx=8)

        # 金額列
        price_row = tk.Frame(bottom, bg="#f9f9f9")
        price_row.pack(fill="x", padx=15, pady=2)

        self.subtotal_label = tk.Label(price_row,
                                       text=f"{text.get('subtotal','Subtotal')}: $0",
                                       bg="#f9f9f9", font=("Arial", 11))
        self.subtotal_label.pack(anchor="e")

        self.discount_label = tk.Label(price_row, text="", bg="#f9f9f9",
                                       font=("Arial", 11), fg="#e74c3c")
        self.discount_label.pack(anchor="e")

        self.total_label = tk.Label(price_row,
                                    text=f"{text.get('total','Total')}: $0",
                                    bg="#f9f9f9", font=("Arial", 14, "bold"))
        self.total_label.pack(anchor="e")

        # 結帳表單
        form = tk.Frame(bottom, bg="#f9f9f9")
        form.pack(fill="x", padx=15, pady=5)

        tk.Label(form, text=text.get("enter_name", "Name:"),
                 bg="#f9f9f9", font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=3)
        self.name_entry = tk.Entry(form, width=25, font=("Arial", 11))
        self.name_entry.grid(row=0, column=1, sticky="w", pady=3, padx=8)

        tk.Label(form, text=text.get("enter_phone", "Phone:"),
                 bg="#f9f9f9", font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=3)
        self.phone_entry = tk.Entry(form, width=25, font=("Arial", 11))
        self.phone_entry.grid(row=1, column=1, sticky="w", pady=3, padx=8)

        tk.Button(form, text=f"✓  {text.get('checkout','Checkout')}",
                  command=self.checkout, bg="#e74c3c", fg="white",
                  font=("Arial", 13, "bold"), relief="flat",
                  padx=30, pady=10).grid(row=2, column=0, columnspan=3, pady=12)

    # ──────────────────────────────────────────────────────────
    # 訂單 Tab
    # ──────────────────────────────────────────────────────────
    def setup_orders_tab(self):
        hdr = tk.Frame(self.orders_tab, bg="#ecf0f1", pady=6)
        hdr.pack(fill="x")
        tk.Label(hdr, text=text.get("order_history", "Order History"),
                 font=("Arial", 14, "bold"), bg="#ecf0f1").pack(side="left", padx=15)

        area = tk.Frame(self.orders_tab)
        area.pack(fill="both", expand=True, padx=10, pady=5)

        canvas = tk.Canvas(area)
        sb     = ttk.Scrollbar(area, orient="vertical", command=canvas.yview)
        self.scrollable_orders = ttk.Frame(canvas)
        self.scrollable_orders.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_orders, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        canvas.bind("<MouseWheel>",
                    lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    # ──────────────────────────────────────────────────────────
    # 菜單顯示
    # ──────────────────────────────────────────────────────────
    def update_menu_display(self):
        for w in self.scrollable_menu.winfo_children():
            w.destroy()

        self.menu_type_label.config(text=self.get_current_menu_name())
        current_items = [i for i in menu if i[8] == current_menu_type]

        if secondary_menu_type == "lunch" and current_menu_type == "afternoon_tea":
            ttk.Label(self.scrollable_menu,
                      text=text.get("afternoon_tea_menu", "Afternoon Tea"),
                      font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=5)
            self.display_menu_section(current_items)

            ttk.Separator(self.scrollable_menu, orient="horizontal").pack(
                fill="x", padx=10, pady=10)

            ttk.Label(self.scrollable_menu,
                      text=text.get("lunch_menu", "Lunch Menu"),
                      font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=5)
            self.display_menu_section([i for i in menu if i[8] == "lunch"])
        else:
            self.display_menu_section(current_items)

    def display_menu_section(self, menu_items):
        current_cat = ""
        count = 0

        for item in menu_items:
            if self.cat_filter != "all" and item[9] != self.cat_filter:
                continue
            if self.show_fav and item[0] not in favorites:
                continue
            if search_query:
                names = [str(item[1]).lower(), str(item[2]).lower(), str(item[3]).lower()]
                if not any(search_query in n for n in names):
                    continue

            count += 1
            cat = self.get_category_name(item[9])

            if cat != current_cat:
                current_cat = cat
                ttk.Label(self.scrollable_menu, text=f"【{cat}】",
                          font=("Arial", 11, "bold")).pack(
                    anchor="w", padx=10, pady=(12, 4))

            # 商品卡片
            card = tk.Frame(self.scrollable_menu, bg="#ffffff", relief="groove", bd=1)
            card.pack(fill="x", padx=12, pady=3, ipady=4)

            # 左側：資訊
            info = tk.Frame(card, bg="#ffffff")
            info.pack(side="left", fill="x", expand=True, padx=10)

            name  = self.get_item_name(item)
            orig  = item[4]
            price = self.get_price(orig)

            name_row = tk.Frame(info, bg="#ffffff")
            name_row.pack(anchor="w", fill="x")

            # 商品名稱（可點擊查看詳情）
            name_lbl = tk.Label(name_row, text=f"{item[0]}. {name}",
                                font=("Arial", 12, "bold"),
                                bg="#ffffff", cursor="hand2")
            name_lbl.pack(side="left")
            name_lbl.bind("<Button-1>", lambda e, i=item: self.show_item_detail(i))

            # 收藏按鈕
            is_fav = item[0] in favorites
            tk.Button(name_row,
                      text="★" if is_fav else "☆",
                      bg="#ffffff",
                      fg="#f39c12" if is_fav else "#bdc3c7",
                      font=("Arial", 13), relief="flat",
                      command=lambda i=item: self.toggle_favorite(i)).pack(
                side="left", padx=4)

            # 價格
            if is_student:
                tk.Label(info,
                         text=f"${orig:.0f}  →  {text.get('discount_price','Disc')}: ${price:.0f}",
                         font=("Arial", 10), bg="#ffffff", fg="#e74c3c").pack(anchor="w")
            else:
                tk.Label(info, text=f"${orig:.0f}",
                         font=("Arial", 11), bg="#ffffff", fg="#2c3e50").pack(anchor="w")

            # 右側：數量控制 + 加入購物車
            act     = tk.Frame(card, bg="#ffffff")
            qty_var = tk.IntVar(value=1)
            act.pack(side="right", padx=10)

            tk.Button(act, text="−", font=("Arial", 12), bg="#ecf0f1",
                      relief="flat", width=2,
                      command=lambda v=qty_var: v.set(max(1, v.get() - 1))).pack(side="left")
            tk.Entry(act, textvariable=qty_var, width=3,
                     font=("Arial", 11), justify="center").pack(side="left", padx=3)
            tk.Button(act, text="+", font=("Arial", 12), bg="#ecf0f1",
                      relief="flat", width=2,
                      command=lambda v=qty_var: v.set(v.get() + 1)).pack(side="left")

            tk.Button(act,
                      text=f"+ {text.get('add_to_cart','Add')}",
                      bg="#e74c3c", fg="white",
                      font=("Arial", 10, "bold"), relief="flat", padx=10,
                      command=lambda i=item, q=qty_var: self.add_to_cart(i, q)).pack(
                side="left", padx=(8, 0))

        if count == 0:
            ttk.Label(self.scrollable_menu, text="— No items found —",
                      font=("Arial", 12)).pack(pady=30)

    # ──────────────────────────────────────────────────────────
    # 新增：商品詳情彈窗
    # ──────────────────────────────────────────────────────────
    def show_item_detail(self, item):
        win = tk.Toplevel(self.master)
        win.title(text.get("item_detail", "Item Details"))
        win.geometry("400x360")
        win.transient(self.master)
        win.grab_set()

        frm = tk.Frame(win, padx=25, pady=20)
        frm.pack(fill="both", expand=True)

        tk.Label(frm, text=self.get_item_name(item),
                 font=("Arial", 18, "bold")).pack(anchor="w")
        ttk.Separator(frm, orient="horizontal").pack(fill="x", pady=10)

        rows = [
            (text.get("category", "Category"),    self.get_category_name(item[9])),
            (text.get("menu_period", "Period"),    item[8].replace("_", " ").title()),
            (text.get("original_price","Price"),   f"${item[4]:.0f}"),
        ]
        if is_student:
            rows.append((text.get("discount_price","Discounted"),
                         f"${self.get_price(item[4]):.0f}"))
        rows += [("繁體中文", item[1]), ("简体中文", item[2]), ("English", item[3])]

        for lbl, val in rows:
            row = tk.Frame(frm)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=f"{lbl}:", font=("Arial", 11, "bold"),
                     width=16, anchor="w").pack(side="left")
            tk.Label(row, text=str(val), font=("Arial", 11),
                     anchor="w").pack(side="left")

        tk.Button(win, text=text.get("confirm", "OK"), command=win.destroy,
                  bg="#3498db", fg="white", font=("Arial", 11),
                  padx=20, pady=6).pack(pady=20)

        self.center_window(win)

    # ──────────────────────────────────────────────────────────
    # 新增：收藏切換
    # ──────────────────────────────────────────────────────────
    def toggle_favorite(self, item):
        if item[0] in favorites:
            favorites.remove(item[0])
        else:
            favorites.add(item[0])
        self.update_menu_display()

    # ──────────────────────────────────────────────────────────
    # 新增：商品定制對話框
    # ──────────────────────────────────────────────────────────
    def show_customization_dialog(self, item):
        """返回 dict（確認）或 None（取消）"""
        is_beverage = (item[9] == "beverage")
        is_food     = (item[9] in ["main_course", "appetizer", "combo"])

        if not (is_beverage or is_food):
            return {}

        win = tk.Toplevel(self.master)
        win.title(text.get("customize_item", "Customize"))
        win.geometry("440x420")
        win.transient(self.master)
        win.grab_set()

        result = [None]

        frm = tk.Frame(win, padx=20, pady=15)
        frm.pack(fill="both", expand=True)

        tk.Label(frm, text=self.get_item_name(item),
                 font=("Arial", 14, "bold")).pack(anchor="w")
        tk.Label(frm, text=text.get("customize_prompt", "Select preferences:"),
                 font=("Arial", 11)).pack(anchor="w", pady=(4, 10))

        opts = {}

        if is_beverage:
            # 甜度
            tk.Label(frm, text=text.get("sweet", "Sweetness") + ":",
                     font=("Arial", 11, "bold")).pack(anchor="w")
            sweet_var = tk.StringVar(value="full")
            sf = tk.Frame(frm)
            sf.pack(anchor="w", pady=(0, 8))
            for v, l in [("full",     text.get("full",     "Full Sugar")),
                         ("half",     text.get("half",     "Half Sugar")),
                         ("less",     text.get("less",     "Less Sugar")),
                         ("no_sugar", text.get("no_sugar", "No Sugar"))]:
                tk.Radiobutton(sf, text=l, variable=sweet_var, value=v,
                               font=("Arial", 10)).pack(side="left", padx=5)
            opts["sweet"] = sweet_var

            # 冰量
            tk.Label(frm, text=text.get("ice", "Ice Level") + ":",
                     font=("Arial", 11, "bold")).pack(anchor="w")
            ice_var = tk.StringVar(value="full_ice")
            icf = tk.Frame(frm)
            icf.pack(anchor="w", pady=(0, 8))
            for v, l in [("full_ice", text.get("full_ice", "Normal Ice")),
                         ("less_ice", text.get("less_ice", "Less Ice")),
                         ("no_ice",   text.get("no_ice",   "No Ice")),
                         ("hot",      text.get("hot",      "Hot"))]:
                tk.Radiobutton(icf, text=l, variable=ice_var, value=v,
                               font=("Arial", 10)).pack(side="left", padx=5)
            opts["ice"] = ice_var

        if is_food:
            # 辣度
            tk.Label(frm, text=text.get("spicy", "Spiciness") + ":",
                     font=("Arial", 11, "bold")).pack(anchor="w")
            spicy_var = tk.StringVar(value="normal")
            spf = tk.Frame(frm)
            spf.pack(anchor="w", pady=(0, 8))
            for v, l in [("normal",      text.get("normal",      "Normal")),
                         ("mild",        text.get("mild",        "Mild")),
                         ("medium",      text.get("medium",      "Medium")),
                         ("extra_spicy", text.get("extra_spicy", "Extra Spicy"))]:
                tk.Radiobutton(spf, text=l, variable=spicy_var, value=v,
                               font=("Arial", 10)).pack(side="left", padx=5)
            opts["spicy"] = spicy_var

        # 備註
        tk.Label(frm, text=text.get("note", "Note") + ":",
                 font=("Arial", 11, "bold")).pack(anchor="w")
        note_var = tk.StringVar()
        tk.Entry(frm, textvariable=note_var, width=40,
                 font=("Arial", 10)).pack(anchor="w", pady=(0, 15))

        bf = tk.Frame(frm)
        bf.pack()

        def on_ok():
            custom = {k: text.get(v.get(), v.get()) for k, v in opts.items()}
            note = note_var.get().strip()
            if note:
                custom["note"] = note
            result[0] = custom
            win.destroy()

        def on_cancel():
            result[0] = None
            win.destroy()

        tk.Button(bf, text=text.get("confirm", "Confirm"), command=on_ok,
                  bg="#4CAF50", fg="white", font=("Arial", 11),
                  padx=20, pady=5).grid(row=0, column=0, padx=10)
        tk.Button(bf, text=text.get("cancel", "Cancel"), command=on_cancel,
                  bg="#f44336", fg="white", font=("Arial", 11),
                  padx=20, pady=5).grid(row=0, column=1, padx=10)

        self.center_window(win)
        self.master.wait_window(win)
        return result[0]

    # ──────────────────────────────────────────────────────────
    # 加入購物車
    # ──────────────────────────────────────────────────────────
    def add_to_cart(self, item, qty_var):
        global free_beverage_map

        try:
            quantity = qty_var.get()
            if quantity <= 0:
                raise ValueError
        except:
            messagebox.showerror(text.get("quantity_error", "Error"),
                                 text.get("quantity_error", "Quantity must be > 0"))
            return

        # 定制對話框
        customization = self.show_customization_dialog(item)
        if customization is None:
            return  # 用戶取消

        orig_price = item[4]
        price      = self.get_price(orig_price)
        name       = self.get_item_name(item)

        cart_item = {
            "id":             item[0],
            "name":           name,
            "price":          price,
            "original_price": orig_price,
            "quantity":       quantity,
            "is_main":        item[9] in ["main_course", "combo"],
            "type":           item[9],
            "customization":  customization,
        }

        # 合併相同商品（同定制）
        found = False
        for idx, existing in enumerate(cart):
            if (existing["id"] == item[0]
                    and existing.get("customization") == customization
                    and not existing.get("is_free", False)):
                cart[idx]["quantity"] += quantity
                found = True
                if cart[idx]["is_main"]:
                    self.offer_free_beverage_for_quantity(idx, quantity)
                break

        if not found:
            cart.append(cart_item)
            if cart_item["is_main"]:
                self.offer_free_beverage(item, len(cart) - 1)

        messagebox.showinfo(text.get("added", "Added"),
                            f"{text.get('added','Added')}: {name} × {quantity}")

        self.update_cart_display()
        self.update_cart_badge()

    def offer_free_beverage_for_quantity(self, main_idx, added_qty):
        global free_beverage_map
        if main_idx in free_beverage_map:
            cart[free_beverage_map[main_idx]]["quantity"] += added_qty
            self.update_cart_display()

    def offer_free_beverage(self, main_item, main_idx):
        beverages = [i for i in menu if i[9] == "beverage" and i[8] == main_item[8]]
        if not beverages:
            return

        win = tk.Toplevel(self.master)
        win.title(text.get("free_beverage", "Free Beverage"))
        win.geometry("480x420")
        win.transient(self.master)
        win.grab_set()

        main_name = self.get_item_name(main_item)
        tk.Label(win,
                 text=f"{text.get('select_beverage','Select')} ({main_name} ×{cart[main_idx]['quantity']})",
                 font=("Arial", 13, "bold"), wraplength=440).pack(pady=15)

        frm = tk.Frame(win)
        frm.pack(fill="both", expand=True, padx=20, pady=5)
        c2  = tk.Canvas(frm)
        sb2 = ttk.Scrollbar(frm, orient="vertical", command=c2.yview)
        sf2 = ttk.Frame(c2)
        sf2.bind("<Configure>", lambda e: c2.configure(scrollregion=c2.bbox("all")))
        c2.create_window((0, 0), window=sf2, anchor="nw")
        c2.configure(yscrollcommand=sb2.set)
        c2.pack(side="left", fill="both", expand=True)
        sb2.pack(side="right", fill="y")

        sel = tk.IntVar(value=-1)
        for i, bev in enumerate(beverages):
            bev_name = self.get_item_name(bev)
            row = tk.Frame(sf2, bg="#f9f9f9", pady=3)
            row.pack(fill="x", padx=5, pady=2)
            tk.Radiobutton(row,
                           text=f"{bev[0]}. {bev_name} (${bev[4]:.0f})",
                           variable=sel, value=i,
                           font=("Arial", 12), bg="#f9f9f9").pack(anchor="w", padx=10)

        bf = tk.Frame(win)
        bf.pack(pady=12)

        def on_select():
            global free_beverage_map
            s = sel.get()
            if s < 0:
                messagebox.showinfo("Info", text.get("select_beverage", "Please select"))
                return
            chosen = beverages[s]
            qty    = cart[main_idx]["quantity"]
            free_bev = {
                "id":             chosen[0],
                "name":           f"{self.get_item_name(chosen)} ({text.get('free_item','Free')})",
                "price":          0,
                "original_price": chosen[4],
                "quantity":       qty,
                "is_free":        True,
                "linked_to_main": main_idx,
                "type":           "beverage",
                "customization":  {},
            }
            cart.append(free_bev)
            free_beverage_map[main_idx] = len(cart) - 1
            self.update_cart_display()
            self.update_cart_badge()
            win.destroy()

        tk.Button(bf, text=text.get("select", "Select"), command=on_select,
                  padx=25, pady=8, font=("Arial", 12),
                  bg="#4CAF50", fg="white").grid(row=0, column=0, padx=12)
        tk.Button(bf, text=text.get("cancel", "Cancel"), command=win.destroy,
                  padx=25, pady=8, font=("Arial", 12),
                  bg="#f44336", fg="white").grid(row=0, column=1, padx=12)

        self.center_window(win)

    # ──────────────────────────────────────────────────────────
    # 新增：購物車 Tab 角標
    # ──────────────────────────────────────────────────────────
    def update_cart_badge(self):
        total_qty = sum(i["quantity"] for i in cart)
        badge = (f"  {text.get('view_cart','Cart')} ({total_qty})  "
                 if total_qty else
                 f"  {text.get('view_cart','Cart')}  ")
        self.tab_control.tab(1, text=badge)

    # ──────────────────────────────────────────────────────────
    # 新增：優惠碼
    # ──────────────────────────────────────────────────────────
    def apply_coupon(self):
        global coupon_discount, current_coupon
        code = self.coupon_entry.get().strip().upper()

        if code in COUPONS:
            ctype, cval = COUPONS[code]
            current_coupon = code
            subtotal = sum(i["price"] * i["quantity"] for i in cart)
            coupon_discount = (min(cval, subtotal) if ctype == "fixed"
                               else round(subtotal * cval / 100))
            self.coupon_msg.config(
                text=f"✓ {text.get('coupon_applied','Applied!')} (−${coupon_discount})",
                fg="#27ae60")
        else:
            coupon_discount = 0
            current_coupon  = ""
            self.coupon_msg.config(
                text=f"✗ {text.get('coupon_invalid','Invalid')}",
                fg="#e74c3c")

        self.update_cart_display()

    # ──────────────────────────────────────────────────────────
    # 更新購物車顯示
    # ──────────────────────────────────────────────────────────
    def update_cart_display(self):
        global coupon_discount
        for w in self.scrollable_cart.winfo_children():
            w.destroy()

        if not cart:
            ttk.Label(self.scrollable_cart,
                      text=text.get("cart_empty", "Cart empty"),
                      font=("Arial", 12)).pack(pady=20)
            self.subtotal_label.config(text=f"{text.get('subtotal','Subtotal')}: $0")
            self.discount_label.config(text="")
            self.total_label.config(text=f"{text.get('total','Total')}: $0")
            return

        subtotal = 0

        for i, item in enumerate(cart):
            card = tk.Frame(self.scrollable_cart, bg="#ffffff", relief="groove", bd=1)
            card.pack(fill="x", padx=8, pady=3, ipady=4)

            sub = item["price"] * item["quantity"]
            subtotal += sub

            txt_frm = tk.Frame(card, bg="#ffffff")
            txt_frm.pack(side="left", fill="x", expand=True, padx=10)

            if item.get("is_free", False):
                linked = item.get("linked_to_main")
                if linked is not None and 0 <= linked < len(cart):
                    info_str = (f"{text.get('free_with_main','Free w/ main')}: "
                                f"{cart[linked]['name']}")
                else:
                    info_str = text.get("free_item", "Free")
                tk.Label(txt_frm,
                         text=f"{i+1}. {item['name']} ×{item['quantity']}  [{info_str}]",
                         font=("Arial", 10), bg="#ffffff", fg="#27ae60",
                         wraplength=420).pack(anchor="w")
            else:
                tk.Label(txt_frm,
                         text=f"{i+1}. {item['name']} ×{item['quantity']} = ${sub:.0f}",
                         font=("Arial", 11, "bold"), bg="#ffffff").pack(anchor="w")
                if is_student:
                    orig_sub = item["original_price"] * item["quantity"]
                    tk.Label(txt_frm,
                             text=f"   ({text.get('original_price','Orig')}: ${orig_sub:.0f})",
                             font=("Arial", 9), bg="#ffffff", fg="#999").pack(anchor="w")

            # 顯示定制選項
            custom = item.get("customization", {})
            if custom:
                parts = [v for k, v in custom.items() if k != "note"]
                note  = custom.get("note", "")
                if parts:
                    tk.Label(txt_frm, text=" | ".join(parts),
                             font=("Arial", 9), bg="#ffffff",
                             fg="#7f8c8d").pack(anchor="w")
                if note:
                    tk.Label(txt_frm, text=f"📝 {note}",
                             font=("Arial", 9, "italic"), bg="#ffffff",
                             fg="#95a5a6").pack(anchor="w")

            # 操作按鈕（非免費商品）
            if not item.get("is_free", False):
                act = tk.Frame(card, bg="#ffffff")
                act.pack(side="right", padx=5)
                ttk.Button(act, text=text.get("modify_quantity", "Edit Qty"),
                           command=lambda idx=i: self.modify_quantity(idx),
                           width=10).pack(side="left", padx=2)
                ttk.Button(act, text=text.get("delete_item", "Delete"),
                           command=lambda idx=i: self.delete_item(idx),
                           width=7).pack(side="left", padx=2)

        # 合計
        self.subtotal_label.config(
            text=f"{text.get('subtotal','Subtotal')}: ${subtotal:.0f}")

        if current_coupon and current_coupon in COUPONS:
            ctype, cval = COUPONS[current_coupon]
            coupon_discount = (min(cval, subtotal) if ctype == "fixed"
                               else round(subtotal * cval / 100))
            self.discount_label.config(
                text=f"🎟 {text.get('coupon_discount','Coupon')} [{current_coupon}]: −${coupon_discount:.0f}",
                fg="#e74c3c")
        else:
            coupon_discount = 0
            self.discount_label.config(text="")

        final = max(0, subtotal - coupon_discount)
        self.total_label.config(text=f"{text.get('total','Total')}: ${final:.0f}")

    # ──────────────────────────────────────────────────────────
    # 修改數量
    # ──────────────────────────────────────────────────────────
    def modify_quantity(self, item_index):
        global free_beverage_map
        item = cart[item_index]

        win = tk.Toplevel(self.master)
        win.title(text.get("modify_quantity", "Modify Quantity"))
        win.geometry("380x200")
        win.transient(self.master)
        win.grab_set()

        tk.Label(win, text=item["name"],
                 font=("Arial", 12, "bold"), wraplength=360).pack(pady=(15, 5))

        qf = tk.Frame(win)
        qf.pack(pady=10)

        tk.Label(qf, text=text.get("enter_quantity", "Qty:"),
                 font=("Arial", 12)).pack(side="left", padx=5)
        qty_var = tk.IntVar(value=item["quantity"])

        tk.Button(qf, text="−", font=("Arial", 12), bg="#ecf0f1",
                  relief="flat", width=2,
                  command=lambda: qty_var.set(max(1, qty_var.get() - 1))).pack(side="left")
        tk.Entry(qf, textvariable=qty_var, width=4,
                 font=("Arial", 12), justify="center").pack(side="left", padx=3)
        tk.Button(qf, text="+", font=("Arial", 12), bg="#ecf0f1",
                  relief="flat", width=2,
                  command=lambda: qty_var.set(qty_var.get() + 1)).pack(side="left")

        bf = tk.Frame(win)
        bf.pack(pady=15)

        def on_ok():
            try:
                qty = qty_var.get()
                if qty <= 0:
                    raise ValueError
                cart[item_index]["quantity"] = qty
                if item_index in free_beverage_map:
                    cart[free_beverage_map[item_index]]["quantity"] = qty
                self.update_cart_display()
                self.update_cart_badge()
                messagebox.showinfo(text.get("updated", "Updated"),
                                    text.get("updated", "Updated"))
                win.destroy()
            except:
                messagebox.showerror(text.get("quantity_error", "Error"),
                                     text.get("quantity_error", "Qty must be > 0"))

        tk.Button(bf, text=text.get("confirm", "OK"), command=on_ok,
                  bg="#4CAF50", fg="white", font=("Arial", 11),
                  padx=20, pady=5).grid(row=0, column=0, padx=10)
        tk.Button(bf, text=text.get("cancel", "Cancel"), command=win.destroy,
                  bg="#f44336", fg="white", font=("Arial", 11),
                  padx=20, pady=5).grid(row=0, column=1, padx=10)

        self.center_window(win)

    # ──────────────────────────────────────────────────────────
    # 刪除商品
    # ──────────────────────────────────────────────────────────
    def delete_item(self, item_index):
        global free_beverage_map

        if item_index in free_beverage_map:
            bev_idx    = free_beverage_map[item_index]
            to_remove  = sorted([item_index, bev_idx], reverse=True)
            for idx in to_remove:
                cart.pop(idx)
            del free_beverage_map[item_index]

            new_map = {}
            for mi, bi in free_beverage_map.items():
                new_mi, new_bi = mi, bi
                for removed in sorted([item_index, bev_idx]):
                    if new_mi > removed: new_mi -= 1
                    if new_bi > removed: new_bi -= 1
                new_map[new_mi] = new_bi
            free_beverage_map = new_map
        else:
            linked_main = next(
                (m for m, b in free_beverage_map.items() if b == item_index), None)
            if linked_main is not None:
                del free_beverage_map[linked_main]
                new_map = {}
                for m, b in free_beverage_map.items():
                    new_map[m] = b if b < item_index else b - 1
                free_beverage_map = new_map
            cart.pop(item_index)

        self.update_cart_display()
        self.update_cart_badge()
        messagebox.showinfo(text.get("deleted", "Deleted"),
                            text.get("deleted", "Deleted"))

    # ──────────────────────────────────────────────────────────
    # 結帳
    # ──────────────────────────────────────────────────────────
    def checkout(self):
        global cart, orders, order_number, free_beverage_map
        global coupon_discount, current_coupon

        if not cart:
            messagebox.showinfo(text.get("cart_empty", "Empty"),
                                text.get("cart_empty", "Cart is empty"))
            return

        name  = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()

        if not name:
            messagebox.showerror("Error", text.get("enter_name", "Enter your name"))
            return
        if not re.match(r'^\d{8}$', phone):
            messagebox.showerror("Error", text.get("invalid_phone", "8-digit phone required"))
            return

        subtotal    = sum(i["price"] * i["quantity"] for i in cart)
        final_total = max(0, subtotal - coupon_discount)

        order_number += 1
        order = {
            "number":          order_number,
            "name":            name,
            "phone":           phone,
            "items":           cart.copy(),
            "subtotal":        subtotal,
            "coupon_code":     current_coupon,
            "coupon_discount": coupon_discount,
            "total":           final_total,
            "status":          "pending",
            "status_text":     text.get("pending", "Pending"),
            "is_student":      is_student,
            "order_type":      order_type,
            "table_number":    table_number,
            "time":            self.get_hk_time().strftime('%Y-%m-%d %H:%M'),
        }

        orders.append(order)
        self.show_order_success(order)

        cart.clear()
        free_beverage_map.clear()
        coupon_discount = 0
        current_coupon  = ""

        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.coupon_entry.delete(0, tk.END)
        self.coupon_msg.config(text="")

        self.update_cart_display()
        self.update_cart_badge()
        self.update_orders_display()

    # ──────────────────────────────────────────────────────────
    # 訂單成功視窗
    # ──────────────────────────────────────────────────────────
    def show_order_success(self, order):
        win = tk.Toplevel(self.master)
        win.title(text.get("order_success", "Order Success!"))
        win.geometry("620x750")
        win.transient(self.master)
        win.grab_set()

        frm = tk.Frame(win)
        frm.pack(fill="both", expand=True, padx=20, pady=15)

        canvas = tk.Canvas(frm)
        sb     = ttk.Scrollbar(frm, orient="vertical", command=canvas.yview)
        sf     = ttk.Frame(canvas)
        sf.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=sf, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        ttk.Label(sf, text=f"✓  {text.get('order_success','Order Success!')}",
                  font=("Arial", 18, "bold"),
                  foreground="#27ae60").pack(pady=12)

        ot_str = text.get(order["order_type"], order["order_type"])
        if order["order_type"] == "dine_in" and order["table_number"]:
            ot_str += f"  |  {text.get('table_number','Table')}: {order['table_number']}"

        for txt_str, fnt in [
            (f"#{order['number']}", "Arial 15 bold"),
            (f"{text.get('customer_name','Customer')}: {order['name']}", "Arial 12"),
            (f"{text.get('contact_phone','Phone')}: {order['phone']}", "Arial 12"),
            (f"{text.get('order_type','Type')}: {ot_str}", "Arial 12"),
            (f"{text.get('student_status','Status')}: "
             f"{text.get('student','Student') if order['is_student'] else text.get('non_student','Non-student')}",
             "Arial 11"),
            (f"⏰  {order['time']}", "Arial 11"),
        ]:
            ttk.Label(sf, text=txt_str, font=fnt).pack(anchor="w", pady=2)

        ttk.Separator(sf, orient="horizontal").pack(fill="x", pady=10)
        ttk.Label(sf, text=text.get("order_items", "Items") + ":",
                  font=("Arial", 14, "bold")).pack(anchor="w", pady=5)

        for item in order["items"]:
            if item.get("is_free", False):
                ttk.Label(sf, text=f"  ✓  {item['name']} ×{item['quantity']}",
                          font=("Arial", 11), foreground="#27ae60",
                          wraplength=530).pack(anchor="w", pady=2)
            else:
                sub = item["price"] * item["quantity"]
                ttk.Label(sf,
                          text=f"  •  {item['name']} ×{item['quantity']} = ${sub:.0f}",
                          font=("Arial", 11), wraplength=530).pack(anchor="w", pady=2)

                custom = item.get("customization", {})
                if custom:
                    parts = [v for k, v in custom.items() if k != "note"]
                    note  = custom.get("note", "")
                    if parts:
                        ttk.Label(sf, text=f"    [{', '.join(parts)}]",
                                  font=("Arial", 9), foreground="#7f8c8d").pack(anchor="w")
                    if note:
                        ttk.Label(sf, text=f"    📝 {note}",
                                  font=("Arial", 9), foreground="#7f8c8d").pack(anchor="w")

                if order["is_student"]:
                    orig_sub = item["original_price"] * item["quantity"]
                    ttk.Label(sf,
                              text=f"    ({text.get('original_price','Orig')}: ${orig_sub:.0f})",
                              font=("Arial", 10),
                              foreground="#999").pack(anchor="w")

        ttk.Separator(sf, orient="horizontal").pack(fill="x", pady=10)

        ttk.Label(sf, text=f"{text.get('subtotal','Subtotal')}: ${order['subtotal']:.0f}",
                  font=("Arial", 12)).pack(anchor="w", pady=2)

        if order["coupon_code"]:
            ttk.Label(sf,
                      text=f"🎟  [{order['coupon_code']}]: −${order['coupon_discount']:.0f}",
                      font=("Arial", 12), foreground="#e74c3c").pack(anchor="w", pady=2)

        ttk.Label(sf, text=f"{text.get('order_total','Total')}: ${order['total']:.0f}",
                  font=("Arial", 16, "bold")).pack(anchor="w", pady=4)
        ttk.Label(sf, text=f"{text.get('status','Status')}: {order['status_text']}",
                  font=("Arial", 12)).pack(anchor="w", pady=2)
        ttk.Label(sf, text=text.get("payment_instruction",
                                    "Please go to counter to pay"),
                  wraplength=530, font=("Arial", 11)).pack(pady=10)

        bf = tk.Frame(win)
        bf.pack(pady=15)

        tk.Button(bf, text=f"✓  {text.get('confirm','OK')}",
                  command=win.destroy, bg="#4CAF50", fg="white",
                  font=("Arial", 12), padx=25, pady=8).grid(row=0, column=0, padx=10)

        # 新增：匯出收據按鈕
        tk.Button(bf, text=f"📄  {text.get('export_receipt','Export Receipt')}",
                  command=lambda: self.export_receipt(order),
                  bg="#3498db", fg="white",
                  font=("Arial", 12), padx=15, pady=8).grid(row=0, column=1, padx=10)

        self.center_window(win)

    # ──────────────────────────────────────────────────────────
    # 新增：匯出收據
    # ──────────────────────────────────────────────────────────
    def export_receipt(self, order):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"receipt_{order['number']}.txt")
        if not path:
            return

        ot_str = order["order_type"].replace("_", " ").title()
        if order.get("table_number"):
            ot_str += f" (Table: {order['table_number']})"

        lines = [
            "=" * 50,
            "  RESTAURANT RECEIPT",
            "=" * 50,
            f"Order #   : {order['number']}",
            f"Date/Time : {order['time']}",
            f"Customer  : {order['name']}",
            f"Phone     : {order['phone']}",
            f"Type      : {ot_str}",
            f"Student   : {'Yes' if order['is_student'] else 'No'}",
            "-" * 50,
            "ITEMS:",
        ]

        for item in order["items"]:
            if item.get("is_free", False):
                lines.append(f"  [FREE] {item['name']} ×{item['quantity']}")
            else:
                sub = item["price"] * item["quantity"]
                lines.append(f"  {item['name']} ×{item['quantity']} = ${sub:.0f}")
                custom = item.get("customization", {})
                parts  = [v for k, v in custom.items() if k != "note"]
                note   = custom.get("note", "")
                if parts: lines.append(f"    Options : {', '.join(parts)}")
                if note:  lines.append(f"    Note    : {note}")

        lines += ["-" * 50, f"Subtotal  : ${order['subtotal']:.0f}"]
        if order["coupon_code"]:
            lines.append(f"Coupon    : [{order['coupon_code']}] −${order['coupon_discount']:.0f}")
        lines += [
            f"TOTAL     : ${order['total']:.0f}",
            "-" * 50,
            f"Status    : {order['status_text']}",
            "Please proceed to counter to pay.",
            "=" * 50,
            "Thank you for dining with us!",
        ]

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            messagebox.showinfo("OK", text.get("receipt_saved", "Receipt saved!"))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ──────────────────────────────────────────────────────────
    # 更新訂單歷史顯示
    # ──────────────────────────────────────────────────────────
    def update_orders_display(self):
        for w in self.scrollable_orders.winfo_children():
            w.destroy()

        if not orders:
            ttk.Label(self.scrollable_orders,
                      text=text.get("no_orders", "No order history"),
                      font=("Arial", 12)).pack(pady=20)
            return

        for idx, order in enumerate(reversed(orders)):
            real_idx = len(orders) - 1 - idx
            sc       = STATUS_COLORS.get(order.get("status", "pending"), "#FFC107")

            row_frm = tk.Frame(self.scrollable_orders, bg="#ffffff",
                               relief="groove", bd=1)
            row_frm.pack(fill="x", padx=10, pady=5, ipady=6)

            tk.Frame(row_frm, bg=sc, width=6).pack(side="left", fill="y")

            content = tk.Frame(row_frm, bg="#ffffff")
            content.pack(side="left", fill="both", expand=True, padx=10)

            # 標題行
            hdr_row = tk.Frame(content, bg="#ffffff")
            hdr_row.pack(fill="x")
            tk.Label(hdr_row,
                     text=f"#{order['number']}  {order['name']}",
                     font=("Arial", 12, "bold"), bg="#ffffff").pack(side="left")
            tk.Label(hdr_row, text=order["status_text"],
                     bg=sc, fg="white", font=("Arial", 9, "bold"),
                     padx=8, pady=2).pack(side="right", padx=5)

            # 時間、電話、用餐方式
            tk.Label(content,
                     text=f"⏰ {order.get('time','')}  |  📞 {order['phone']}",
                     font=("Arial", 10), bg="#ffffff", fg="#666").pack(anchor="w")

            ot_str = text.get(order.get("order_type", ""), order.get("order_type", ""))
            if order.get("order_type") == "dine_in" and order.get("table_number"):
                ot_str += f" | {text.get('table_number','Table')}: {order['table_number']}"
            tk.Label(content, text=ot_str, font=("Arial", 10),
                     bg="#ffffff", fg="#666").pack(anchor="w")

            # 商品摘要
            non_free = [i for i in order["items"] if not i.get("is_free", False)]
            summary  = ", ".join(
                f"{i['name']} ×{i['quantity']}" for i in non_free[:3])
            if len(non_free) > 3:
                summary += f"  (+{len(non_free) - 3} more)"
            tk.Label(content, text=summary, font=("Arial", 10),
                     bg="#ffffff", fg="#555", wraplength=500).pack(anchor="w")

            # 金額
            total_str = f"{text.get('order_total','Total')}: ${order['total']:.0f}"
            if order.get("coupon_code"):
                total_str += f"  (−${order.get('coupon_discount',0):.0f} coupon)"
            tk.Label(content, text=total_str,
                     font=("Arial", 11, "bold"), bg="#ffffff").pack(anchor="w")

            # 新增：重新訂購按鈕
            btn_row = tk.Frame(content, bg="#ffffff")
            btn_row.pack(fill="x")
            tk.Button(btn_row, text=f"↺  {text.get('reorder','Reorder')}",
                      command=lambda o=order: self.reorder(o),
                      bg="#3498db", fg="white", font=("Arial", 9),
                      relief="flat", padx=8, pady=2).pack(side="right", pady=3)

    # ──────────────────────────────────────────────────────────
    # 新增：重新訂購
    # ──────────────────────────────────────────────────────────
    def reorder(self, order):
        added = 0
        for item in order["items"]:
            if item.get("is_free", False):
                continue
            menu_item = next((m for m in menu if m[0] == item["id"]), None)
            if menu_item:
                cart.append({
                    "id":             menu_item[0],
                    "name":           self.get_item_name(menu_item),
                    "price":          self.get_price(menu_item[4]),
                    "original_price": menu_item[4],
                    "quantity":       item["quantity"],
                    "is_main":        menu_item[9] in ["main_course", "combo"],
                    "type":           menu_item[9],
                    "customization":  item.get("customization", {}),
                })
                added += 1

        self.update_cart_display()
        self.update_cart_badge()

        if added:
            messagebox.showinfo(text.get("added", "Added"),
                                f"{added} item(s) added to cart!")
            self.tab_control.select(1)
        else:
            messagebox.showinfo("Info", "No items could be re-added.")

    # ──────────────────────────────────────────────────────────
    # 新增：管理員面板
    # ──────────────────────────────────────────────────────────
    def open_admin_panel(self):
        pwd_win = tk.Toplevel(self.master)
        pwd_win.title(text.get("admin_panel", "Admin Panel"))
        pwd_win.geometry("300x185")
        pwd_win.transient(self.master)
        pwd_win.grab_set()

        tk.Label(pwd_win, text=f"⚙  {text.get('admin_panel','Admin Panel')}",
                 font=("Arial", 14, "bold")).pack(pady=12)
        tk.Label(pwd_win, text=text.get("admin_password", "Password:"),
                 font=("Arial", 11)).pack()

        pwd_var = tk.StringVar()
        entry   = tk.Entry(pwd_win, textvariable=pwd_var, show="*",
                           font=("Arial", 12), width=20)
        entry.pack(pady=6)
        entry.focus()

        def login():
            if pwd_var.get() == ADMIN_PASSWORD:
                pwd_win.destroy()
                self.show_admin_panel()
            else:
                messagebox.showerror(
                    "Error", text.get("wrong_password", "Wrong password"))
                entry.delete(0, tk.END)

        entry.bind("<Return>", lambda e: login())

        bf = tk.Frame(pwd_win)
        bf.pack(pady=6)
        tk.Button(bf, text=text.get("confirm", "Login"), command=login,
                  bg="#2c3e50", fg="white", font=("Arial", 11),
                  padx=15, pady=5).grid(row=0, column=0, padx=8)
        tk.Button(bf, text=text.get("cancel", "Cancel"), command=pwd_win.destroy,
                  bg="#95a5a6", fg="white", font=("Arial", 11),
                  padx=15, pady=5).grid(row=0, column=1, padx=8)

        self.center_window(pwd_win)

    def show_admin_panel(self):
        win = tk.Toplevel(self.master)
        win.title(f"⚙  {text.get('admin_panel','Admin Panel')}")
        win.geometry("960x680")
        win.transient(self.master)

        tc = ttk.Notebook(win)
        order_tab = ttk.Frame(tc)
        stats_tab = ttk.Frame(tc)
        tc.add(order_tab, text=f"  {text.get('orders','Orders')}  ")
        tc.add(stats_tab, text=f"  {text.get('statistics','Stats')}  ")
        tc.pack(fill="both", expand=True)

        self._build_order_management(order_tab)
        self._build_statistics(stats_tab)
        self.center_window(win)

    # 管理員：訂單管理
    def _build_order_management(self, parent):
        hdr = tk.Frame(parent, bg="#2c3e50", pady=6)
        hdr.pack(fill="x")
        tk.Label(hdr,
                 text=f"📋  {text.get('orders','Orders')} — {text.get('update_status','Update Status')}",
                 font=("Arial", 13, "bold"), bg="#2c3e50", fg="white").pack(padx=15)

        STATUS_INFO = [
            ("pending",   text.get("pending",   "Pending"),   "#FFC107"),
            ("preparing", text.get("preparing", "Preparing"), "#2196F3"),
            ("ready",     text.get("ready",     "Ready"),     "#4CAF50"),
            ("completed", text.get("completed", "Completed"), "#9E9E9E"),
        ]

        legend = tk.Frame(parent, pady=4)
        legend.pack(fill="x", padx=10)
        for _, lbl, col in STATUS_INFO:
            tk.Label(legend, text=f"  ● {lbl}  ",
                     bg=col, fg="white", font=("Arial", 9)).pack(side="left", padx=2)

        area = tk.Frame(parent)
        area.pack(fill="both", expand=True, padx=10, pady=5)

        canvas = tk.Canvas(area)
        sb     = ttk.Scrollbar(area, orient="vertical", command=canvas.yview)
        sf     = ttk.Frame(canvas)
        sf.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=sf, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        if not orders:
            ttk.Label(sf, text=text.get("no_orders", "No orders"),
                      font=("Arial", 12)).pack(pady=20)
            return

        sc_map  = {s[0]: s[2] for s in STATUS_INFO}

        for real_idx, order in enumerate(reversed(orders)):
            oi     = len(orders) - 1 - real_idx
            cur_sc = sc_map.get(order.get("status", "pending"), "#FFC107")

            row = tk.Frame(sf, bg="#ffffff", relief="groove", bd=1)
            row.pack(fill="x", padx=5, pady=3, ipady=5)

            left = tk.Frame(row, bg="#ffffff")
            left.pack(side="left", fill="both", expand=True, padx=10)

            tk.Label(left,
                     text=(f"#{order['number']}  {order['name']}  "
                           f"📞 {order['phone']}  ⏰ {order.get('time','')}"),
                     font=("Arial", 11, "bold"), bg="#ffffff").pack(anchor="w")

            items_str = " | ".join(
                f"{i['name']} ×{i['quantity']}"
                for i in order["items"] if not i.get("is_free", False))
            tk.Label(left, text=items_str, font=("Arial", 9),
                     bg="#ffffff", fg="#666", wraplength=540).pack(anchor="w")
            tk.Label(left,
                     text=f"{text.get('order_total','Total')}: ${order['total']:.0f}",
                     font=("Arial", 10), bg="#ffffff").pack(anchor="w")

            right = tk.Frame(row, bg="#ffffff")
            right.pack(side="right", padx=10)

            badge = tk.Label(right, text=order["status_text"],
                             bg=cur_sc, fg="white",
                             font=("Arial", 9, "bold"), padx=10, pady=3)
            badge.pack(pady=(0, 4))

            for sk, sl, col in STATUS_INFO:
                if sk != order.get("status", "pending"):
                    tk.Button(right, text=sl,
                              bg=col, fg="white", font=("Arial", 8),
                              relief="flat", padx=5, pady=2,
                              command=lambda idx=oi, s=sk, l=sl, b=badge, c=col:
                              self._update_order_status(idx, s, l, b, c)
                              ).pack(fill="x", pady=1)

    def _update_order_status(self, order_idx, status_key, status_text,
                             badge_lbl, color):
        orders[order_idx]["status"]      = status_key
        orders[order_idx]["status_text"] = status_text
        badge_lbl.config(text=status_text, bg=color)
        self.update_orders_display()

    # 管理員：銷售統計
    def _build_statistics(self, parent):
        hdr = tk.Frame(parent, bg="#2c3e50", pady=6)
        hdr.pack(fill="x")
        tk.Label(hdr, text=f"📊  {text.get('statistics','Statistics')}",
                 font=("Arial", 13, "bold"), bg="#2c3e50", fg="white").pack(padx=15)

        frm = tk.Frame(parent, padx=20, pady=15)
        frm.pack(fill="both", expand=True)

        if not orders:
            tk.Label(frm, text=text.get("no_orders", "No orders yet"),
                     font=("Arial", 12)).pack(pady=30)
            return

        total_cnt = len(orders)
        total_rev = sum(o["total"] for o in orders)
        stu_cnt   = sum(1 for o in orders if o["is_student"])
        avg_order = total_rev / total_cnt if total_cnt else 0

        # 彩色摘要卡片
        cards = tk.Frame(frm)
        cards.pack(fill="x", pady=10)
        for title, val, col in [
            (text.get("total_orders", "Total Orders"), total_cnt,          "#3498db"),
            (text.get("total_revenue", "Revenue"),     f"${total_rev:.0f}","#27ae60"),
            (text.get("student", "Students"),           stu_cnt,           "#9b59b6"),
            ("Avg Order",                               f"${avg_order:.0f}","#e67e22"),
        ]:
            c = tk.Frame(cards, bg=col, padx=15, pady=12)
            c.pack(side="left", fill="both", expand=True, padx=4)
            tk.Label(c, text=title, font=("Arial", 9),  bg=col, fg="white").pack()
            tk.Label(c, text=str(val), font=("Arial", 17, "bold"),
                     bg=col, fg="white").pack()

        # 熱門商品表
        tk.Label(frm, text=f"🏆  {text.get('popular_items','Popular Items')}",
                 font=("Arial", 12, "bold")).pack(anchor="w", pady=(18, 4))

        item_qty = {}
        item_rev = {}
        for o in orders:
            for i in o["items"]:
                if not i.get("is_free", False):
                    iid = i["id"]
                    item_qty[iid] = item_qty.get(iid, 0) + i["quantity"]
                    item_rev[iid] = item_rev.get(iid, 0) + i["price"] * i["quantity"]

        sorted_items = sorted(item_qty.items(), key=lambda x: x[1], reverse=True)

        th = tk.Frame(frm, bg="#2c3e50")
        th.pack(fill="x")
        for col_name, w in [("Item", 22), ("Qty", 8), ("Revenue", 10)]:
            tk.Label(th, text=col_name, font=("Arial", 10, "bold"),
                     bg="#2c3e50", fg="white", width=w, anchor="w").pack(
                side="left", padx=5, pady=4)

        for iid, qty in sorted_items[:10]:
            mi   = next((m for m in menu if m[0] == iid), None)
            name = self.get_item_name(mi) if mi else str(iid)
            rev  = item_rev.get(iid, 0)

            data_row = tk.Frame(frm, bg="#f9f9f9")
            data_row.pack(fill="x")
            ttk.Separator(frm, orient="horizontal").pack(fill="x")
            for val, w in [(name, 22), (str(qty), 8), (f"${rev:.0f}", 10)]:
                tk.Label(data_row, text=val, font=("Arial", 10),
                         bg="#f9f9f9", anchor="w", width=w).pack(
                    side="left", padx=5, pady=3)

        # 狀態分佈
        tk.Label(frm, text=f"📋  {text.get('status','Status')} Breakdown",
                 font=("Arial", 12, "bold")).pack(anchor="w", pady=(18, 4))

        sc_count = {}
        for o in orders:
            s = o.get("status_text", "Pending")
            sc_count[s] = sc_count.get(s, 0) + 1

        for s, cnt in sc_count.items():
            tk.Label(frm, text=f"  {s}: {cnt}",
                     font=("Arial", 11)).pack(anchor="w")


# ============================================================
def main():
    root = tk.Tk()
    root.title("Restaurant Ordering System")
    root.geometry("1050x750")
    root.minsize(900, 600)
    RestaurantApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
