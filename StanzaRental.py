from lxml import html
from tempfile import NamedTemporaryFile
from random import *
from lxml.html import fromstring
from itertools import cycle
import shutil, csv, time, json, calendar, datetime, decimal, math, xlwt
import requests
import string
import pandas as pd
import numpy
import random
#from exceptions import ValueError
from time import sleep      
from _sqlite3 import Row

def Analyzer(price, seller, isbn, minb, maxb, target, at, st):
    #isbn = isbn.lstrip("0")
    #cost = 0
    #comp = 0
    minc = float(minb[0])
    maxc = float(maxb[0])
    targetc = float(target[0])
    #with open('Rental File.csv', 'rt') as k:
        #reader = csv.reader(k, delimiter =',')
        #for row in reader:
            #if isbn == row[9]:
            #   #print row[10]
            #    comp = row[10]
            #    if comp > cost:
            #        cost = comp
    #profit = ((cost-7)*.85)*.75
    rep2 = ","
    rep = "$"
    for k in rep:
        price = price.replace(k,"")
    for u in rep2:
        price = price.replace(u,"")
    split = price.split()
    split = map(float, split)
    selsplit = seller.split(':')
    #print selsplit
    #print split
    #if len(selsplit) > len(split):
        #del selsplit[1]
    #print selsplit
    #print split
    amazon = 0
    stanza = targetc
    if st == 1:
        try:
            index = selsplit.index(' STANZA')
        except:
            index = selsplit.index('STANZA')
        stanza = split[index]
    if at == 1:
        try:
            index = selsplit.index(' Amazon Warehouse')
        except:
            index = selsplit.index('Amazon Warehouse')
        amazon = split[index]
    #print index
    owo = 0
    for loc in reversed(split):
        if stanza > loc and loc > minc and owo < 3 and not stanza == loc: #and not loc == amazon:
            stanza = loc - .04
        if owo >= 2 and loc > stanza:
            stanza = loc - .04
                #print "incoming: " and owo
                #print "saved: " and stanza
                #print "difference: " and (stanza - owo)
        if loc > stanza:
            owo = owo + 1   
        if loc < minc:
            stanza = minc
    if stanza > maxc:
        stanza = maxc
    if stanza < minc:
        stanza = minc
    print stanza
    return stanza

def Time():
    ts = datetime.datetime.now()
    return ts

def Deposit(isbn, ideal):
    #isbn = isbn.lstrip("0")
    tempfile = NamedTemporaryFile(mode='wb', delete=False)
    fields = ['SKU', 'Standard Price', 'StartDate', 'EndDate', 'R1', 'R2','R3','R4','Stock','ISBN', 'Min','Max','Target','Notes']
    with open('Rental File.csv', 'rb') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            if row['ISBN'] == isbn:
                row['R1'], row['R2'], row['R3'] = round(ideal,2), round(ideal,2), round(ideal/2, 2)
            row = {'SKU': row['SKU'], 'Standard Price': row['Standard Price'], 'StartDate': row['StartDate'], 'EndDate': row['EndDate'],'R1': row['R1'], 'R2': row['R2'],'R3': row['R3'], 'R4': row['R4'], 'Stock': row['Stock'], 'ISBN': row['ISBN'], 'Min': row['Min'], 'Max': row['Max'], 'Target': row['Target'], 'Notes': row['Notes']}
            writer.writerow(row)
    shutil.move(tempfile.name, 'Rental File.csv')
    tempfile.close()
    #df = pd.read_csv('Rental File.csv')
    #df.loc[df.ISBN == isbn, 'Rental_1'].replace(ideal)
    #df.loc[df.ISBN == isbn, 'Rental_2'].replace(ideal)
    #df.loc[df.ISBN == isbn, 'Rental_3'].replace(round(ideal/2, 2))
    #df.to_csv('Rental File.csv')

#def get_proxies():
    #url = 'https://free-proxy-list.net/'
    #response = requests.get(url)
    #parser = fromstring(response.text)
    #proxies = set()
    #for i in parser.xpath('//tbody/tr')[:10]:
        #if i.xpath('.//td[7][contains(text(),"yes")]'):
            #proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            #proxies.add(proxy)
    #return proxies
                

