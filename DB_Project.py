#!/usr/bin/env python
# coding: utf-8




import mysql.connector
import tkinter as tk
from tkinter import *
import re


# In[1017]:


#mydb = mysql.connector.connect(host = 'sql7.freemysqlhosting.net', user = 'sql7611863', password = 'J9Bun7GiVd', database = 'sql7611863')
mydb = mysql.connector.connect(host = 'db4free.net', user = 'mohamedakhalil', password = 'admin123', database = 'usedcars_db')


# In[8]:





# In[1088]:



def ReturnHome():
    for widgets in root.winfo_children():
        widgets.destroy()
    Label(root, text = "Home Page", pady = 20, padx = 20, font=('Calibra', 24)).grid(row=0, column = 1)

    make.set("")
    body.set("")
    year.set("")
    loc.set("")
    
    button = tk.Button(root, text='Register New User', width=25, command = view_register)
    button.grid(row=1, column = 0)
    button = tk.Button(root, text='Add a Sale', width=25, command = view_sale)
    button.grid(row=1, column = 1)
    button = tk.Button(root, text='View Reviews of an Ad', width=25, command = view_ad_rev)
    button.grid(row=1, column = 2)
    button = tk.Button(root, text='View Rating of an Owner', width=25, command = view_owner_rate)
    button.grid(row=2, column = 0)
    button = tk.Button(root, text='Show Ad of a Specific Car', width=25, command = view_show_car)
    button.grid(row=2, column = 1)
    button = tk.Button(root, text='Show Cars from Location and Price', width=25, command = view_car_loc)
    button.grid(row=2, column = 2)
    button = tk.Button(root, text='Show Top Locations', width=25, command = view_top_location)
    button.grid(row=3, column = 0)
    button = tk.Button(root, text='Show Top Sellers', width=25, command = view_top_seller)
    button.grid(row=3, column = 1)
    button = tk.Button(root, text='Show All listings by a Seller', width=25, command = view_listing)
    button.grid(row=3, column = 2)
    button = tk.Button(root, text='Show Top Car inventories', width=25, command = view_top_car)
    button.grid(row=4, column = 1)




def view_ad_rev():
    for widgets in root.winfo_children():
        widgets.destroy()
    entry_lab = Label(root, text="Enter the ad link you want to check", padx = 10).grid(row = 0,column=0)
    link = Entry(root)
    link.grid(row = 0, column =1)

    button = tk.Button(root, text='View Reviews', width=25, command = lambda:view_rev(link.get()))
    button.grid(row=1,column=0, columnspan=2)
    Button(root, text = "Return Home", command = ReturnHome).grid(row=6, column =0, columnspan = 2)


def view_owner_rate():
    for widgets in root.winfo_children():
        widgets.destroy()
    name_lab = Label(root, text="Enter the seller you want to check", padx = 10).grid(row = 3,column=0)
    Name = Entry(root)
    Name.grid(row = 3, column = 1)

    button = tk.Button(root, text='View Rating', width=25, command = lambda:view_rate(Name.get()))
    button.grid(row=4,column=0, columnspan=2)
    Button(root, text = "Return Home", command = ReturnHome).grid(row=6, column =0, columnspan = 2)


# In[ ]:





# ## Third requirement "View existing reviews of a given ad"
# But we need to make it dynamic for the user

# In[1067]:


def view_rev(link):
    mycursor = mydb.cursor()
    value = link
    sql = """
    select Review from car where Ad_link = '{}'
    """.format(value)
    mycursor.execute(sql)
    result = mycursor.fetchall()
    query=""
    for r in result:
        query+= str(r) + "\n"
    f = Frame(root)
    f.grid(row=2, column=  0)

    xscrollbar = Scrollbar(f, orient=HORIZONTAL)
    xscrollbar.grid(row=1, column=0, sticky=N+S+E+W)

    yscrollbar = Scrollbar(f)
    yscrollbar.grid(row=0, column=1, sticky=N+S+E+W)

    text = Text(f, wrap=NONE,
                xscrollcommand=xscrollbar.set,
                yscrollcommand=yscrollbar.set, width = 50, height = 5)
    text.grid(row=0, column=0)

    xscrollbar.config(command=text.xview)
    yscrollbar.config(command=text.yview)
    text.insert(END, query)
    Button(root, text = "Return Home", command = ReturnHome).grid(row=6, column =0, columnspan = 2)


