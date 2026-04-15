import re
def checkout(self):
    global cart, orders, order_number, free_beverage_map
    global coupon_discount, current_coupon

    if not cart:
        messagebox.showinfo(text.get("cart_empty", "Empty"),
                            text.get("cart_empty", "Cart is empty"))
        return

    name = self.name_entry.get().strip()
    phone = self.phone_entry.get().strip()

    if not name:
        messagebox.showerror("Error", text.get("enter_name", "Enter your name"))
        return
    if not re.match(r'^\d{8}$', phone):
        messagebox.showerror("Error", text.get("invalid_phone", "8-digit phone required"))
        return