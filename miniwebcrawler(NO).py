from bs4 import BeautifulSoup
import requests

def openAndreadGermanWords():
    with open("test.txt", "r") as germanFile: # with statement automatically takes care of closing the file once it leaves the with block
        #allGermanWords = germanFile.read()
        return [word.strip() for word in germanFile]

def appendEnglischWords(setWords):
    with open("englischWords.txt", "a+") as englischFile:
        for word in setWords:
            word = str(setWords)
            englischFile.write(word+'\n')

def crawlOptionalLinks(soup):
    allLinks = []
    for link in soup.find_all('a', {'class': 'vignette__label'}): # 'class': 'vignette__label'
        href = link.get('href')
        wordUrl = "https://www.duden.de" + href
        allLinks.append(wordUrl)
    return allLinks

def searchEnglischInHerkunft(urls,word):
    englischWords = set()
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        for element in soup.findAll('div', {'id': 'herkunft'}):
            paragraph = element.find("p").text
            if "englisch" in paragraph:
                englischWords.add(word)
    return englischWords

def main():
    germanWords = openAndreadGermanWords()
    url = 'https://www.duden.de/suchen/dudenonline/'
    for word in germanWords:
        try:
            print(word)
            page = requests.get(url+word)
            page.raise_for_status()#If the response was successful, no Exception will be raised
            soup = BeautifulSoup(page.text, 'lxml') #html5lib
            urls = crawlOptionalLinks(soup)
            englischWords = searchEnglischInHerkunft(urls,word)
            appendEnglischWords(englischWords)
                    
        except page.exceptions.RequestException as err:
            print ("Oops: Something Else",err)
        except page.exceptions.HTTPError as errh:
            print ("General Kenovi (Http Error):",errh)
        except page.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        except page.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)    

if __name__ == "__main__":
    main()
