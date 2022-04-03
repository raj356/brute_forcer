import requests
import sys
import random
import os
import time
import threading

inputfile = str()
inputurl = str()
errors_list = list()
list_of_words = list()
total_threads=list()
response_recvd = dict()

def BruteForce(site):
    global inputfile
    global inputurl
    global errors_list
    global list_of_words
    global total_threads 
    global response_recvd

    try:
        resp = requests.get(site)
        response_recvd[site] = int(resp.status_code)
    
    except:
        print("Not found: " + site)
        response_recvd[site] = 404


def formation():
    try:
        global inputfile
        global inputurl
        global errors_list
        global list_of_words
        global total_threads

        inputfile = sys.argv[1]
        inputurl = sys.argv[2]

        for i in range(4, len(sys.argv)):
            errors_list.append(int(sys.argv[i]))
        
        if (os.path.isfile(inputfile) == False):
            print("Check the file name")
        
        else:
            list_of_words = open(inputfile,'r').readlines()

        for i in range(len(list_of_words)):
            list_of_words[i] = list_of_words[i].strip()    

    except IndexError:
        print("Check CLI i/p")
        sys.exit()
    except Exception:
        print(Exception)
        sys.exit()

def create(inputurl,words):
    return "https://" + inputurl + "/" + words

def constructing_urls():
    global inputfile
    global inputurl
    global errors_list
    global list_of_words
    global total_threads
    global response_recvd

    const_url = []
    
    for words in list_of_words:
        const_url.append(create(inputurl,words))

    for url in const_url:
        total_threads.append(threading.Thread(target=BruteForce,args=(url,)))    

    for i in range(len(total_threads)):
        total_threads[i].start()

def result():
    global inputfile
    global inputurl
    global errors_list
    global list_of_words
    global total_threads 
    global response_recvd

    for i in range(len(total_threads)):
        total_threads[i].join()
    
    output_file = sys.argv[3]

    file = open(output_file,'w')

    print("Details of status codes")

    for code,resp in response_recvd.items():
        print(code+ "   Code :" + str(resp))
        if resp in errors_list:
            copy_to_out_file = code + " Code:" + str(resp) +"\n"
            file.write(copy_to_out_file)
        
    file.close()

if __name__ == "__main__":
    begin = time.time()
    formation()
    constructing_urls()
    result()
    print("Time taken in seconds %s" % (time.time() - begin))