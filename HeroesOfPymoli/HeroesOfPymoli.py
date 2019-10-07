# Dependencies and Setup
import pandas as pd

# File to Load (Remember to Change These)
file_to_load = "Resources/purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(file_to_load)

#Show the file
purchase_data.head()

#View stats
purchase_data.describe()

purchase_data.columns

#Total number of game players

#Find the unique player identified by the Social Sec Number
unique_players = purchase_data['SN'].nunique()
players_count_df = pd.DataFrame({"Total Players": [unique_players]}, columns= ["Total Players"])
players_count_df

#Purchasing Analysis(TOTAL)
#--------------------------------------
# Unique items sold count
unique_items = purchase_data['Item ID'].nunique()

average_price = (purchase_data['Price'].sum()/purchase_data['Price'].count()).round(2)
#Total purchases
total_purchase_count = purchase_data['Price'].count()
#Purchase price
total_revenue = purchase_data["Price"].sum()
 

final_summary_df = pd.DataFrame({"Number of Unique Items": [unique_items], 
                              "Average Purchase Price": [average_price],
                             "Number of Purchases": [total_purchase_count],
                             "Total Revenue": [total_revenue]}, columns= ["Number of Unique Items", "Average Purchase Price",
                            "Number of Purchases", "Total Revenue"])

final_summary_df.style.format({"Average Purchase Price": "${:.2f}", "Total Revenue": "${:.2f}"})


#Demo counts of Genders
#Male, female and extra counts
demo_count = purchase_data["SN"].nunique()
male_total_count = purchase_data[purchase_data["Gender"] == "Male"]["SN"].nunique()
female_total_count = purchase_data[purchase_data["Gender"] == "Female"]["SN"].nunique()
other_count = demo_count - male_total_count - female_total_count

#Percentages calculations
percentage_of_male = ((male_total_count/demo_count)*100)
percentage_of_female = ((female_total_count/demo_count)*100)
percentage_of_other = ((other_count/demo_count)*100)


gender_df = pd.DataFrame({"Gender": ["Male", "Female", "Other / Non-Disclosed"], "Percentage of Players": [percentage_of_male, percentage_of_female, percentage_of_other],
                                        "Total Count": [male_total_count, female_total_count, other_count]}, columns = 
                                        ["Gender", "Percentage of Players", "Total Count"])
                                        
new_gender = gender_df.set_index("Gender")
new_gender.style.format({"Percentage of Players": "{:.2f}%"})


#PURCHASING ANALYSIS (GENDER)
#Gender purchase count
m_purchase = purchase_data[purchase_data["Gender"] == "Male"]["Price"].count()
f_purchase = purchase_data[purchase_data["Gender"] == "Female"]["Price"].count()
o_purchase = total_purchase_count - m_purchase - f_purchase

#Gender purchase average count
m_average_price = purchase_data[purchase_data["Gender"] == "Male"]['Price'].mean()
f_average_price = purchase_data[purchase_data["Gender"] == "Female"]['Price'].mean()
o_average_price = purchase_data[purchase_data["Gender"] == "Other / Non-Disclosed"]['Price'].mean()

#Total price per gender purchase
m_total_price = purchase_data[purchase_data["Gender"] == "Male"]['Price'].sum()
f_total_price = purchase_data[purchase_data["Gender"] == "Female"]['Price'].sum()
o_total_price = purchase_data[purchase_data["Gender"] == "Other / Non-Disclosed"]['Price'].sum()

#Calculate the normalized count per gender
m_normalized = m_total_price/male_total_count
f_normalized = f_total_price/female_total_count
o_normalized = o_total_price/other_count

#Gender Analysis summary 

gender_purchase_df = pd.DataFrame({"Gender": ["Male", "Female", "Other / Non-Disclosed"], "Purchase Count": [m_purchase, f_purchase, o_purchase],
                                        "Average Purchase Price": [m_average_price, f_average_price, o_average_price], "Total Purchase Value": [m_total_price, f_total_price, o_total_price],
                                "Normalized Totals": [m_normalized, f_normalized, o_normalized]}, columns = 
                                        ["Gender", "Purchase Count", "Average Purchase Price", "Total Purchase Value", "Normalized Totals"])
                                        
new_gender_purchase = gender_purchase_df.set_index("Gender")
new_gender_purchase.style.format({"Average Purchase Price": "${:.2f}", "Total Purchase Value": "${:.2f}", "Normalized Totals": "${:.2f}"})


#AGE DEMOGRAPHICS
# Establish the bins for 4 years(age) length 
age_bins = [0, 9.90, 14.90, 19.90, 24.90, 29.90, 34.90, 39.90, 99999]
group_names = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]

# Categorize the existing players using the age bins
purchase_data["Age Ranges"] = pd.cut(purchase_data["Age"], age_bins, labels=group_names)

# Calculate the Numbers and Percentages by Age Group
total_age_demo = purchase_data["Age Ranges"].value_counts()

#Summarized data frame
age_percentage = total_age_demo / unique_players * 100
age_demo = pd.DataFrame({"Total Count": total_age_demo, "Percentage of Players": age_percentage})

