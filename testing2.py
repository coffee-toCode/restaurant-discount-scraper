import tkinter as tk
from tkinter import ttk
from app import response_list

root = tk.Tk()
root.title("Google Places API")

# Add a header label
header_label = ttk.Label(root, text="Google Places API", font=("Arial", 20))
header_label.pack(pady=20)

# Add a treeview to display the results
tree = ttk.Treeview(root)
tree["columns"] = ("Name", "Place ID", "Rating", "Types",
                   "User Ratings", "Latitude", "Longitude")
tree.heading("#0", text="Index", anchor="w")
tree.column("#0", anchor="w")
for col in tree["columns"]:
    tree.heading(col, text=col)
    for index, result in enumerate(response_list, start=1):
        values = (
        result.get("name", ""),
        result.get("place_id", ""),
        result.get("rating", ""),
        ", ".join(result.get("types", [])),
        result.get("user_ratings_total", ""),
        result.get("geometry", {}).get("location", {}).get("lat", ""),
        result.get("geometry", {}).get("location", {}).get("lng", "")
        )
# Check if the Place ID already exists in the treeview
    if result.get("place_id", "") not in (tree.item(iid)["values"][1] for iid in tree.get_children()):
        tree.insert("", "end", index, text=index, values=values)

# explode the "Types" column
new_data = []
for row in tree.get_children():
    values = tree.item(row)["values"]
    types = values[3].split(",")
    for t in types:
        new_row = [values[0], t.strip()]
        new_data.append(new_row)

# delete existing rows from the Treeview widget
tree.delete(*tree.get_children())

# insert new rows into the Treeview widget
for row in new_data:
    tree.insert("", "end", values=row)

tree.pack(fill="both", expand=True, padx=20, pady=20)

root.mainloop()
