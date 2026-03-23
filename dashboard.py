import flet as ft
import os

# We use this constant for our text file name
FILE_NAME = "inventory.txt"

def init_file():
    # Create the text file if it doesn't exist yet
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w") as f:
            pass 

def main(page: ft.Page):
    # Window setup
    page.title = "Inventory CRM Dashboard"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 30

    # Initialize the text file when the app launches
    init_file()

    # UI: INPUT FIELDS
    name_input = ft.TextField(label="Product Name", width=250, border_radius=8)
    qty_input = ft.TextField(label="Qty", width=100, border_radius=8)
    price_input = ft.TextField(label="Price ($)", width=120, border_radius=8)

    # UI: DATA TABLE
    inventory_table = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("ID", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(label=ft.Text("Name", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(label=ft.Text("Quantity", weight=ft.FontWeight.BOLD), numeric=True),
            ft.DataColumn(label=ft.Text("Price", weight=ft.FontWeight.BOLD), numeric=True),
            ft.DataColumn(label=ft.Text("Action", weight=ft.FontWeight.BOLD)),
        ],
        rows=[]
    )

    # LOGIC: TEXT FILE OPERATIONS
    def load_data():
        # Clear the table before repopulating it
        inventory_table.rows.clear()
        
        # Read data from the text file
        with open(FILE_NAME, "r") as f:
            lines = f.readlines()
        
        # Populate the Flet GUI table
        for line in lines:
            if not line.strip(): 
                continue # Skip empty lines
            
            # Split the line by our pipe separator
            parts = line.strip().split("|")
            if len(parts) == 4:
                item_id, name, qty, price = parts
                inventory_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(item_id)),
                            ft.DataCell(ft.Text(name)),
                            ft.DataCell(ft.Text(qty)),
                            ft.DataCell(ft.Text(f"${float(price):.2f}")),
                            ft.DataCell(
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_color=ft.Colors.RED_400,
                                    data=item_id,  # Store the ID in the button
                                    on_click=delete_item,
                                    tooltip="Delete Item"
                                )
                            ),
                        ]
                    )
                )
        page.update()

    def add_item(e):
        # Validation to prevent empty fields
        if not name_input.value or not qty_input.value or not price_input.value:
            return 

        try:
            # Convert input values to numbers
            qty = int(str(qty_input.value))
            price = float(str(price_input.value))
        except ValueError:
            return # Cancel if the user typed letters instead of numbers

        # Calculate the next ID by reading the last line of the file
        next_id = 1
        with open(FILE_NAME, "r") as f:
            lines = f.readlines()
            # Filter out any accidental empty lines at the end
            valid_lines = [line for line in lines if line.strip()]
            if valid_lines:
                last_line = valid_lines[-1].strip()
                last_id = int(last_line.split("|")[0])
                next_id = last_id + 1

        # Append the new record to the text file
        with open(FILE_NAME, "a") as f:
            f.write(f"{next_id}|{name_input.value}|{qty}|{price}\n")

        # Clear the UI input fields
        name_input.value = ""
        qty_input.value = ""
        price_input.value = ""
        
        # Refresh the table
        load_data()

    def delete_item(e):
        # Extract the ID from the clicked button
        target_id = str(e.control.data)
        
        # Read all lines
        with open(FILE_NAME, "r") as f:
            lines = f.readlines()
            
        # Write back everything EXCEPT the line with the matching ID
        with open(FILE_NAME, "w") as f:
            for line in lines:
                if not line.strip(): 
                    continue
                current_id = line.split("|")[0]
                if current_id != target_id:
                    f.write(line)
        
        # Refresh the table
        load_data()

    # Custom add button
    add_btn = ft.Button(
        content=ft.Row(
            controls=[ft.Icon(ft.Icons.ADD), ft.Text("Add Item")], 
            alignment=ft.MainAxisAlignment.CENTER
        ),
        on_click=add_item,
        height=50
    )

    # LAYOUT ASSEMBLY
    page.add(
        ft.Text("Local Inventory", size=28, weight=ft.FontWeight.BOLD),
        ft.Divider(height=20, color="transparent"),
        ft.Row(
            controls=[name_input, qty_input, price_input, add_btn], 
            alignment=ft.MainAxisAlignment.START,
            spacing=15
        ),
        ft.Divider(height=20, color="transparent"),
        inventory_table
    )
    # Load initial data on startup
    load_data()

ft.run(main)