def AmzonParser(url, ISBN):
    ru = None
    user_agent_list = [
   #Chrome
        'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        #Firefox
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
        #internet explore
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko'
        #AOL
        'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.21; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
        'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; GTB7.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
        'Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
        'Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)'
        
    ]
    #proxies = ['121.129.127.209:80', '124.41.215.238:45169', '185.93.3.123:8080', '194.182.64.67:3128', '106.0.38.174:8080', '163.172.175.210:3128', '13.92.196.150:8080']
    #proxy = random.choice(proxies)
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    #page = requests.get(url, headers=headers, proxies={"http": proxy, "https": proxy})
    page = requests.get(url, headers=headers)
    while page.status_code != 200:
        #print ValueError('capcha')
        print page.status_code
        with open("error_log.txt", "a") as text_file:
            text_file.write(str(page.status_code) + " " + str(ISBN) + " " + user_agent + "\n")
        text_file.close()
        print ("failed")
        sleep(8)
        #proxy = random.choice(proxies)
        user_a = random.choice(user_agent_list)
        headers = {'User-Agent': user_a}
        #page = requests.get(url, headers=headers, proxies={"http": proxy, "https": proxy}) 
        page = requests.get(url, headers=headers)     
    while True:
        sleep(randint(2,4))
        doc = html.fromstring(page.content)
        #XPATH_NAME = '//h1/text()'
        XPATH_PRICE = '//span[@class="a-size-large a-color-price olpOfferPrice a-text-bold"]/text()'
        XPATH_SELLER = '//a[contains(@href,"merch_name")]/text()'
        XPATH_AMAZON = '//img[contains(@alt,"Amazon Warehouse")]/@alt'

        #RAW_NAME = doc.xpath(XPATH_NAME)
        RAW_PRICE = doc.xpath(XPATH_PRICE)
        RAW_SELLER = doc.xpath(XPATH_SELLER)
        RAW_AMAZON = doc.xpath(XPATH_AMAZON)
                
        #NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
        PRICE = ' '.join(''.join(RAW_PRICE).split())
        SELLER = ': '.join(RAW_SELLER)
        AMAZON = RAW_AMAZON
        df = pd.read_csv('Rental File.csv', converters={i: str for i in range(9000)})
        df1 = df[df['ISBN'] == ISBN]
        mina = df1.Min.values
        maxa = df1.Max.values
        target = df1.Target.values
        #df.info()
        acount = 0
        scount = 0
        
        if AMAZON:
            SELLER = "Amazon Warehouse: " + SELLER
            acount = 1
        if "STANZA" in SELLER:
            scount = 1
        #if "Cengage Learning, Inc." in SELLER:
            #print("1")
            #SELLER.replace("Cengage Learning, Inc.", "Cengage Learning Inc")
            #print SELLER
        if SELLER:
            ru =Analyzer(PRICE, SELLER, ISBN, mina, maxa, target, acount, scount)
            Deposit(ISBN, ru)
            data = {
                # 'NAME': NAME,
                'SALE_PRICE': PRICE,
                'SELLER': SELLER,
                # 'URL': url,
                'ISBN': ISBN,
                'Projected': ru
            }
            return data
        if not SELLER:
            ru = float(maxa[0])
            Deposit(ISBN, ru)
            data = {
                # 'NAME': NAME,
                'SALE_PRICE': PRICE,
                'SELLER': SELLER,
                # 'URL': url,
                'ISBN': ISBN,
                'Projected': ru
            }
            return data
        return None

def WriteI():
    df = pd.read_csv('Rental File.csv', converters={'ISBN': lambda x: str(x)})
    #with open("test.txt", "w") as test:
        #for x in df['ISBN']:
            #test.write(str(df['ISBN']) + "\n")
        #test.close()
    df['ISBN'].to_csv('test.txt', header=None, index=None)
    #numpy.savetxt('test.txt', df['ISBN'], fmt='%d')
    print("ISBN list created")
    return None

def ReadAsin():
    AsinList=[]
    data = open("StanzaRental.csv", 'w')
    out = csv.writer(data)
    WriteI()
    filez = "test.txt"
    filep = open(filez,"r")
    for line in filep:
        AsinList.append(line)
        #print AsinList
    f = open('dataSR.json', 'w')
    for i in AsinList:
        extracted_data = []
        ISBN1 = i.rstrip()
        while not len(ISBN1) == 10:
            ISBN1 = "0" + ISBN1
        url = "https://www.amazon.com/gp/offer-listing/" +ISBN1 +"/ref=dp_olp_rentals?ie=UTF8&f_rental=true"
        print("Processing: " + url)
        x = AmzonParser(url,i.rstrip())
        if x != None:
            extracted_data.append(x)
            #print Time()
            #print extracted_data
            sleep(2)
            json.dump(extracted_data, f, indent=1)
            for ree in extracted_data:
                try:
                    out.writerow(ree.values())
                except:
                    out.writerow("unicode error")
    data.close()
    filep.close()
    f.close()
    
if __name__ == "__main__":
    ReadAsin()
    #Time()
print("Finished")


        
    