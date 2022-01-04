from bs4 import BeautifulSoup
import requests
from flask import Flask,render_template,request


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/details',methods = ['POST','GET'])
def Details_fun():
    res = ""
    if request.method == 'POST':
        SearchString = request.form['SearchString']
        res = SearchString.replace(" ","") 

        url = "https://www.flipkart.com/search?q="+res
        res = requests.get(url).content
        soup = BeautifulSoup(res,"html.parser")
        titiles = []
        ratings = []
        prices = []
        rating_given_by = []
        reviwe_given_by = []
        titile = soup.findAll('div',{'class':'_4rR01T'})
        rating = soup.findAll('div',{'class':'_3LWZlK'})
        price  = soup.findAll('div',{'class':'_25b18c'})
        for i in titile:
            titiles.append(i.text)
        for i in rating:
            ratings.append(i.text)
        for i in price:
            text1 = i.text
            lst1 = text1.split('₹')
            p = lst1[1]
            prices.append(p)
        rating_and_reviwes_given_by = soup.findAll('span',{'class':'_2_R_DZ'})
        for i in rating_and_reviwes_given_by:
            text2 = i.text
            lst2 = text2.split('&')
            rgb1 = lst2[0]
            rgb2 = lst2[1]
            rating_given_by.append(rgb1.split()[0])
            reviwe_given_by.append(rgb2.split()[0])
            data = []
        for title, rating, number_of_ratings, number_of_revies, price in zip(titiles, ratings, rating_given_by,reviwe_given_by,prices):
            new_data = []
            new_data = [title, rating, number_of_ratings, number_of_revies, price]
            data.append(new_data) 
        headers = ["Titiles","Rating","Number of ratings","Number of reviews","Prices"]
        
    return render_template('result.html',data = data,SearchString=SearchString,headers=headers) 

if __name__=="__main__":
    app.run(debug=True)