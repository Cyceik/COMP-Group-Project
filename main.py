import tkinter as tk
from restaurant_app import RestaurantApp

def main():
    root = tk.Tk()
    root.title("Restaurant Ordering System")
    root.geometry("1050x750")
    root.minsize(900, 600)
    RestaurantApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()