# ## Forth requirement "View aggregated rating of a seller / owner"

# In[1068]:


def view_rate(Name):
    mycursor = mydb.cursor()
    name = Name
    sql = """
    select avg(rating), Owner_name from car innner join car_owner on Seller_Profile = Owner_Profile where Owner_name="{}" AND rating != ' ' group by 2
    """.format(name)
    mycursor.execute(sql)
    result = mycursor.fetchall()
    query=""
    for r in result:
        query+= str(r) + "\n"
    f = Frame(root)
    f.grid(row=5, column=  0)

    xscrollbar = Scrollbar(f, orient=HORIZONTAL)
    xscrollbar.grid(row=1, column=0, sticky=N+S+E+W)

    text = Text(f, wrap=NONE,
                xscrollcommand=xscrollbar.set,
                width = 25, height = 2)
    text.grid(row=0, column=0)

    xscrollbar.config(command=text.xview)
    text.insert(END, query)
    Button(root, text = "Return Home", command = ReturnHome).grid(row=6, column =0, columnspan = 2)


# ## Fifth requirement "Show all the ads for a given car make, body type and year in a specific location / area, along with the average price the number of listings for each model"
# But we need to make it dynamic for the user and make price int

# In[1069]:


def chooseBrand():
    #Getting all body types
    mycursor = mydb.cursor()
    global brand
    brand=make.get()
    brand = re.search("'(.*)'", brand).group(1)
    sql = """
    select distinct(body_type) from car where brand = '{}'
    """.format(brand)
    mycursor.execute(sql)
    body_res = mycursor.fetchall()
    bodies = OptionMenu(root, body, *body_res)
    bodies.grid(row = 0, column = 1)
    button = tk.Button(root, text='Choose Body Type', width=25, command = chooseYear)
    button.grid(row = 1, column = 1)

    
    
def chooseYear():
    #Getting all Years
    mycursor = mydb.cursor()
    global body_type
    body_type=body.get()
    body_type = re.search("'(.*)'", body_type).group(1)
    sql = """
    select distinct(year_prod) from car where body_type = '{}' AND brand = '{}'
    """.format(body_type, brand)
    mycursor.execute(sql)
    year_res = mycursor.fetchall()
    year_res = sorted(year_res, key=lambda tup: tup[0])
    years = OptionMenu(root, year, *year_res)
    years.grid(row = 0, column = 2)
    button = tk.Button(root, text='Choose Year', width=25, command = chooseLocation)
    button.grid(row = 1, column = 2)

    
def chooseLocation():
    #Getting all Locations
    mycursor = mydb.cursor()
    global year_prod
    year_prod=year.get()
    year_prod = year_prod[1:5]
    sql = """
    select distinct(Location) from car where year_prod = '{}' AND brand = '{}' AND body_type = '{}'
    """.format(year_prod, brand, body_type)
    mycursor.execute(sql)
    loc_res = mycursor.fetchall()
    loc_res = sorted(loc_res, key=lambda tup: tup[0])
    Locations = OptionMenu(root, loc, *loc_res)
    Locations.grid(row = 0, column = 3)
    button = tk.Button(root, text='Choose Location', width=25, command = showResult)
    button.grid(row = 1, column = 3)

