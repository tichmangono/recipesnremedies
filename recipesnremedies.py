###############################################################################
                #--------MY RECIPES 'N REMEDIES recipesnremediesLICATION-------------------#
###############################################################################

"""
This should take our data from a plain text file, (in the future maybe from
 MS Word to txt and to python readable type - list and/or string)

#FIXME - Is it possible to use python to open word file and convert it into
a txt format normally - with line breaks and replaceable xters options 
just like in the manual save-as menu?

This program should make it easier to retrieve out options of what we want 
to have at any time on any day. I will also be easily connected to a web 
recipesnremedieslication and small database. Enjoy!

    author  :   Tich Mangono
    date    :   10/24/15
    project :   Independent

"""

# import the modules we need
import os
import sqlite3

from flask import Flask, render_template, request, g

# Create the recipesnremedieslication object
recipesnremedies = Flask(__name__)
#recipesnremedies.debug = True
# Add in a configuration variable for the database, assign
recipesnremedies.database ="cookbook.db"

#use decorators to link the function to a url
@recipesnremedies.route('/', methods=['GET', 'POST'])
def home():
    """ Function for flask interaction with the html webpage - homepage or index"""

    try:
        # g is a temp object specific to flask and it stores the database 
        #connection in this case
        # this value is reset after each request use it to connect and store
        # the db object
        g.db = connect_db()
        cur= g.db.execute('SELECT * FROM recipes')
        
        # #cast the data to a dictionary
        recipes = [
                    dict
                        (
                        dish_index = row[0],
                        dish_name= row[1],
                        dish_method = row[2],
                        category= row[3]
                        ) for row in cur.fetchall()
                    ]
        #close the database
        g.db.close()
        return render_template('index.html', recipes=recipes) #render a template

    except Exception as e:
        return str(e)

#decorator and function to add the url for the search page
@recipesnremedies.route('/search', methods=['GET', 'POST'])
def search():
    """ Function for search page of the recipes page"""
    try:  
        g.db = connect_db()
        #search_var = request.form['search']
        cur= g.db.execute('SELECT * FROM recipes')
        # #cast the data to a dictionary
        recipes = [
                    dict
                        (
                        dish_index = row[0],
                        dish_name= row[1],
                        dish_method = row[2][:45],
                        category= row[3]
                        ) for row in cur.fetchall()
                    ]       
        g.db.close()
       
        search = [request.form['search']]

        return render_template('search.html', recipes=recipes, search=search)
        
    except Exception as e: 
        return str(e)
    
#return render_template('search.html') # render search page

#decorator and function to add the url for the search page
@recipesnremedies.route('/detail', methods=['GET', 'POST'])
def detail():
    #return 'Hello'
    # search the database based on input from search box!
    try: 
        g.db = connect_db()
        #search_var = request.form['search']
        cur= g.db.execute('SELECT * FROM recipes')
        # #cast the data to a dictionary
        recipes = [
                    dict
                        (
                        dish_index = row[0],
                        dish_name= row[1],
                        dish_method = row[2],
                        category= row[3]
                        ) for row in cur.fetchall()
                    ]       
        g.db.close()
        
        input = [request.form['input']]
       
        return render_template('detail.html', recipes=recipes, input=input)
        
    except Exception as e: 
        return str(e)

#use decorators to link the function to a url
@recipesnremedies.route('/health', methods=['GET', 'POST'])
def health():
    """ Function for flask interaction with the html webpage - homepage or index"""
    # g is a temp object specific to flask and it stores the database connection 
    # in this case this value is reset after each request use it to 
    # connect and store the db object
    
    try:        
        g.db = connect_db()
        cur= g.db.execute('SELECT * FROM remedies')
        
        # #cast the data to a dictionary
        remedies = [
                    dict
                        (
                        index = row[0],
                        name= row[1],
                        method = row[2],
                        category= row[3]
                        ) for row in cur.fetchall()
                    ]
        #close the database
        g.db.close()

        return render_template('health.html', remedies=remedies) #render template
        #return 'Hello World'
    except Exception as e:
        return str(e)

