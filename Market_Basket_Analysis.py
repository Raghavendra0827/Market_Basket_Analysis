import streamlit as st
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

# Load initial data
data = pd.read_csv("data.csv")
# Load item images
item_images = {
    'Onion': 'https://m.media-amazon.com/images/I/71GUFttn0jL._AC_UF1000,1000_QL80_.jpg',
    'Potato': 'https://m.media-amazon.com/images/I/61yXL70-RaL._AC_UF1000,1000_QL80_.jpg',
    'Burger': 'https://img.freepik.com/free-photo/front-view-tasty-meat-burger-with-cheese-salad-dark-background_140725-89597.jpg',
    'Milk': 'https://www.heritagefoods.in/blog/wp-content/uploads/2020/12/shutterstock_539045662.jpg',
    'Beer': 'https://cdn.pixabay.com/photo/2017/06/24/23/41/beer-2439237_640.jpg',
    'Eggs': 'https://img.freepik.com/free-photo/brown-eggs_2829-13455.jpg',
    'Bread': 'https://thumbs.dreamstime.com/b/bread-cut-14027607.jpg',
    'Cheese': 'https://t3.ftcdn.net/jpg/05/66/02/98/360_F_566029808_X7praimuCQt0MsLCmw5d65Pp5KqmTS8e.jpg',
    'Tomato': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Tomato_je.jpg/1231px-Tomato_je.jpg',
    'Chicken': 'https://assets.epicurious.com/photos/62f16ed5fe4be95d5a460eed/1:1/w_4318,h_4318,c_limit/RoastChicken_RECIPE_080420_37993.jpg',
    'Rice': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRbfzh6ANLy74mq6aBFMC0P9BWFsiMH8Di0HuZouSSj5Q&s',
    'Cereal': 'https://t4.ftcdn.net/jpg/00/60/08/87/360_F_60088763_3CVRHjk4Mn75y6kraCsSqNKEZkuf9032.jpg',
    'Yogurt': 'https://www.shutterstock.com/image-photo/sour-cream-yogurt-wooden-bowl-260nw-1333497695.jpg',
    'Apples': 'https://www.shutterstock.com/image-photo/red-apple-isolated-on-white-600nw-1727544364.jpg'
}

# Function to append new customer basket items to original data
def append_customer_basket(items):
    global data
    last_id = data['ID'].max()
    if pd.isna(last_id):  # If there's no previous data
        last_id = 0
    new_row = {item: 0 for item in data.columns[1:]}  # Initialize with 0s
    new_row['ID'] = last_id + 1
    for item in items:
        if item in new_row:  # Check if item exists in data columns
            new_row[item] = 1
    data = data.append(new_row, ignore_index=True)
    data.to_csv("data.csv", index=False)

# Function to find items with highest lift or confidence
def items_with_metric(rules, metric, n=10):
    sorted_rules = rules.sort_values(by=metric, ascending=False)
    return sorted_rules.head(n)

# Sidebar option for company view
st.sidebar.write('<h2 style="color: #ff6666;">Company View</h2>', unsafe_allow_html=True)
st.sidebar.markdown('Enter new customer basket items:')
new_onion = st.sidebar.checkbox('Onion')
new_potato = st.sidebar.checkbox('Potato')
new_burger = st.sidebar.checkbox('Burger')
new_milk = st.sidebar.checkbox('Milk')
new_beer = st.sidebar.checkbox('Beer')
new_eggs = st.sidebar.checkbox('Eggs')
new_bread = st.sidebar.checkbox('Bread')
new_cheese = st.sidebar.checkbox('Cheese')
new_tomato = st.sidebar.checkbox('Tomato')
new_chicken = st.sidebar.checkbox('Chicken')
new_rice = st.sidebar.checkbox('Rice')
new_cereal = st.sidebar.checkbox('Cereal')
new_yogurt = st.sidebar.checkbox('Yogurt')
new_apples = st.sidebar.checkbox('Apples')

if st.sidebar.button('Add Items'):
    new_items = [item for item, new in zip(data.columns[1:], [new_onion, new_potato, new_burger, new_milk, new_beer, new_eggs, new_bread, new_cheese, new_tomato, new_chicken, new_rice, new_cereal, new_yogurt, new_apples]) if new]
    append_customer_basket(new_items)
    st.sidebar.success('New customer basket items added successfully!')

