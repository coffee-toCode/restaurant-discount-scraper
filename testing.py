import tkinter as tk
from tkinter import ttk
from app import response_list
    
root = tk.Tk()
root.title("Google Places API")

# Add a header label
header_label = tk.Label(root, text="Google Places API", font=("Arial", 20))
header_label.pack(pady=20)

# Add a treeview to display the results
tree = tk.ttk.Treeview(root)
tree["columns"] = ("Name", "Place ID", "Rating", "Types", "User Ratings", "Latitude", "Longitude")
tree.heading("#0", text="Index")
tree.heading("Name", text="Name")
tree.heading("Place ID", text="Place ID")
tree.heading("Rating", text="Rating")
tree.heading("Types", text="Types")
tree.heading("User Ratings", text="User Ratings")
tree.heading("Latitude", text="Latitude")
tree.heading("Longitude", text="Longitude")

index = 0
for result in response_list:
    index += 1
    name = result.get("name", "")
    place_id = result.get("place_id", "")    
    rating = result.get("rating", "")
    types = ", ".join(result.get("types", []))
    user_ratings_total = result.get("user_ratings_total", "")
    latitude = result.get("geometry", {}).get("location", {}).get("lat", "")
    longitude = result.get("geometry", {}).get("location", {}).get("lng", "")
    tree.insert("", tk.END, index, text=index, values=(name, place_id, rating, types, user_ratings_total, latitude, longitude))

tree.pack(fill="both", expand=True, padx=20, pady=20)

root.mainloop()


"""This will display the results from `response_list` in a treeview widget with sortable columns. The user can interact with the treeview by clicking on the column headers to sort the results."""