def clear():
    for widgets in root.winfo_children():
        widgets.destroy()
        #getting all the brands
    mycursor = mydb.cursor()
    sql = """
    select distinct(Brand) from car
    """
    mycursor.execute(sql)
    result = mycursor.fetchall()
    result = sorted(result, key=lambda tup: tup[0])
    make.set("")
    body.set("")
    year.set("")
    loc.set("")
    brands = OptionMenu(root, make, *result)
    brands.grid(row = 0, column = 0)
    button = tk.Button(root, text='Choose Make', width=25, command = chooseBrand)
    button.grid(row=1, column = 0)
    
    
def showResult():
    mycursor = mydb.cursor()
    sql = """
    select model, avg(price), count(*) from car where brand = '{}' AND year_prod = "{}" AND body_type = '{}' AND location = '{}'
    group by 1
    """.format(brand, year_prod,body_type,re.search("'(.*)'", loc.get()).group(1))
    mycursor.execute(sql)
    result = mycursor.fetchall()
    query = ""
    for r in result:
        query += str(r) + '\n'
        

    Label(root, text = query).grid(row =2,column = 0)
    f = Frame(root)
    f.grid(row=2, column=  0)

    xscrollbar = Scrollbar(f, orient=HORIZONTAL)
    xscrollbar.grid(row=1, column=0, sticky=N+S+E+W)

    yscrollbar = Scrollbar(f)
    yscrollbar.grid(row=0, column=1, sticky=N+S+E+W)

    text = Text(f, wrap=NONE,
                xscrollcommand=xscrollbar.set,
                yscrollcommand=yscrollbar.set, width = 40, height = 6)
    text.grid(row=0, column=0)

    xscrollbar.config(command=text.xview)
    yscrollbar.config(command=text.yview)
    text.insert(END, query)
    
    button = tk.Button(root, text='Search Another Car', width=25, command = clear)
    button.grid(row = 3, column = 0)
    Button(root, text = "Return Home", command = ReturnHome).grid(row=6, column =0, columnspan = 2)


# In[1070]:


def view_show_car():
    #getting all the brands
    for widgets in root.winfo_children():
        widgets.destroy()
    mycursor = mydb.cursor()
    sql = """
    select distinct(Brand) from car
    """
    mycursor.execute(sql)
    result = mycursor.fetchall()


    result = sorted(result, key=lambda tup: tup[0])

    brands = OptionMenu(root, make, *result)
    #print(make.get())
    brands.grid(row = 0, column = 0)
    button = tk.Button(root, text='Choose Make', width=25, command = chooseBrand)
    button.grid(row=1, column = 0)
    Button(root, text = "Return Home", command = ReturnHome).grid(row=6, column =0, columnspan = 2)


# ## Trying the sixth requirement
# 

# In[1071]:

def chooseRange():
    #Getting all Price Ranges
    mycursor = mydb.cursor()
    global location
    location=loc.get()
    location = re.search("'(.*)'", location).group(1)
    sql = """
    select min(price), max(price) from car where location = '{}'
    """.format(location)
    mycursor.execute(sql)
    prices = mycursor.fetchall()


    lower = Scale(root, from_=prices[0][0], to = prices[0][1], orient = HORIZONTAL)
    lower.grid(row =0, column = 1)
    upper = Scale(root, from_=prices[0][0], to = prices[0][1], orient = HORIZONTAL)
    upper.grid(row =0, column = 2)
    
    
    button = tk.Button(root, text='Choose Price Range', width=25, command = lambda:choosePrice(lower.get(),upper.get()))
    button.grid(row = 1, column = 1, columnspan = 2)