# Perform market basket analysis
frequent_itemsets = apriori(data.drop(columns=['ID']), min_support=0.2, use_colnames=True)
rules = association_rules(frequent_itemsets, metric='lift', min_threshold=1)

# Radio button to select metric
selected_metric = st.sidebar.radio("Select Metric:", ('lift', 'confidence'))
# Display items with highest lift in customer view
st.markdown('<h1 style="color: #66ccff;">Exclusive Offers</h1>' if selected_metric == 'lift' else '<h1 style="color: #66ccff;">Your Fav Combo Awaits! Grab Exciting Offers Now!</h1>', unsafe_allow_html=True)
items_displayed = set()  # To avoid duplicate pairs

item2 = ""
for index, row in items_with_metric(rules, selected_metric).iterrows():
    if list(row['antecedents'])[0] != item2:
        item1 = list(row['antecedents'])[0]
        item2 = list(row['consequents'])[0]
        # Check if the pair is already displayed or its reverse is displayed
        if (item1, item2) not in items_displayed and (item2, item1) not in items_displayed:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.image(item_images[item1], caption=item1, width=150)
            with col2:
                st.markdown('<h1 style="color: #66ccff;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+</h1>', unsafe_allow_html=True)
            with col3:
                st.image(item_images[item2], caption=item2, width=150)


        if selected_metric == 'lift':
            if row['lift'] > 1.2:
                if st.button(f"Weekly Offer: 20% off on purchase of {item1} and {item2}", key=f"{item1}_{item2}", help='Weekly Offer'):
                    pass
                st.markdown('<style>div.stButton > button{background-color: #00FF00; color: black;}</style>', unsafe_allow_html=True)

            elif row['lift'] > 1:
                if st.button(f"Daily Offer: 15% off on purchase of {item1} and {item2}", key=f"{item1}_{item2}", help='Daily Offer'):
                    pass
                st.markdown('<style>div.stButton > button{background-color: #00FF00; color: black;}</style>', unsafe_allow_html=True)

            else:
                if st.button(f"Festival Offer: Buy {item1} get {item2} free", key=f"{item1}_{item2}", help='Festival Offer'):
                    pass
                st.markdown('<style>div.stButton > button{background-color: #00FF00; color: black;}</style>', unsafe_allow_html=True)

        else:  # Confidence
            if row['confidence'] > 0.7:
                if st.button(f"High Confidence Offer: 25% off on purchase of {item1} and {item2}", key=f"{item1}_{item2}", help='High Confidence Offer'):
                    pass
                st.markdown('<style>div.stButton > button{background-color: #00FF00; color: black;}</style>', unsafe_allow_html=True)

            elif row['confidence'] > 0.5:
                if st.button(f"Medium Confidence Offer: 15% off on purchase of {item1} and {item2}", key=f"{item1}_{item2}", help='Medium Confidence Offer'):
                    pass
                st.markdown('<style>div.stButton > button{background-color: #00FF00; color: black;}</style>', unsafe_allow_html=True)

            else:
                if st.button(f"Low Confidence Offer: Buy {item1} get {item2} free", key=f"{item1}_{item2}", help='Low Confidence Offer'):
                    pass
                st.markdown('<style>div.stButton > button{background-color: #00FF00; color: black;}</style>', unsafe_allow_html=True)


    # items_displayed.add((item1, item2))  # Add the pair to displayed items
    

company_password = "MYCOMPANY@123"

# Sidebar option for viewing association rules separately
view_rules = st.sidebar.checkbox('View Association Rules (Protected)')

if view_rules:
    # Create an empty slot for password input
    password_input = st.sidebar.text_input("Enter Company Password", type="password")

    # Display association rules and download option if password is correct
    if st.sidebar.button("Submit") and password_input == company_password:
        st.sidebar.markdown('<h1 style="color: #66ccff;">Association Rules</h1>', unsafe_allow_html=True)
        # st.table(rules)
        st.sidebar.markdown('<a href="data:text/csv;charset=utf-8,%EF%BB%BF' + rules.to_csv(index=False).encode('utf-8').decode().replace('\n', '%0A') + '" download="association_rules.csv" target="_blank">Download Association Rules</a>', unsafe_allow_html=True)
    elif password_input != "":
        st.sidebar.error("Incorrect password. Please try again.")