# Round(2) to format the percentage column to 2 decimal points
age_demo = age_demo.round(2)

# Display Age Demographics Table
age_demo.sort_index()


#PURCHASING ANALYIS(Age)
# Bin the Purchasing Data
purchase_data["Age Ranges"] = pd.cut(purchase_data["Age"], age_bins, labels=group_names)

# Run basic calculations
total_age_purchase = purchase_data.groupby(["Age Ranges"]).sum()["Price"].rename("Total Purchase Value")
age_average = purchase_data.groupby(["Age Ranges"]).mean()["Price"].rename("Average Purchase Price")
total_age_demo = purchase_data.groupby(["Age Ranges"]).count()["Price"].rename("Purchase Count")

# Calculate the purchase per person
normalized_totals = total_age_purchase / age_demo["Total Count"]

# Convert to DataFrame
age_data = pd.DataFrame({"Purchase Count": total_age_demo, "Average Purchase Price": age_average, "Total Purchase Value": total_age_purchase, "Avg Total Purchase per Person": normalized_totals})

# Minor Data Munging
age_data["Average Purchase Price"] = age_data["Average Purchase Price"].map("${:,.2f}".format)
age_data["Total Purchase Value"] = age_data["Total Purchase Value"].map("${:,.2f}".format)
age_data ["Purchase Count"] = age_data["Purchase Count"].map("{:,}".format)
age_data["Avg Total Purchase per Person"] = age_data["Avg Total Purchase per Person"].map("${:,.2f}".format)
age_data = age_data.loc[:, ["Purchase Count", "Average Purchase Price", "Total Purchase Value", "Avg Total Purchase per Person"]]

# Display the Age Table
age_data


#TOP SPEMDERS
grouped_sn = purchase_data.groupby(["SN"])

#Find total spent per user
total_price_sn = grouped_sn.sum()["Price"]

#Find avg spent per user
avg_price_sn = grouped_sn.mean()["Price"]

#Find purchase count per user
count_sn = grouped_sn.count()["Price"]

#Create new dataframe
top_user_df = pd.DataFrame({"Purchase Count":count_sn,
                            "Average Purchase Price":avg_price_sn,
                            "Total Purchase Price": total_price_sn
                            })

#Sort by total purchase price
sorted_df = top_user_df.sort_values("Total Purchase Price",ascending=False)

#Format numbers
sorted_df["Average Purchase Price"] = sorted_df["Average Purchase Price"].map("${:,.2f}".format) 
sorted_df["Total Purchase Price"] = sorted_df["Total Purchase Price"].map("${:,.2f}".format) 

#Reorder Columns
sorted_df = sorted_df[["Purchase Count", "Average Purchase Price", "Total Purchase Price"]]

#Display top 5
sorted_df.head(5)


#MOST POPULAR Items
grouped_id = purchase_data.set_index(["Item ID", "Item Name"])

grouped_id = grouped_id.groupby(level=["Item ID", "Item Name"])

#Find total spent per user
total_price_id = grouped_id.sum()["Price"]

#Find avg spent per user
avg_price_id = grouped_id.mean()["Price"]

#Find purchase count per user
count_id = grouped_id.count()["Price"]


#Create new dataframe
items_df = pd.DataFrame({ 
                         "Count":count_id,
                            "Average Purchase Price":avg_price_id,
                            "Total Purchase Price": total_price_id,
                            })


#Sort by total purchase price
sorted_items = items_df.sort_values("Count",ascending=False)

sorted_items["Average Purchase Price"] = sorted_items["Average Purchase Price"].map("${:,.2f}".format) 
sorted_items["Total Purchase Price"] = sorted_items["Total Purchase Price"].map("${:,.2f}".format) 

#Reorder Columns
sorted_items = sorted_items[["Count", "Average Purchase Price", "Total Purchase Price"]]


#Display top 5
sorted_items.head(5)


#MOST PROFITABLE Items
grouped_id = purchase_data.set_index(["Item ID", "Item Name"])

grouped_id = grouped_id.groupby(level=["Item ID", "Item Name"])

#Find total spent per user
total_price_id = grouped_id.sum()["Price"]

#Find avg spent per user
avg_price_id = grouped_id.mean()["Price"]

#Find purchase count per user
count_id = grouped_id.count()["Price"]

#Create new dataframe
items_df = pd.DataFrame({ "Count":count_id,
                        "Average Purchase Price":avg_price_id,
                        "Total Purchase Price": total_price_id,
                            })


#Sort by total purchase price
sorted_items = items_df.sort_values("Total Purchase Price",ascending=False)

sorted_items["Average Purchase Price"] = sorted_items["Average Purchase Price"].map("${:,.2f}".format) 
sorted_items["Total Purchase Price"] = sorted_items["Total Purchase Price"].map("${:,.2f}".format) 

#Reorder Columns
sorted_items = sorted_items[["Count", "Average Purchase Price", "Total Purchase Price"]]

#Display top 5
sorted_items.head(5)