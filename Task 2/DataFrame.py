import pandas as pd


def create_menu(self):
    global menu
    try:
        df = pd.read_excel("W:\comp gp project\menu_data.xlsx")
        menu = df.values.tolist()
        return True
    except Exception as e:
        print(f"Error loading menu: {e}")
        messagebox.showerror("Error", text.get("excel_load_error", "Failed to load menu"))
        return False