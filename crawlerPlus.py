from bs4 import BeautifulSoup
import requests

# This function append the Herkunft and the Grammatik to the txt
def appendEnglischWords(word):
    with open("englishWordsPlus.txt", "a") as englischFile:
        englischFile.write(word)

# This function search the section grammatik and then look for a table that contains the conjugations or the paragraph of the section that also contains the conjugations
def searchInGrammatik(htmlWordPage):
    grammatik = htmlWordPage.findAll('div', {'id': 'grammatik'})
    for gElement in grammatik:
        table = gElement.find("table")
        t = gElement.find("p")
        if t is not None:
            tText = t.text
            appendEnglischWords(" Grammatik: "+tText)
        elif table is not None:
            singular = table.find("tbody").find("tr").findAll("td")[0].text
            plural = table.find("tbody").find("tr").findAll("td")[1].text
            appendEnglischWords(" Grammatik: " + singular + " ")
            appendEnglischWords(plural+'\n')      

# This funcion get the link of the next word
def get_link(htmlWordPage):
    link =  htmlWordPage.findAll('a', {'class': 'hookup__link'})[5]
    href = link.get('href')
    url = 'https://www.duden.de' + href   
    return url

# This function search if there is the Herkunft section
def searchEnglischInHerkunft(htmlWordPage):
    herkunft = htmlWordPage.find('div', {'id': 'herkunft'})
    if not herkunft:
        return ""
    else: 
        paragraph = herkunft.p.text
        if "englisch" in paragraph:
            appendEnglischWords("Herkunft: "+paragraph)
            searchInGrammatik(htmlWordPage)

# This function request and process the web page and use Beautiful Soup to analize the HTML doc and then extract information
def processWebPage(url):
    page = requests.get(url)
    if page.status_code == 200:
        htmlPage = BeautifulSoup(page.text, 'lxml')
        return htmlPage
    else:
        print("Status code of Page: " ,page.status_code)
        print("Repeating request for Page: ", url)
        processWebPage(url)

# This function calls recursively to continue crawling the pages
def start(url):
    html = processWebPage(url)
    searchEnglischInHerkunft(html)
    next_link = get_link(html)
    print(next_link)
    start(next_link)

def main():
    url = 'https://www.duden.de/rechtschreibung/Aachen'
    #url = 'https://www.duden.de/rechtschreibung/Computer'
    #url = 'https://www.duden.de/rechtschreibung/Abalone'
    start(url) 

if __name__ == "__main__":
    main()