def chooseFeatures():
    i=0
    features_i_want=[]
    for f in feature_res:
        if(var_list[i].get()):
            features_i_want.append(f[0][:-1])
        i+=1
    sqlQuery = """   
            select c.ad_link, c.brand, c.model from car c inner join car_features f on f.ad_link = c.ad_link 
            where price between {} AND {} AND location = '{}' AND
            """.format(upper_price, lower_price, location)
    for i in range(len(features_i_want)):
        if (i==len(features_i_want)-1):
            sqlQuery+= f"feature like '{features_i_want[i]}%' "
        else:
            sqlQuery+= f"feature like '{features_i_want[i]}%' OR "
    sqlQuery = sqlQuery.replace('\n',' ')
    sqlQuery+= "group by 1,2,3"
    mycursor = mydb.cursor()
    mycursor.execute(sqlQuery)
    result = mycursor.fetchall()
    query=""
    for r in result:
        query+=str(r)+'\n'
    frame = Frame(root).grid(row = 2, column =0)
    f = Frame(root)
    f.grid(row=2, column=  0)

    xscrollbar = Scrollbar(f, orient=HORIZONTAL)
    xscrollbar.grid(row=1, column=0, sticky=N+S+E+W)

    yscrollbar = Scrollbar(f)
    yscrollbar.grid(row=0, column=1, sticky=N+S+E+W)

    text = Text(f, wrap=NONE,
                xscrollcommand=xscrollbar.set,
                yscrollcommand=yscrollbar.set, width = 50, height = 20)
    text.grid(row=0, column=0)

    xscrollbar.config(command=text.xview)
    yscrollbar.config(command=text.yview)
    text.insert(END, query)
    
def choosePrice(upper, lower):
    #Getting all featues
    mycursor = mydb.cursor()
    global upper_price
    global lower_price
    upper_price=upper
    lower_price = lower
    sql = """
    select distinct(feature) from car_features f inner join car c on f.ad_link = c.ad_link
    where price between {} AND {} AND location = '{}'
    """.format(upper_price,lower_price, location)
    mycursor.execute(sql)
    global feature_res
    feature_res = mycursor.fetchall()
    feature_res = sorted(feature_res, key=lambda tup: tup[0])
    
    frame = Frame(root)
    frame.grid(column=1, row=2, columnspan = 5)

    global var_list
    var_list = []
    r=0
    c = 0
    for index, feat in enumerate(feature_res):
        var_list.append(IntVar(value=0))
        Checkbutton(frame, variable=var_list[index],
                    text=feat[0], padx = 5).grid(sticky= "W",row=r, column=c)
        c+=1
        if(c==3):
            r+=1
            c=0

    
    button = tk.Button(root, text='Choose Features', width=25, command = chooseFeatures)
    button.grid(row = r+1, column = 1)
    


# In[1072]:


def view_car_loc():

    for widgets in root.winfo_children():
        widgets.destroy()
    #getting all the brands
    mycursor = mydb.cursor()
    sql = """
    select distinct(Location) from car
    """
    mycursor.execute(sql)
    result = mycursor.fetchall()

    result = sorted(result, key=lambda tup: tup[0])

    locations = OptionMenu(root, loc, *result)
    locations.grid(row = 0, column = 0)
    button = tk.Button(root, text='Choose Location', width=25, command = chooseRange)
    button.grid(row=1, column = 0)
    Button(root, text = "Return Home", command = ReturnHome).grid(row=10, column =0, columnspan = 2)


# ## This is requirement 7

# In[1091]:


def showTopLocation():
    #Getting top locations
    brand=make.get()
    brand = re.search("'(.*)'", brand).group(1)
    mycursor = mydb.cursor()
    sql = """
    select location, brand, count(*), avg(price) from car where brand = '{}'
    group by 1,2
    order by 3 desc
    limit 5
    """.format(brand)
    
    mycursor.execute(sql)
    result = mycursor.fetchall()
    query=""
    for r in result:
        query+=str(r)+'\n'
    f = Frame(root)
    f.grid(row=2, column=  0)

    xscrollbar = Scrollbar(f, orient=HORIZONTAL)
    xscrollbar.grid(row=1, column=0, sticky=N+S+E+W)

    yscrollbar = Scrollbar(f)
    yscrollbar.grid(row=0, column=1, sticky=N+S+E+W)

    text = Text(f, wrap=NONE,
            xscrollcommand=xscrollbar.set,
            yscrollcommand=yscrollbar.set, width = 50, height = 6)
    text.grid(row=0, column=0)

    xscrollbar.config(command=text.xview)
    yscrollbar.config(command=text.yview)
    text.insert(END, query)
    Button(root, text='Search Another Brand', width=25, command = view_top_location).grid(row = 3,column=0)