#decorator and function to add the url for the search page
@recipesnremedies.route('/hsearch', methods=['GET', 'POST'])
def hsearch():
    #return 'Hello'
    # search the database based on input from search box!
    try: 
        g.db = connect_db()
        #search_var = request.form['search']
        cur= g.db.execute('SELECT * FROM remedies')
        # #cast the data to a dictionary
        remedies = [
                    dict
                        (
                        index = row[0],
                        name= row[1],
                        method = row[2][:45],
                        category= row[3]
                        ) for row in cur.fetchall()
                    ]       
        g.db.close()
       
        search = [request.form['search']]
        
        return render_template('hsearch.html', remedies=remedies, search=search)
        
    except Exception as e: 
        return str(e)
    
#return render_template('search.html') # render search page

#decorator and function to add the url for the search page
@recipesnremedies.route('/hdetail', methods=['GET', 'POST'])
def hdetail():
    try: 
        g.db = connect_db()
        #search_var = request.form['search']
        cur= g.db.execute('SELECT * FROM remedies')
        # #cast the data to a dictionary
        remedies = [
                    dict
                        (
                        index = row[0],
                        name= row[1],
                        method = row[2],
                        category= row[3]
                        ) for row in cur.fetchall()
                    ]       
        g.db.close()
       
        input = [request.form['input']]
       
        return render_template('hdetail.html', remedies=remedies, input=input)
        
    except Exception as e: 
        return str(e)
        
#initiatilizing global variables
bon_apetit=[]
relief =[]

# delare the main source file for the recipe data. Currently puling from text file
# MY_FILE = 'C:\\Users\\Tichakunda Mangono\\My Projects\\recipe\\recipes.txt'
# Using os path to avoid hard-coding: remedy file and recipe file
s = '\\'
dir = os.getcwd()
folder = 'datafiles'
file1 = 'recipes.txt'
file2 = 'remedies.txt'
path1 = [dir, folder, file1]
path2 = [dir, folder,file2]

MY_RECIPES_FILE = s.join(path1)
MY_REMEDIES_FILE = s.join(path2)

def insert_to_db(bon_apetit, relief):    
    """
    This is our database interaction function. It will take our final recipes data 
    and insert it into a sqlite3 db to be accessed by the web recipesnremedies later
    """
    # Create database if it does not exist
    with sqlite3.connect("cookbook.db") as connection:
        c= connection.cursor()
    #drop table just in case, we want to make a new one    
        print("\nDrop and create recipes table.....")
        c.execute("""DROP TABLE if exists recipes""")
    #create table to insert our recipes
        c.execute('''CREATE TABLE recipes(dish_index INTEGER, 
                                        dish_name TEXT, 
                                        dish_method TEXT, 
                                        category TEXT)''')
        print("\nDrop and create remedies table.....")
        c.execute("""DROP TABLE if exists remedies""")
        c.execute('''CREATE TABLE remedies(H_index INTEGER, 
                                        name TEXT, 
                                        method TEXT, 
                                        category TEXT)''')
        #insert the extract recipe dictionary into our new database, 
        #using for loop
        print("\nInserting values into remedies table.....\n")
        #ran = random.randrange(4,73)
        ran = range(0,74)
        for item in ran:            
            c.execute('''INSERT INTO recipes VALUES (?,?,?,?)''', 
                        [
                        bon_apetit[item]['dish index'],
                        bon_apetit[item]['dish name'],
                        bon_apetit[item]['dish method'],
                        bon_apetit[item]['category']
                        ]
                        )
        print("\nInserting values into remedies table.....\n")
        #ran = random.randrange(4,73)
        ran = range(0,321)
        for item in ran:            
            c.execute('''INSERT INTO remedies VALUES (?,?,?,?)''', 
                        [
                        relief[item]['index'],
                        relief[item]['name'],
                        relief[item]['method'],
                        relief[item]['category']
                        ]
                        )
                                                 
def connect_db():
    """ Function to add an object (database) that we can connect to
    To test the db object is connectable to:
    go to cmd, and open python shell
    ----BEGIN-------
    from recipesnremedies import *
    c= connect_db()
    c
    c.close()
    ----END-------
    """ 
    return sqlite3.connect(recipesnremedies.database)
    
    
