# importing Tkinter
from tkinter import *
from tkinter.ttk import *
# importing pandas
import pandas as pd
# importing numpy
import numpy as np

pd.set_option('display.max_columns', None)

nash_starting_fans = .53
nash_current_fans = .63
cha_starting_fans = .42
cha_current_fans = .58

all_seats = 21315
upper_level = 10657
lower_level_total = 10657
lower_level_seats = (lower_level_total * 0.60).__round__()
box_seats = (lower_level_total * .35).__round__()
courtside_seats = (lower_level_total * .05).__round__()

seats = [upper_level, lower_level_seats, box_seats, courtside_seats]
seating = ['upper', 'lower_level', 'box_seats', 'courtside_seats']

seating_counts = pd.DataFrame([seats], columns=seating)
print(seating_counts)


def pricing_df_columns():
    seat_price = []
    for i in seating:
        i = f"{i}_pricing"
        seat_price.append(i)
    return seat_price


pricing = [40, 150, 300, 1500]
seat_pricing = pd.DataFrame([pricing], columns=pricing_df_columns())
print(seat_pricing)

sold_out_tix_revenue = pd.DataFrame()

# Iterate over the columns of DataFrame 1
for col1 in seating_counts.columns:
    # Iterate over the columns of DataFrame 2
    for col2 in seat_pricing.columns:
        # Multiply the columns and store the result in the result DataFrame
        sold_out_tix_revenue[f'{col1}_sold_out'] = seating_counts[col1] * seat_pricing[col2]


single_games_sold_out_tix_revenue = sold_out_tix_revenue * 41


def format_usd(value):
    return '${:,.2f}'.format(value)


# Apply formatting to all values in the result DataFrame
sold_out_tix_revenue = sold_out_tix_revenue.map(format_usd)
print(sold_out_tix_revenue)
single_games_sold_out_tix_revenue = single_games_sold_out_tix_revenue.map(format_usd)
print(single_games_sold_out_tix_revenue)


def price_increases():
    seat_price = []
    for i in pricing:
        price = i
        i = i * .05
        price = price + i
        seat_price.append(price)
    new_price = seat_price
    return new_price


new_seat_pricing = pd.DataFrame([price_increases()], columns=pricing_df_columns())


predicted_sold_out_tix_revenue = pd.DataFrame()

# Iterate over the columns of DataFrame 1
for col1 in seating_counts.columns:
    # Iterate over the columns of DataFrame 2
    for col2 in seat_pricing.columns:
        # Multiply the columns and store the result in the result DataFrame
        predicted_sold_out_tix_revenue[f'{col1}_sold_out_revenue'] = seating_counts[col1] * new_seat_pricing[col2]


predicted_sold_out_tix_revenue = predicted_sold_out_tix_revenue.map(format_usd)
print(predicted_sold_out_tix_revenue.sum())


def on_button_click():
    # message in the original pop-up window once the button is clicked
    label.config(text="Data Loaded!")

    # Upload the DataFrame
    df = predicted_sold_out_tix_revenue

    # Create a new window to display the DataFrame
    df_window = Toplevel(run_it)
    # give the new window a title to display
    df_window.title("Sample DataFrame")

    # Create a Treeview widget to display the DataFrame
    tree = Treeview(df_window, columns=list(df.columns), show='headings')

    # Add columns to the Treeview
    for col in df.columns:
        # set the column heading text for the specified column
        tree.heading(col, text=col)
        # centering the text in each column
        tree.column(col, anchor='center')

    # Insert data into the Treeview
    for i, row in df.iterrows():
        # insert a new row at the end of values of list 'row'
        tree.insert("", "end", values=list(row))

    # create a vertical scrollbar widget
    vsb = Scrollbar(df_window, orient="vertical", command=tree.yview)
    # Enable the scrollbar, positioned above the data here to ensure the
    # scrollbar will be at the side of the data shown
    tree.configure(yscrollcommand=vsb.set)

    # display the scrollbar
    vsb.pack(side="right", fill="y")
    # display the Treeview
    tree.pack(fill='y', expand=True, padx=10, pady=10)


# Create the main window
run_it = Tk()
# Title for main window
run_it.title("NBA Scores Data Analysis")

# Create a label
label = Label(run_it, text="Data Window")
# display the label with 10 pixels of padding
label.pack(pady=10)

# Create a button to open the stored data
button = Button(run_it, text="Click to Show DataFrame", command=on_button_click)
# display the button with 10 pixels of padding
button.pack(pady=10)

# Start the Tkinter event loop
# run_it.mainloop()