# In[1090]:


def view_top_location():
    for widgets in root.winfo_children():
        widgets.destroy()
    mycursor = mydb.cursor()
    sql = """
    select distinct(Brand) from car
    """
    mycursor.execute(sql)
    result = mycursor.fetchall()
    result = sorted(result, key=lambda tup: tup[0])
    brands = OptionMenu(root, make, *result)
    brands.grid(row = 0, column = 0)
    button = tk.Button(root, text='Show Top Locations', width=25, command = showTopLocation)
    button.grid(row=1, column = 0)
    Button(root, text = "Return Home", command = ReturnHome).grid(row=6, column =0, columnspan = 2)


# ## This is requirement 8

# In[1076]:


def view_top_seller():
    for widgets in root.winfo_children():
        widgets.destroy()
    #Getting top locations
    mycursor = mydb.cursor()
    sql = """
    select Owner_profile, owner_name, year_prod, count(*), avg(price) from car inner join car_owner on seller_profile = owner_profile
    group by 1,2,3
    order by 4 desc
    limit 5
    """
    mycursor.execute(sql)
    result = mycursor.fetchall()
    query=""
    for r in result:
        query+=str(r)+'\n'
    f = Frame(root)
    f.grid(row=2, column=  0)

    xscrollbar = Scrollbar(f, orient=HORIZONTAL)
    xscrollbar.grid(row=1, column=0, sticky=N+S+E+W)

    yscrollbar = Scrollbar(f)
    yscrollbar.grid(row=0, column=1, sticky=N+S+E+W)

    text = Text(f, wrap=NONE,
            xscrollcommand=xscrollbar.set,
            yscrollcommand=yscrollbar.set, width = 50, height = 6)
    text.grid(row=0, column=0)

    xscrollbar.config(command=text.xview)
    yscrollbar.config(command=text.yview)
    text.insert(END, query)
    Button(root, text = "Return Home", command = ReturnHome).grid(row=6, column =0, columnspan = 2)


# ## This is requirement 9

# In[1077]:


def showListing(Name,Num):
    mycursor = mydb.cursor()
    sql = """
        select brand, model,price from car inner join car_owner on seller_profile = owner_profile
        where owner_name = '{}' or Phone_number ='{}' 
        """.format(Name, Num)

    mycursor.execute(sql)
    result = mycursor.fetchall()
    query=""
    for r in result:
        query+=str(r)+'\n'
    f = Frame(root)
    f.grid(row=3, column=  0)

    xscrollbar = Scrollbar(f, orient=HORIZONTAL)
    xscrollbar.grid(row=1, column=0, sticky=N+S+E+W)

    yscrollbar = Scrollbar(f)
    yscrollbar.grid(row=0, column=1, sticky=N+S+E+W)

    text = Text(f, wrap=NONE,
            xscrollcommand=xscrollbar.set,
            yscrollcommand=yscrollbar.set, width = 50, height = 10)
    text.grid(row=0, column=0)

    xscrollbar.config(command=text.xview)
    yscrollbar.config(command=text.yview)
    text.insert(END, query)    
    Button(root, text = "Return Home", command = ReturnHome).grid(row=6, column =0, columnspan = 2)


# In[1097]:


