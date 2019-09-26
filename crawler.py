from bs4 import BeautifulSoup
import requests

def openAndreadGermanWords():
    with open("test.txt", "r") as germanFile:
        return [word.strip() for word in germanFile]

def appendEnglischWords(word):
    with open("englishWords.txt", "a") as englischFile:
        englischFile.write(word+'\n')

def searchEnglischInHerkunft(htmlWordPage, word):
    for element in htmlWordPage.find_all('div', {'id': 'herkunft'}):
        paragraph = element.find("p").text
        if "englisch" in paragraph:
            appendEnglischWords(word)

def checkUmlaut(word):
    if 'Ä' in word:
        nW = word.replace("Ä","Ae")
    elif 'Ö' in word:
        nW = word.replace("Ö","Oe")
    elif 'Ü' in word:
        nW = word.replace("Ü","Ue")
    elif 'ä' in word:
        nW = word.replace("ä","ae")
    elif 'ö' in word:
        nW = word.replace("ö","oe")
    elif 'ü' in word:
        nW = word.replace("ü","ue")
    else:
        nW = word
    return nW 

def crawlOptionalLinks(htmlPage, word):
    #urls = []
    for link in htmlPage.find_all('a', {'class': 'vignette__label'}):
        href = link.get('href')

        if href is not None:
            splitURl = href.split("/")
            splitW = splitURl[2].split("_")
            wordChecked = checkUmlaut(word)

            if wordChecked == splitW[0]:
                wordUrl = "https://www.duden.de" + href
                #urls.append(wordUrl)
                pageWord = requests.get(wordUrl)
                
                if pageWord.status_code == 200:
                    htmlWordPage = BeautifulSoup(pageWord.text, 'lxml')
                    searchEnglischInHerkunft(htmlWordPage,word)
                else: 
                    print("Status code of Word Page: " ,pageWord.status_code)
                #return wordUrl # return the first link of each word
    #return urls

def processWebPage(word):
    url = 'https://www.duden.de/suchen/dudenonline/'+word
    page = requests.get(url)
    if page.status_code == 200:
        htmlPage = BeautifulSoup(page.text, 'lxml')
        crawlOptionalLinks(htmlPage,word)
    else:
        print("Status code of Page: " ,page.status_code)

def main():
    germanWords = openAndreadGermanWords()
    for word in germanWords:
        print("Processing word: ",word)
        processWebPage(word) 

if __name__ == "__main__":
    main()
