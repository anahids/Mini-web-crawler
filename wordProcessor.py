import csv
import re

def openEnglishWords():
    with open('englishWords.txt', 'r') as wordList: 
        englishList = []
        for word in wordList:
            englishList.append(word)
        return ([e.strip('\n') for e in englishList])

def openArticles(): 
    with open('articles.csv') as articlesFile:  
        reader = csv.reader(articlesFile)
        cleanArticles(reader)

def cleanArticles(reader):
    d = []    
    for article in reader:
        joinElements = [','.join(article)]
        for element in joinElements:
            clean = [re.sub(r'[^a-zA-ZäöüÄÖÜß0-9]', ' ', element)]
            d.append(compare(clean))
    for index,val in enumerate(d, start=1):
        print("No. Article: " + str(index) + " " + str(val))

def compare(cleanList):
    found = []
    result = []
    keys = ['Article length', 'Number of matches', 'Percentage of english words', 'Words found']

    englishList = openEnglishWords()
    for element in cleanList:
        splits = element.split()
        for word in splits:
            if word in englishList:
                found.append(word)

    totalWords =  len(splits)
    result.append(totalWords)
    wordsFound = len(found)
    result.append(wordsFound)
    percentage = round(((wordsFound * 100.0)/totalWords),2)
    result.append(percentage)
    result.append(found)
    
    return dict(zip(keys,result))

def main():
    openArticles()

if __name__ == "__main__":
    main()