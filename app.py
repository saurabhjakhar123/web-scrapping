from flask import Flask, render_template, request
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs

app = Flask(__name__)

@app.route('/' , methods = ["GET", "POST"])
def home_page():
    return render_template('index.html')

@app.route('/search', methods = ["GET", "POST"])
def search_result():
    try:
        items_list = []
        search_for = request.form['searching_for'].replace(" ", '+')
        comp_url = "https://www.flipkart.com/search?q=" + search_for
        url_open = urlopen(comp_url)
        read_url = url_open.read()
        beautify_url = bs(read_url, 'html.parser')
        bigBox = beautify_url.findAll("div", {"class" : "_2kHMtA"})
        
        
        for i in bigBox:
            items_dict = {}
            #title
            title = i.find("div", {'class' : '_4rR01T'}).text
            items_dict["title"] = title

            #rating
            rating = i.find("div", {'class' : '_3LWZlK'}).text
            items_dict["rating"] = rating
            
            #people_count
            people_count = i.find("span", {'class' : '_2_R_DZ'}).text
            items_dict["people_count"] = people_count
            
            #price
            price = i.find("div", {'class' : '_30jeq3 _1_WHN1'}).text
            items_dict["price"] = price

            #product_link
            link = i.find("a", {"class" : "_1fQZEK"})["href"]
            product_link = "https://flipkart.com"+link
            items_dict["product_link"] = product_link 
            

            #key_specifications
            ul_list = i.find("ul", {'class': '_1xgFaf'})
            specs = []
            if ul_list:
                for li in ul_list.find_all('li'):
                    specs.append(li.text)
            items_dict["key_specs"] = specs

            items_list.append(items_dict)
            
        # return render_template('result.html', search_result = search_for, searching = items_list[0:len(items_list)])
        return render_template('result.html', search_result = search_for, searching = items_list[:])
    except Exception as e:
        return render_template('error.html', error = e)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
#--------------------------------------------------
#testing