def get_recipes(recipe_file):
    """ 
    This will locate the file and load the content and change items
    to python format
    """
    #declare our output,  alist of dictionaries as global 
    # to enable the insert into db function to access it later
    global bon_apetit
    
    print("\nOpening file.......")
    f = open(recipe_file, 'r')
    
    # read the whole file into  a single string, but skip over the table 
    # of contents
    print("\nReading file.......")
    text = f.read()
    f.close()    
    #split the string along the line breaks? #FIXME - may need another way
    recipe_list = text.strip().split('\n\n')
        
    # Now organize the recipes into recipesnremediesropriate categories"""
    cookbook ={}
    categories = [#'To Cook List',
                    'Breakfast',
                    'Lunch & Veggie Dishes',
                    'Meat',
                    'Dessert',
                    'Drinks']
    test_cat= []
                    
    # Find out exactly where the categories are located in recipe list           
    cat_pos = [i for i,x in enumerate(recipe_list) if x in categories]
    
    # insert recipes with their categories into a dictionary
    # run through the list of recipes
    #Now assign categories
    #FIXME PLEASE!! There has to be a better way that this
    #this is brute force!!! A more pythonic way
    print("\nCategorizing recipes.......")
    for item in recipe_list:
        if recipe_list.index(item) in cat_pos:
            cookbook[recipe_list.index(item)] = recipe_list.index(item)        
        if recipe_list.index(item)< cat_pos[1]:
            cookbook[recipe_list.index(item)] = cat_pos[0]
        if recipe_list.index(item)> cat_pos[1] and recipe_list.index(item)< cat_pos[2]:
            cookbook[recipe_list.index(item)] = cat_pos[1]
        if recipe_list.index(item)> cat_pos[2] and recipe_list.index(item)< cat_pos[3]:
            cookbook[recipe_list.index(item)] = cat_pos[2]
        if recipe_list.index(item)> cat_pos[3] and recipe_list.index(item)< cat_pos[4]:
            cookbook[recipe_list.index(item)] = cat_pos[3]      
        if recipe_list.index(item)> cat_pos[4]: #and recipe_list.index(item)< cat_pos[5]:
            cookbook[recipe_list.index(item)] = cat_pos[4]      
        #if recipe_list.index(item)> cat_pos[5]:
            #cookbook[recipe_list.index(item)] = cat_pos[5]
    
    #separate out the two components of the cookbook, to keep indices in order
    #and split the menu entries further to get the name of the dish
    dish_index =[i for i,x in cookbook.items()]
    cat_index =[x for i,x in cookbook.items()]

    dish_name =[]
    dish_method=[]
    
    for i in dish_index:
        split = recipe_list[i].strip().split('\n',1)
        if len(split)<2:
            dish_name.recipesnremediesend(split[0])
            dish_method.recipesnremediesend("N/A")
        else:
            dish_name.recipesnremediesend(split[0])
            dish_method.recipesnremediesend(split[1])
            
    # Finally construct an all-encompasing dictionary, combining
    # dish names and the respective methods, and adding their category!
    print("\nAlmost there.......")
    bon_apetit = []
    for i in dish_index:
        bon_apetit.recipesnremediesend({
                       "dish index": i,
                       "dish name": dish_name[i],
                       "dish method": dish_method[i],
                       "category": recipe_list[cat_index[i]]
                            })
    return bon_apetit