def view_listing():
    for widgets in root.winfo_children():
        widgets.destroy()
    
    name_lab = Label(root, text="Enter the Owner Name you want to check", padx = 10).grid(row = 0,column=0)
    number_lab = Label(root, text="Enter the Owner Number you want to check", padx = 10).grid(row = 1,column=0)

    Name = Entry(root)
    Name.grid(row = 0, column = 1)

    Num = Entry(root)
    Num.grid(row = 1, column = 1)


    button = tk.Button(root, text='Show Listings by this Seller', width=25, command = lambda:showListing(Name.get(),Num.get()))
    button.grid(row=2, column = 0, columnspan=2)
    Button(root, text = "Return Home", command = ReturnHome).grid(row=6, column =0, columnspan = 2)


# ## This is requirement 10

# In[1079]:


def showTopCar(low,up):
    mycursor = mydb.cursor()

    sql = """
        select brand, model, count(*), avg(price) from car where year_prod between {} AND {}
        group by 1,2
        order by 3 desc
        limit 5
        """.format(low,up)

    mycursor.execute(sql)
    result = mycursor.fetchall()
    query = ""
    for r in result:
        query+=str(r)+'\n'
    f = Frame(root)
    f.grid(row=3, column=  0)

    xscrollbar = Scrollbar(f, orient=HORIZONTAL)
    xscrollbar.grid(row=1, column=0, sticky=N+S+E+W)

    yscrollbar = Scrollbar(f)
    yscrollbar.grid(row=0, column=1, sticky=N+S+E+W)

    text = Text(f, wrap=NONE,
            xscrollcommand=xscrollbar.set,
            yscrollcommand=yscrollbar.set, width = 50, height = 10)
    text.grid(row=0, column=0)

    xscrollbar.config(command=text.xview)
    yscrollbar.config(command=text.yview)
    text.insert(END, query)
    


# In[1095]:


def view_top_car():
    for widgets in root.winfo_children():
        widgets.destroy()
    lower = Scale(root, from_=2000, to = 2023, orient = HORIZONTAL)
    lower.grid(row =0, column = 0)
    upper = Scale(root, from_=2000, to = 2023, orient = HORIZONTAL)
    upper.grid(row =0, column = 1)


    button = tk.Button(root, text='Choose Year Range', width=25, command = lambda:showTopCar(lower.get(),upper.get()))
    button.grid(row = 1, column = 0, columnspan = 2)
    Button(root, text = "Return Home", command = ReturnHome).grid(row=6, column =0, columnspan = 2)


# ## Creating the top level

# In[1169]:



# In[1154]:



# In[1082]:


def register():
    user = username.get()
    em = email.get()
    gen = Gender.get()
    ag = Age.get()
    mycursor = mydb.cursor()

    sql = """
        insert into buyer VALUES ('{}','{}','{}',{})
        """.format(user,em,gen,ag)

    mycursor.execute(sql)
    mydb.commit()
    username.delete(0,END)
    email.delete(0,END)
    Gender.delete(0,END)
    Age.delete(0,END)
    Label(root, text="You have been registered").grid(row = 5, column = 0, columnspan = 2)


# In[1060]:


def view_register():
    for widgets in root.winfo_children():
        widgets.destroy()
    username_label = Label(root, text="Enter your username", padx = 10).grid(row = 0,column=0)
    global username
    username = Entry(root)
    username.grid(row = 0, column =1)
    email_label = Label(root, text="Enter your Email", padx = 10).grid(row = 1,column=0)
    global email
    email = Entry(root)
    email.grid(row = 1, column =1)
    Gender_label = Label(root, text="Enter your Gender", padx = 10).grid(row = 2,column=0)
    global Gender
    Gender = Entry(root)
    Gender.grid(row = 2, column =1)
    Age_label = Label(root, text="Enter your Age", padx = 10).grid(row = 3,column=0)
    global Age
    Age = Entry(root)
    Age.grid(row = 3,column =1)
    Button(root, text = "Register", command = register).grid(row=4, column =0, columnspan = 2)
    Button(root, text = "Return Home", command = ReturnHome).grid(row=6, column =0, columnspan = 2)


