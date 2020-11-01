from bs4 import BeautifulSoup            
import requests
import re
import os
import zipfile
import numpy as np
import csv
import io
from os import listdir
from os.path import isfile, join
import pickle
import gzip

columns = [
        'region',
        'p1',
        'p36',
        'p37',
        'p2a',
        'weekday(p2a)',
        'p2b',
        'p6',
        'p7',
        'p8',
        'p9',
        'p10',
        'p11',
        'p12',
        'p13a',
        'p13b',
        'p13c',
        'p14',
        'p15',
        'p16',
        'p17',
        'p18',
        'p19',
        'p20',
        'p21',
        'p22',
        'p23',
        'p24',
        'p27',
        'p28',
        'p34',
        'p35',
        'p39',
        'p44',
        'p45a',
        'p47',
        'p48a',
        'p49',
        'p50a',
        'p50b',
        'p51',
        'p52',
        'p53',
        'p55a',
        'p57',
        'p58',
        'a',
        'b',
        'd',
        'e',
        'f',
        'g',
        'h',
        'i',
        'j',
        'k',
        'l',
        'n',
        'o',
        'p',
        'q',
        'r',
        's',
        't',
        'p5a']

regionsDict = {'00': 'PHA', '01': 'STC', '02': 'JHC', '03': 'PLK', '04': 'ULK', '05': 'HKK', '06': 'JHM', 
               '07': 'MSK', '14': 'OLK', '15': 'ZLK', '16': 'VYS', '17': 'PAK', '18': 'LBK', '19': 'KVK'} 

def isFloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def getRegionID(val): 
    for key, value in regionsDict.items(): 
        if val == value: 
            return key 

