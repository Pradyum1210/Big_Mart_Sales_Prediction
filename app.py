import streamlit as st
import pandas as pd
import pickle

# === Load Model and Version Info from Pickle ===
with open("bigmart_best_model.pkl", "rb") as f:
    model , sklearn_version = pickle.load(f)

st.markdown("""
    <style>
    /* Dark opaque success box */
    div[data-baseweb="toast"] {
        background-color: #0A3D0A !important;   /* Solid dark green */
        color: #FFFFFF !important;              /* White text */
        border: 2px solid #145A32 !important;
        border-radius: 10px !important;
        padding: 16px !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        opacity: 1 !important;                 /* Full opacity */
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.4) !important;
    }
    </style>
""", unsafe_allow_html=True)




st.set_page_config(page_title="BigMart Sales Prediction", layout="centered")

# === Background Images for Each Item Type (move this UP before Item_Type selectbox) ===
item_backgrounds = {
    "Dairy": "https://www.shutterstock.com/image-photo/dairy-products-bottles-milk-cottage-260nw-2483159649.jpg",
    "Meat": "https://images.unsplash.com/photo-1600891964599-f61ba0e24092",
    "Fruits and Vegetables": "https://images.unsplash.com/photo-1542838132-92c53300491e",
    "Baking Goods": "https://www.shutterstock.com/image-photo/assortment-baked-goods-displayed-on-600nw-2575371219.jpg",
    "Snack Foods": "https://img.freepik.com/free-photo/top-view-fast-food-meal_23-2148273108.jpg?semt=ais_incoming&w=740&q=80",
    "Frozen Foods": "https://static.toiimg.com/photo/77315077.cms",
    "Breakfast": "https://c.ndtvimg.com/2020-01/i9tt6s48_breakfast_625x300_29_January_20.jpg",
    "Breads": "https://images.unsplash.com/photo-1608198093002-ad4e005484ec?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8YnJlYWR8ZW58MHx8MHx8fDA%3D",
    "Starchy Foods": "https://images.onlymyhealth.com/imported/images/2019/May/02_May_2019/Big__ap-foods-best.jpg",
    "Seafood": "https://media.istockphoto.com/id/520490716/photo/seafood-on-ice.jpg?s=612x612&w=0&k=20&c=snyxGY26viNQ6BWqW-ez4U7tAO65Z_tmAFPMobiZ9Q4=",
    "Soft Drinks": "https://images.unsplash.com/photo-1510626176961-4b57d4fbad03",
    "Hard Drinks": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRT7VJThOwauDlw9G1Ge0QcHPZZB3sOFjNuJw&s",
    "Household": "https://i0.wp.com/pediaa.com/wp-content/uploads/2022/05/Household.png?fit=640%2C470&ssl=1",
    "Health and Hygiene": "https://www.shutterstock.com/shutterstock/photos/1927423103/display_1500/stock-photo-hygiene-mind-map-health-concept-for-presentations-and-reports-1927423103.jpg",
    "Canned": "https://images.unsplash.com/photo-1674176508097-463b009c6004?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8Y2Fuc3xlbnwwfHwwfHx8MA%3D%3D&fm=jpg&q=60&w=3000",
    "Others": "https://images.unsplash.com/photo-1594051104380-8ab3d64ab36c"
}

# === Function to Set Background ===
def set_background(image_url=None, color=None):
    if image_url:
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("{image_url}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}
            .main-card {{
                background-color: rgba(255, 255, 255, 0.8);
                padding: 2rem;
                border-radius: 1rem;
                box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
                width: 80%;
                margin: auto;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    elif color:
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-color: {color};
            }}
            .main-card {{
                background-color: rgba(255, 255, 255, 0.9);
                padding: 2rem;
                border-radius: 1rem;
                box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
                width: 80%;
                margin: auto;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )


# === Title inside a styled box ===
st.markdown("""
    <div style="
        background-color: rgba(255, 255, 255, 0.85);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        color: #2E4053;
        margin-bottom: 25px;
    ">
        🛒 BigMart Sales Prediction App
    </div>
""", unsafe_allow_html=True)


# ✅ Item Type comes first
Item_Type = st.selectbox("Item Type", list(item_backgrounds.keys()))

# Change background immediately
if Item_Type in item_backgrounds:
    set_background(image_url=item_backgrounds[Item_Type])
else:
    set_background(color="#f8f9fa")

# === Remaining Inputs ===
Item_Identifier = st.text_input("Item Identifier", "FDA15")
Item_Weight = st.number_input("Item Weight", min_value=0.0, value=12.5)
Item_Fat_Content = st.selectbox("Item Fat Content", ["Low Fat", "Regular"])
Item_Visibility = st.slider("Item Visibility", min_value=0.0, max_value=0.3, step=0.01, value=0.1)
Item_MRP = st.number_input("Item MRP", min_value=0.0, value=150.0)
Outlet_Identifier = st.selectbox("Outlet Identifier", [
    "OUT027", "OUT013", "OUT049", "OUT035", "OUT046",
    "OUT017", "OUT045", "OUT018", "OUT019", "OUT010"
])
Outlet_Size = st.selectbox("Outlet Size", ["Small", "Medium", "High"])
Outlet_Location_Type = st.selectbox("Outlet Location Type", ["Tier 1", "Tier 2", "Tier 3"])
Outlet_Type = st.selectbox("Outlet Type", [
    "Supermarket Type1", "Supermarket Type2",
    "Supermarket Type3", "Grocery Store"
])
Outlet_Age = st.slider("Outlet Age (Years)", 0, 40, 15)

# === Predict Button ===
if st.button("Predict Sales"):
    input_df = pd.DataFrame([{
        "Item_Identifier": Item_Identifier,
        "Item_Weight": Item_Weight,
        "Item_Fat_Content": Item_Fat_Content,
        "Item_Visibility": Item_Visibility,
        "Item_Type": Item_Type,
        "Item_MRP": Item_MRP,
        "Outlet_Identifier": Outlet_Identifier,
        "Outlet_Size": Outlet_Size,
        "Outlet_Location_Type": Outlet_Location_Type,
        "Outlet_Type": Outlet_Type,
        "Outlet_Age": Outlet_Age
    }])
   
    prediction = model.predict(input_df)[0]
    st.success(f"📈 Predicted Item Outlet Sales: ₹{prediction:.2f}")

st.markdown('</div>', unsafe_allow_html=True)
