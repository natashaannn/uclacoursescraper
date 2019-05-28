import pandas as pd
import codecs
import bs4 #importing the beautifulsoup library i.e. the webscraping parser
from urllib.request import urlopen as uReq #module that opens URLs
from bs4 import BeautifulSoup as soup #renaming beautiful soup into something easier to type

catalog_url = 'http://catalog.registrar.ucla.edu/ucla-catalog18-19-4.html' #the website you want to scrape
uClient = uReq(catalog_url) #downloading and requesting data from url
catalog_html = uClient.read() #dumping requested data into a variable
uClient.close() #exiting the requester so that it won't keep requesting data (might cause overloading)

catalog_page = soup(catalog_html,'html.parser')  #parsing the downloaded data to give a nested data structure for us to navigate

with codecs.open("majors.csv", 'w', 'utf8') as f:
    f.write("Major" + "," + "Courses" + "," + "\n")

    list = catalog_page.findAll('a',{'class':"main"}) #finds data that corresponds to attributes such as class or id

    for major in list: #creating the loop for code to run on ALL divs, not just first one
        major_name = major.text #indicating which particular item within the div we want
        major_link = "http://catalog.registrar.ucla.edu/" + major.get("href")

        uClient = uReq(major_link)
        link_html = uClient.read()
        uClient.close()

        link_page = soup(link_html,'html.parser')

        header = link_page.find('div',{'class':"main-text"}).h1.text

        maintext = link_page.findAll('p')

        course = ""

        for paragraph in maintext:
            paragraphtext = paragraph.text
            if "Required" in paragraphtext:
                course = course + paragraphtext

        if " BA"  in header or " BS" in header:
            f.write('"' + header + '"' + "," + '"' + course + '"' + ',' + '\n')

        else:
            link2list = link_page.findAll("a",{"class":"main"})

            for link2 in link2list:
                link2text = link2.text

                if " BA" in link2text or " BS" in link2text:
                    major_link2 = "http://catalog.registrar.ucla.edu/" + link2.get("href")

                    uClient = uReq(major_link2)
                    link2_html = uClient.read()
                    uClient.close()

                    link2_page = soup(link2_html,'html.parser')

                    header2 = link2_page.find('div',{'class':"main-text"}).h1.text

                    maintext2 = link2_page.findAll('p')

                    course2 = ""

                    for paragraph in maintext2:
                        paragraphtext = paragraph.text
                        if "Required" in paragraphtext:
                            course2 = course2 + paragraphtext

                    if " BA"  in header2 or " BS" in header2:
                        f.write('"' + header2 + '"' + "," + '"' + course2 + '"' + ',' + '\n')

f.close() #closes file