class DataDownloader:
    #CLASS VARIABLES
    memory = {}
    fullLists = []

    def __init__(self, url='https://ehw.fit.vutbr.cz/izv/',folder='data', cache_filename='data_{}.pkl.gz'):
        self.url = url
        self.folder = folder
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        self.cache_filename = cache_filename

    def download_data(self): #this function downloads all .zip files from url https://ehw.fit.vutbr.cz/izv/
        headers = headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', 'Upgrade-Insecure-Requests': '1','DNT': '1','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language': 'en-US,en;q=0.5','Accept-Encoding': 'gzip, deflate'}
        html = requests.get(self.url, headers = headers) #add headers to simulate communication as browser (avoid script detector)
        soup = BeautifulSoup(html.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.endswith('.zip'):
                print(f'Downloading: {os.path.join(self.folder, href[5:])}')
                r = requests.get(self.url + href, stream=True)
                with open(os.path.join(self.folder, href[5:]), 'wb') as fd:
                    for chunk in r.iter_content(chunk_size=128):
                        fd.write(chunk)

    def parse_region_data(self, region):       
        regionID = getRegionID(region)

        lists = [[] for _ in range(65)] #initialize empty 64 lists (then converted to numpy arrays) maybe create new function for this because it must be called only one time
        toReturn = []                   #returned second list from tuple which will be filled with 65 numpy arrays (one numpy array for one value etc.)

        folders = [f for f in listdir(self.folder) if isfile(join(self.folder, f))]  #take all folders from self.folder/*
        self.download_if_not_exists(folders) #control if we got all files from url
        r = re.compile(r"^(datagis)((-rok-\d{4})|(\d{4})).zip$")   #regex for take only last year folders
        chosenFolders = list(filter(r.match, folders)) #taken last year folders for data comparison
        chosenFolders.append('datagis-09-2020.zip')    #add last month from 2020 #TODO NEED TO CHANGE THIS (if AOctober, then 10 month will be called etc.``)

        for folder in chosenFolders:                   #iterate through folders
            f = self.folder + '/' + folder             #specify path
            print(f)
            with zipfile.ZipFile(f) as zf:             #open zipfile
                with zf.open(f'{regionID}.csv', 'r') as infile: #read .csv from zipfile
                    print(f'{regionID}.csv')
                    reader = csv.reader(io.TextIOWrapper(infile, 'ISO 8859-2'), delimiter=';') #parse file and cut them with ; delimiter
                    for row in reader:              #iterate through every list (row)
                        for i in range(64):                     
                            if i in range(0,3) or i in range(4,47) or i in range(60,62) or i == 63 or i == 56:   #range where ints are
                                if row[i] == '' or (row[i].isnumeric() == False and row[i] != ''):
                                    lists[i].append(-1)   #insert -1 if value in row is invalid
                                    self.fullLists[i].append(-1)   #insert -1 if value in row is invalid
                                else:
                                    lists[i].append(row[i]) #add id to list for ids etc. [list(p1) -> p1 etc.]
                                    self.fullLists[i].append(row[i])
                            elif i in range(47,51):   #range where floats are                                         
                                row[i] = row[i].replace(',', '.')
                                if row[i] == '' or (isFloat(row[i]) == False and row[i] != ''):
                                    lists[i].append(-1)  #insert -1 if value in row is invalid
                                    self.fullLists[i].append(-1)
                                else:
                                    lists[i].append(row[i]) #add id to list for ids etc. [list(p1) -> p1 etc.]
                                    self.fullLists[i].append(row[i])
                            else:                   #if not range of ints or floats, then its string
                                lists[i].append(row[i]) #add id to list for ids etc. [list(p1) -> p1 etc.]
                                self.fullLists[i].append(row[i])
                        lists[64].append(f'{region}')   #append region column with code
                        self.fullLists[64].append(f'{region}')

        toReturn = self.createBigNumpy(lists)
        print("Columns", type(columns), len(columns))
        print("GetList", type(toReturn), type(toReturn[0]), len(toReturn), len(toReturn[0]))
        return (columns, toReturn)                    #return it as tuple

    def get_list(self, regions = None):
        self.fullLists = [[] for _ in range(65)]
        folders = [f for f in listdir(self.folder) if isfile(join(self.folder, f))]
        if regions:
            for region in regions:
                #if region in memory:
                if region in self.memory.keys():
                    returned = self.memory.get(region)[1]  #take only data and not headers 
                    #add data to final_list from dict(returned)
                    print("Loading from memory!")
                    for i in range(65):
                        self.fullLists[i] += returned[i].tolist() 
            
                #if region not in memory and cache is created
                    #read from cache file
                    #  filename = self.folder + "/" + self.cache_filename.replace("{}", f"{region}")
                    #  cachefile = gzip.open(filename, 'rb')
                    #  loadedCache = pickle.load(cachefile)
                    #  cachefile.close()
                    #add loadedCache to dict and then to fullLists
                elif self.cache_filename.replace("{}", f"{region}") in folders:
                    filename = self.folder + "/" + self.cache_filename.replace("{}", f"{region}")
                    cachefile = gzip.open(filename, 'rb')
                    loadedCache = pickle.load(cachefile)
                    cachefile.close()
                    #add to memory
                    self.memory.update({region: loadedCache})
                    print("Loading from cache!")
                    #add to fullLists from loadedCache
                    for i in range(65):
                        self.fullLists[i] += loadedCache[1][i].tolist() 
                #if region not in memory and cache is not created
                    #call parse_region_data for region
                    #create cache file
                    #add data to dict and then to fullLists
                else:
                    toCache = self.parse_region_data(region)
                    print(f"Zipping {region}")
                    #create cache
                    filename = self.folder + "/" + self.cache_filename.replace("{}", f"{region}")
                    f_in = gzip.open(filename, 'wb')
                    pickle.dump(toCache, f_in)
                    f_in.close()
                    #add to memory
                    print("Loading from XXX")
                    self.memory.update({region: toCache})
                    
        else:
            for region in regionsDict.values():
                #if region in memory:
                if region in self.memory.keys():
                    returned = self.memory.get(region)[1]  #take only data and not headers 
                    #add data to final_list from dict(returned)
                    print(f"Loading from memory! {region}")
                    for i in range(65):
                        self.fullLists[i] += returned[i].tolist() 
            
                #if region not in memory and cache is created
                    #read from cache file
                    #  filename = self.folder + "/" + self.cache_filename.replace("{}", f"{region}")
                    #  cachefile = gzip.open(filename, 'rb')
                    #  loadedCache = pickle.load(cachefile)
                    #  cachefile.close()
                    #add loadedCache to dict and then to fullLists
                elif self.cache_filename.replace("{}", f"{region}") in folders:
                    filename = self.folder + "/" + self.cache_filename.replace("{}", f"{region}")
                    cachefile = gzip.open(filename, 'rb')
                    loadedCache = pickle.load(cachefile)
                    cachefile.close()
                    #add to memory
                    self.memory.update({region: loadedCache})
                    print(f"Loading from cache! {region}")
                    #add to fullLists from loadedCache
                    for i in range(65):
                        self.fullLists[i] += loadedCache[1][i].tolist() 
                #if region not in memory and cache is not created
                    #call parse_region_data for region
                    #create cache file
                    #add data to dict and then to fullLists
                else:
                    toCache = self.parse_region_data(region)
                    print(f"Zipping {region}")
                    #create cache
                    filename = self.folder + "/" + self.cache_filename.replace("{}", f"{region}")
                    f_in = gzip.open(filename, 'wb')
                    pickle.dump(toCache, f_in)
                    f_in.close()
                    #add to memory
                    print("Loading from XXX")
                    self.memory.update({region: toCache})
        
        final_list = self.createBigNumpy(self.fullLists)
        print("Columns", type(columns), len(columns))
        print("GetList", type(final_list), type(final_list[0]), len(final_list), len(final_list[0]))
        return (columns, final_list)

    #optional functions
    '''
        function for redownload missing .zip files [06,08], [07 missing so it downloads it]
    '''
    def download_if_not_exists(self, folders):
        headers = headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', 'Upgrade-Insecure-Requests': '1','DNT': '1','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language': 'en-US,en;q=0.5','Accept-Encoding': 'gzip, deflate'}
        html = requests.get(self.url, headers = headers) #add headers to simulate communication as browser (avoid script detector)
        soup = BeautifulSoup(html.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.endswith('.zip'):
                if href[5:] not in folders:
                    print(f'Downloading: {os.path.join(self.folder, href[5:])}')
                    r = requests.get(self.url + href, stream=True)
                    with open(os.path.join(self.folder, href[5:]), 'wb') as fd:
                        for chunk in r.iter_content(chunk_size=128):
                            fd.write(chunk)

    def createBigNumpy(self, fullLists):  #this function converts list to numpy array
        toReturn = []
        for i in range(65):
            if i in range(0,3) or i in range(4,47) or i in range(60,62) or i == 63 or i == 56:
                toReturn.append(np.array(fullLists[i], dtype=int))     #convert those lists to numpy arrays with ints
            elif i in range(47,51):
                toReturn.append(np.array(fullLists[i], dtype=float))     #convert those lists to numpy arrays with floats
            else:
                toReturn.append(np.array(fullLists[i], dtype=str))        #convert those lists to numpy arrays with string
        return toReturn