def get_remedies(remedy_file):
    """ 
    This will locate the file and load the content and change items
    to python format. Later, this function can be generalized and 
    used for both recipes and remedies to minimize the code
    
    """
    #declare our output,  alist of dictionaries as global 
    # to enable the insert into db function to access it later
    global relief
    
    print("\nOpening file.......")
    f = open(remedy_file, 'r')
    
    # read the whole file into  a single string, but skip over the 
    # table of contents
    print("\nReading file.......")
    text = f.read()
    f.close()  
    
    # make toc, kind of a raw table of contents from the text file
    # this will help us to separate and locate the titles in the
    # document's table of content to use as a reference later
    # if we can find the positions of these titles and the are numbered
    # corrrectly in a consecutive manner, then the text between these 
    # titles will belong to the previous title. Voila! We have a way to
    # demarcate, locate, label and extract specific related pieces of
    # text. This is a master parsing function!
    c = text.strip().split('\n')
    toc = []
    for item in c:
        if '\t' in item:
            toc.recipesnremediesend(item)
        else:
            pass

    # for raw table of contents separate the titles with two tabs surrounding (tabs)
    # from the ones that have one tab and one peiod (dots)
    dots ={}
    tabs ={}
    for title in toc:
        i = toc.index(title)
        if '. ' in title:
            dots[i]=title.split('. ')
        elif '\t' in title:
            tabs[i] = title.split('\t')
        else:
            pass
            
    # Still working with the titles only, clean up the dots list and keep the value of its pasition
    # keep the page numbers and the roman numeral numbering 
    # in case we need these later
    dots_list =[]
    for key,value in enumerate(dots):
        x = dots[value][0]        
        y = dots[value][1].split('\t')[0]
        dots_list.recipesnremediesend([value, x, y])    
    
    tabs_list =[]
    for key,value in enumerate(tabs):
        x = tabs[value][0]
        y = tabs[value][1]
        tabs_list.recipesnremediesend([value, x, y])
    
    # COncatenate the full list from dots and tabs
    full_list = dots_list + tabs_list
    full_list.sort(key = lambda x:x[1] )
    
    #split the string along the line breaks? #FIXME - may need another way
    remedy_list = text.strip().split('\n')
    chunky_list = text.strip().split('\n\n')    
    lookup_list = ''.join(remedy_list) #searchable for categories later
    raw_list = ''.join(chunky_list[:2]).split('\n')
    
    #loop and remove the trailing tab tags, last 3 characters for each
    lst_of_lst =[]
    for item in raw_list:        
        if '\t' in item:
            lst_of_lst.recipesnremediesend(item.split('\t'))
    tbl_of_contents = []
    
    for item in full_list:    
        tbl_of_contents.recipesnremediesend(item[2])
        
    # Now take out the table of content from original split list
    # first removing trailing text on table of contents cast to separate list
    x = lookup_list.split('Have in garden')
    threshold =len(x[0])    

    # Now organize the recipes into recipesnremediesropriate categories
    # insert recipes with their categories into a dictionary
    # run through the list of recipes
    
    #find position of table of content element in the big list/string
    ref_list =[]   
    m = len(lookup_list)
    listZ = lookup_list[threshold:m]
        
    for i in range(len(tbl_of_contents)):
        item =tbl_of_contents[i]
        start = listZ.find(item.strip())
        end = start + len(item)
        ref_list.recipesnremediesend([int(start), int(end), item])
    
    # sort list
    ref_list.sort(key = lambda x:x[0])        
    print(len(ref_list))    

    for i in range(len(ref_list)-1):
        if i>=1:
            dict = {}
            x =ref_list[i-1][1]
            y =ref_list[i][0]
            if len(listZ[x:y].strip())<=2:
                z='source'
            else:
                z='remedy'
            
            dict['index'] = int(i-1)
            dict['name'] = ref_list[i-1][2]
            dict['method'] = listZ[x:y]
            dict['category'] = z
            relief.recipesnremediesend(dict)
        else:
            pass        

    return relief
    
def search_recipes(): #TODO must add code to searh by other criteria
    """ This is a search function that retrives specific recipes based 
        on desired search criteria. """
    global bon_apetit
    
    # run the get recipe func and put it into a data object
    data = get_recipes(MY_FILE)
    
    # insert this data into a database 
    #(will replace the data obj in search soon)
    insert_to_db(bon_apetit)
    
    #Get index for how long the list is
    max = len(data)

    print('\n--------\nYou have a total of ', str(max), ' records')

    # Can add in the future searchable
    # star_ranking
    # hall_of_fame

    # Quick search function by index
    index = int(input('\nEnter number less than '+ str(max)+
                   ' to search recipes by index: '))    
    print(
          '\n#Great Choice! today you can enjoy:\n\n',
          data[index]['dish name'],
          'for ',data[index]['category'],
         '\n\n#Preparation Instructions:\n\n',
          data[index]['dish method']
          )

def loopy():
    """ Just a conditional function to loop over the main search"""
    search_again = input('\nLooking for a recipe:[Y/N]?')
    if search_again not in ('y', 'Y', 'n', 'N'):
        print("Invalid input")    
        search_again = input('\nTry another search:[Y/N]?')  
    elif search_again in ('n', 'N'):
        print("Goodbye!")
    else:
        search_recipes()        

def main():
    """ This runs the actual logic of the program, calling all the helper functions"""
    #search_again = input('\nLooking for a recipe:[Y/N]?')
    #disable for now 
    #loopy()
    #search_recipes()
    get_recipes(MY_RECIPES_FILE)
    get_remedies(MY_REMEDIES_FILE)
    insert_to_db(bon_apetit, relief)
    recipesnremedies.run()
                
if __name__ == "__main__":
    main()
