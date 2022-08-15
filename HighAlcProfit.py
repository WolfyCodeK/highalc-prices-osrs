from math import floor
from time import sleep
from bs4 import BeautifulSoup
import requests
import re
import os

# thread sleep length
pauseLength = 1
# how often the data gets updated in seconds
defaultLoadTime = 32

cmd = 'mode 34,8'
os.system(cmd)
cmd = 'color 06'     
os.system(cmd)

# beautiful soup header
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
}

# url of high alc prices wiki
url = "https://oldschool.runescape.wiki/w/High_Level_Alchemy"
    
# The price considered valuable
defaultProfit = 0
print("      [MINIMUM PROFIT SHOWN]")
#print("ALL ITEMS -> 0 \nDEFAULT PROFIT (" + str(defaultProfit) + ") -> HIT ENTER ")
print("----------------------------------")
profitLimit = int(input("MINIMUM PROFIT (gp) = ") or defaultProfit)
print("----------------------------------")
print("  [HOW OFTEN PRICES ARE UPDATED]")
#print("DEFAULT TIME (32s) -> HIT ENTER")
print("----------------------------------")
loadTime = int(input("UPDATE TIME (s) = ") or defaultLoadTime)

# set minium loadTime
if (loadTime < 4):
    loadTime = 1
else:
    loadTime = floor(loadTime / 4)
    
# scrape all data from a url
def collect_all_data(url):
    result = requests.get(url, headers=headers, timeout=10)
    data = result.text  
    
    return data

# filter only price data from a textfile
def collect_html(data):
    # get all html
    htmlData = BeautifulSoup(data, "html.parser")
    data = str(htmlData)
    #write_data(data, "allData.txt")
    
    return data

def create_item_list(itemData):
     # find all relevant html data
    itemList = re.findall(r'(?<=ROI)(.*?)(?=NOT)', itemData, flags=re.MULTILINE|re.DOTALL)
    
    itemList = re.findall(r'(?<=title)(.*?)(?=%)', str(itemList), flags=re.MULTILINE|re.DOTALL)
    
    itemTitles = re.findall(r'(?<=title=")(.*?)(?=")', str(itemList), flags=re.MULTILINE|re.DOTALL)
    
    itemPrices = re.findall(r'(?<=class=")(.*?)(?=</span)', str(itemList), flags=re.MULTILINE|re.DOTALL)
    
    # counter to get every 4th value in loop
    i = 0
    newPrices = []
    for price in itemPrices:
        i += 1
        if (i % 4 == 0):
            newPrices.append(price)
            
    itemPrices.clear
    itemPrices = newPrices
    itemPrices[len(itemPrices)-1] = itemPrices[len(itemPrices)-1] + "coins"
    itemPrices = str(itemPrices).replace("', '", "")
    
    itemPrices = re.findall(r'(?<=>)(.*?)(?=coins)', str(itemPrices), flags=re.MULTILINE|re.DOTALL)
    
    items = []
    for i in range(len(itemTitles)):
        items.append((itemTitles[i], itemPrices[i]))
    
    #write_data(itemTitles, "itemTitles.txt")
    #write_data(itemPrices, "itemPrices.txt")
    #write_data(itemList, "itemList.txt")
    
    return items

def check_target_price(items):
    i = 0
    indexList = []
    for price in items:
        if (int(str(price[1])) >= profitLimit):
            indexList.append(i)
        i += 1
    
    valuableItems = []
    i = 0
    for index in indexList:
        valuableItems.append(items[index][0] + " -> " + items[index][1])  
        
    #write_data(valuableItems, "valuableItems.txt")
    
    return valuableItems

# write data to a text file
def write_data(data, filename):
    file = open(filename, "w", encoding="utf-8")
    # write either an entire string or a list of strings to a text file
    if type(data) == str:
        file.write(data)
    elif type(data) == list:
        for elem in data:
            file.write(elem)
            file.write("\n")
            
    file.close()

def sort_valuable_items(valuableItems):
    sortedList = []
    for item in valuableItems:
        sortedList.append(re.sub(r'^.*?-> ', '', item))
    
    for i in range(len(sortedList)):
        for i in range(len(sortedList)-1):
            if (int(sortedList[i]) < int(sortedList[i+1])):
                temp = sortedList[i+1]
                sortedList[i+1] = sortedList[i]
                sortedList[i] = temp
                
                temp = valuableItems[i+1]
                valuableItems[i+1] = valuableItems[i]
                valuableItems[i] = temp
    
    return sortedList

# Decrease terminal size
cmd = 'mode 26,24'
os.system(cmd)

# Find items with best profit
data = collect_all_data(url)
data = collect_html(data)
items = create_item_list(data)
valuableItems = check_target_price(items)
sortedValuableItems = sort_valuable_items(valuableItems)

while True:
    # Show load
    for cycle in range(loadTime):
        for pos in "|/-\\":
            os.system('cls')
            print("Profits @ " + str(profitLimit))
            print("--------------------------")
            for items in valuableItems:
                print(" " + str(items))
            print("--------------------------")
            print("")
            print("Checking " + str(pos))
            print("")
            print("CTRL + C to EXIT")
            sleep(pauseLength)
            
    os.system('cls') 
    
    # Find items with best profit
    data = collect_all_data(url)
    data = collect_html(data)
    items = create_item_list(data)
    valuableItems = check_target_price(items)
    sortedValuableItems = sort_valuable_items(valuableItems)