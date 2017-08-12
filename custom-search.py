import json
import requests
from googleapiclient.discovery import build
import time

def getService():
    service = build("customsearch", "v1",
            developerKey="AIzaSyCyEJRAuPmPp6zOxHe4kbBP1sUu2ldj0yI")

    return service

def google_custom_search_api(q,pageLimit):

    pageLimit = 1
    service = getService()
    startIndex = 1
    response = []
    link_data = []

    for nPage in range(0, pageLimit):
        print ("Reading page number:",nPage+1)
        response.append(service.cse().list(
#            q='heaviest', #Search words
            cx='013003672663057511130:ewkefht62rk',  #CSE Key
         #   lr='lang_pt', #Search language
            start=startIndex
        ).execute())

        startIndex = response[nPage].get("queries").get("nextPage")[0].get("startIndex")

    for page in range(0,pageLimit): #take every data of  page from response
        page_data = response[page] 
        query_data = page_data['items'] # take value of key:item 
        for each_data in query_data: #take value of key:link
            link_data.append(each_data['link'])
    return link_data

def google_custom_search_crawler(query,page_limit):
    start_time = time.time()

    result_index_limit = int(page_limit)*10
    result_index = 0
    response = []
    link_data=[]
   
    query_url = "https://www.googleapis.com/customsearch/v1element?"
    key = "key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY"
    rsz ="&rsz=filtered_cse" #no use
    results_num = "&num=10"
    language = "&hl=zh_TW"
    Print = "&prettyPrint=true"
    source = "&source=gcsc&gss=.com"
    sig = "&sig=01d3e4019d02927b30f1da06094837dc"
    start ="&start="# +str(result_index)
    cx="&cx=013003672663057511130:ewkefht62rk"
    q ="&q="+query
    cse_tok = "&cse_tok=ahl74mxjun1-rdpgntn7igqyvwtn:1502359101089"
    sort = "&sort=date"   #sort by 
    for npage in range(0,page_limit):
        temp =requests.get(query_url+ key+results_num+language+Print+source+sig+start+str(result_index)+cx+q+cse_tok+sort)
        response.append(temp.text)
        result_index = result_index +10     
    
    for page in range(0,page_limit): #take every data of  page from response
        page_data = response[page] 
        page_data_dict = eval(page_data)
#        print(page_data_dict)
        try:
            query_data = page_data_dict['results'] # take value of key:item

            for each_data in query_data: #take value of key:link
                link_data.append(each_data["unescapedUrl"])

        except KeyError:
            print("have error")
    end_time = time.time()
    time_cost = end_time - start_time
    print("custom:",time_cost)
    return link_data

def crawler_content(link_data): #path should rename content_link
    start_time = time.time()
    content = [] 

    for link in link_data:
        link = '/' + link.strip("https//:www.ptt.cc")
        payload = {"from":  link , "yes": "yes"}
        res = requests.post("https://www.ptt.cc/ask/over18",data=payload)
        res.encoding = 'usf8'
        content.append(res.text)
    end_time = time.time()
    time_cost = end_time - start_time
    print("crawler_content:",time_cost)
    return content

def analysis_content(content_list):
    start_time = time.time()
    title = []
    ip = []
    ID_content = []
    date = []
    board = []

    title_index_start ='<span class="article-meta-tag">標題</span><span class="article-meta-value">' 
    title_index_end = "</span>"
    ip_index_start='<span class="f2">※ 發信站: 批踢踢實業坊(ptt.cc), 來自: ' 
    ip_index_end='</span>' 
    ''' 
    title_end = 100000
    content = content_list[0]
    title_start = content.index(title_index_start,title_end) + len(title_index_start)
    title_end = content.index(title_index_end,title_start)
    print(content[title_start:title_end])
    '''     
        
    for content in content_list:
        title_end  = 0
        title_start = 0
        ip_start=0
        ip_end=0

        exception = False
        while exception != True:
            try:
                title_start = content.index(title_index_start,title_end) + len(title_index_start)
                title_end = content.index(title_index_end,title_start)
                ip_start = content.index(ip_index_start,ip_end)+len(ip_index_start)
                ip_end = content.index(ip_index_end,ip_start)
                ip.append(content[ip_start:ip_end].strip('\n'))
 #                print(content[title_start:title_end])
                title.append(content[title_start:title_end])
            except ValueError:
                exception = True
    end_time =time.time()
    time_cost=end_time-start_time
    print("analysis:",time_cost)
    return title,ip,ID_content,date,board


#f = open("./content.html","w")
#f.write(crawler_content(google_custom_search_crawler("heaviest",1)))
start_time = time.time()
analysis_content(crawler_content(google_custom_search_crawler("heaviest",10)))
#print(analysis_content(crawler_content(google_custom_search_crawler("heaviest",1))))
end_time = time.time()
time_cost=end_time-start_time
print("sum:",time_cost)
