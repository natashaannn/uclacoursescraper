import pandas as pd
import codecs
import bs4 #importing the beautifulsoup library i.e. the webscraping parser
from urllib.request import urlopen as uReq #module that opens URLs
from bs4 import BeautifulSoup as soup #renaming beautiful soup into something easier to type
from string import ascii_uppercase
import csv

catalog_url = 'https://catalog.registrar.ucla.edu/ucla-catalog18-19-271.html' #the website you want to scrape
uClient = uReq(catalog_url) #downloading and requesting data from url
catalog_html = uClient.read() #dumping requested data into a variable
uClient.close() #exiting the requester so that it won't keep requesting data (might cause overloading)

catalog_page = soup(catalog_html,'html.parser')  #parsing the downloaded data to give a nested data structure for us to navigate

with codecs.open("courses.csv", 'w', 'utf8') as f:
    f.write("Word" + "," + "Tag" + "\n")

    list = catalog_page.findAll('a',{'class':'main'}) #finds data that corresponds to attributes such as class or id

    for course in list: #creating the loop for code to run on ALL divs, not just first one
        course_name = course.text #indicating which particular item within the div we want
        words = course_name.split()

        for word in words:
            if word == words[0]:
                f.write('"' + word + '"' + "," + 'B-course' + '\n')
            else:
                f.write('"' + word + '"' + "," + 'I-course' + '\n')

    for x in range(1,199):
        course_number = str(x)
        f.write('"' + course_number + '"' +  "," + "I-course" + "\n")
        for c in ascii_uppercase:
            course_code = course_number + c
            f.write('"' + course_code + '"' +  "," + "I-course" + "\n")

f.close() #closes file

with open('courses.csv','r') as csvin, open('courses.tsv', 'w') as tsvout:
    csvin = csv.reader(csvin)
    tsvout = csv.writer(tsvout, delimiter='\t')

    for row in csvin:
        tsvout.writerow(row)