# In[1153]:


def chooseBuyer():
    car_label = Label(root, text="Enter Sold Car ad", padx = 10).grid(row = 0,column=1)
    global car
    car = Entry(root)
    car.grid(row = 0, column =2)
    rev_label = Label(root, text="Enter your review", padx = 10).grid(row = 1,column=1)
    global review
    review = Entry(root)
    review.grid(row = 1, column =2)
    rate_label = Label(root, text="Enter your Rating", padx = 10).grid(row = 2,column=1)
    global Rating
    Rating = Entry(root)
    Rating.grid(row = 2, column =2)
    Price_label = Label(root, text="Enter the Purchasing Price", padx = 10).grid(row = 3,column=1)
    global price
    price = Entry(root)
    price.grid(row = 3,column =2)
    Button(root, text = "Confirm Selling", command = chooseCar).grid(row=4, column =1, columnspan = 2)
def chooseCar():
    user = buyer.get()
    user= re.search("'(.*)'", user).group(1)

    ca = car.get()
    rev = review.get()
    rate = Rating.get()
    pric = price.get()
    
    mycursor = mydb.cursor()

    sql = """
        update car set review = '{}', rating = '{}', username='{}', purchase_price = {} where ad_link = '{}'
        """.format(rev,rate,user, pric, ca)

    mycursor.execute(sql)
    mydb.commit()
    
    
    Label(root, text="Sale is registered").grid(row = 5, column = 1, columnspan = 2)


# In[1156]:


def view_sale():
    for widgets in root.winfo_children():
        widgets.destroy()
    mycursor = mydb.cursor()
    sql = """
        select b.username from buyer b left outer join car c on b.username = c.username where ad_link is NULL
        order by 1
        """
    mycursor.execute(sql)
    buyers_res = mycursor.fetchall()
    global buyer
    buyer = StringVar()
    buyers = OptionMenu(root, buyer, *buyers_res)
    buyers.grid(row = 0, column = 0)

    Button(root, text = "Select Buyer", command = chooseBuyer).grid(row=1, column =0, columnspan = 1)
    Button(root, text = "Return Home", command = ReturnHome).grid(row=6, column =1, columnspan = 2)


# In[ ]:



root=tk.Tk(className = 'Used Cars')
root.geometry('700x300')

Label(root, text = "Home Page", pady = 20, padx = 20, font=('Calibra', 24)).grid(row=0, column = 1)

make = StringVar()
body = StringVar()
year = StringVar()
loc = StringVar()
feature = StringVar()
lower = IntVar()
upper = IntVar()

button = tk.Button(root, text='Register New User', width=25, command = view_register)
button.grid(row=1, column = 0)
button = tk.Button(root, text='Add a Sale', width=25, command = view_sale)
button.grid(row=1, column = 1)
button = tk.Button(root, text='View Reviews of an Ad', width=25, command = view_ad_rev)
button.grid(row=1, column = 2)
button = tk.Button(root, text='View Rating of an Owner', width=25, command = view_owner_rate)
button.grid(row=2, column = 0)
button = tk.Button(root, text='Show Ad of a Specific Car', width=25, command = view_show_car)
button.grid(row=2, column = 1)
button = tk.Button(root, text='Show Cars from Location and Price', width=25, command = view_car_loc)
button.grid(row=2, column = 2)
button = tk.Button(root, text='Show Top Locations', width=25, command = view_top_location)
button.grid(row=3, column = 0)
button = tk.Button(root, text='Show Top Sellers', width=25, command = view_top_seller)
button.grid(row=3, column = 1)
button = tk.Button(root, text='Show All listings by a Seller', width=25, command = view_listing)
button.grid(row=3, column = 2)
button = tk.Button(root, text='Show Top Car inventories', width=25, command = view_top_car)
button.grid(row=4, column = 1)


root.mainloop()

