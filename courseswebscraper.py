import codecs
import bs4 #importing the beautifulsoup library i.e. the webscraping parser
from urllib.request import urlopen as uReq #module that opens URLs
from bs4 import BeautifulSoup as soup #renaming beautiful soup into something easier to type
from string import ascii_uppercase
import string
import csv

#major and requirements scraper
def majorscraper(catalog_url,majors,requirements):
    uClient = uReq(catalog_url) #downloading and requesting data from url
    catalog_html = uClient.read() #dumping requested data into a variable
    uClient.close() #exiting the requester so that it won't keep requesting data (might cause overloading)

    catalog_page = soup(catalog_html,'html.parser')  #parsing the downloaded data to give a nested data structure for us to navigate

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
            majors.append(header)
            requirements.append(course)

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
                        majors.append(header2)
                        requirements.append(course2)

#course code scraper
def coursecodescraper(catalog_url,course_names,course_codes):
    uClient = uReq(catalog_url) #downloading and requesting data from url
    catalog_html = uClient.read() #dumping requested data into a variable
    uClient.close() #exiting the requester so that it won't keep requesting data (might cause overloading)

    catalog_page = soup(catalog_html,'html.parser')  #parsing the downloaded data to give a nested data structure for us to navigate

    list = catalog_page.findAll('a',{'class':'main'}) #finds data that corresponds to attributes such as class or id

    for course in list: #creating the loop for code to run on ALL divs, not just first one
        course_name = course.text #indicating which particular item within the div we want
        course_names.append(course_name)

    for x in range(1,199):
        course_number = str(x)

        course_codes.append(course_number)

        for c in ascii_uppercase:
            course_alphanumber = course_number + c
            course_numberalpha = c + course_number

            course_codes.append(course_alphanumber)
            course_codes.append(course_numberalpha)

majors = []
requirements=[]
course_names = []
course_codes = []
# majorscraper('http://catalog.registrar.ucla.edu/ucla-catalog18-19-4.html', majors)
coursecodescraper('https://catalog.registrar.ucla.edu/ucla-catalog18-19-271.html', course_names, course_codes)
majorscraper('https://catalog.registrar.ucla.edu/ucla-catalog18-19-4.html', majors, requirements)

# with codecs.open("major_requirements.csv", 'w', 'utf8') as f:
#     for requirement, major in zip(requirements, majors):
#         for course_name in course_names:
#             if requirement.find(course_name) != -1:
#                 f.write('"' + major + '"' +  "," + '"' + course_name + '"' + "\n")
# f.close()

with codecs.open("major_course_requirements.csv", 'w', 'utf8') as f:
    for require, major in zip(requirements, majors):
        indexes = []
        requirement = require.translate(str.maketrans('', '', string.punctuation))
        for course_name in course_names:
            if requirement.find(course_name) != -1:
                indexes.append(requirement.index(course_name))

        indexes.append(len(requirement)-1)

        for x in range(0,(len(indexes)-2)):
            for course_name in course_names:
                if requirement.find(course_name, indexes[x],indexes[x+1]) != -1:
                    for course_code in course_codes:
                        space_course_code = " " + course_code + " "
                        if requirement.find(space_course_code,indexes[x],indexes[x+1]) != -1:
                            f.write('"' + major + '"' +  "," + '"' + course_name + '"' + "," + '"' + course_code + '"' + "\n")

                        if requirement.find(space_course_code,indexes[(len(indexes)-1)],(len(requirement)-1)) != -1:
                            f.write('"' + major + '"' +  "," + '"' + course_name + '"' + "," + '"' + course_code + '"' + "\n")
f.close()
