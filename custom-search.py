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

def google_custom_search_crawler(query,one_query_num,page_limit):
    start_time = time.time()
    result_index_limit = int(page_limit)*one_query_num
    result_index = 0
    response = []
    link_data=[]
   
    query_url = "https://www.googleapis.com/customsearch/v1element?"
    key = "key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY"
    rsz ="&rsz=filtered_cse" #no use
    results_num = "&num="+str(one_query_num)
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
        result_index = result_index +one_query_num
    
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
        start_requests = time.time()
        res = requests.post("https://www.ptt.cc/ask/over18",data=payload)
        end_requests = time.time()
        time_request = end_requests - start_requests
        print("requsets:",time_request)
        res.encoding = 'usf8'
        content.append(res.text)
    end_time = time.time()
    time_cost = end_time - start_time
    print("crawler_content:",time_cost)
    return content

def crawler_content_improve(link_data): #path should rename content_link
    start_time = time.time()
    content = [] 

    for link in link_data:
   #    link = '/' + link.strip("https//:www.ptt.cc")
        payload = {"from":  link , "yes": "yes"}
        start_requests = time.time()
   #     res = requests.post("https://www.ptt.cc/ask/over18",data=payload)
        VERIFY = True
        res = requests.get(url=link, cookies={'over18': '1'}, verify=VERIFY)      
        end_requests = time.time()
        time_request = end_requests - start_requests
        print("requsets:",time_request)
        res.encoding = 'usf8'
        content.append(res.text)
    end_time = time.time()
    time_cost = end_time - start_time
    print("crawler_content:",time_cost)
    return content,link_data

def analysis_content(content_list):
    start_time = time.time()
    title = []
    ip = []
    ID_content = []
    date = []
    board = []
    author = []
    ID_push = []
    ID_push_time = None
    ID = 'heaviest'

    title_index_start ='<span class="article-meta-tag">標題</span><span class="article-meta-value">' 
    title_index_end = "</span>"
    ip_index_start='<span class="f2">※ 發信站: 批踢踢實業坊(ptt.cc), 來自: ' 
    ip_index_end='</span>' 
    date_index_start ='時間</span><span class="article-meta-value">'
    date_index_end = '</span></div>'
    board_index_start ='看板</span><span class="article-meta-value">'
    board_index_end = '</span></div>'
    author_index_start = '作者</span><span class="article-meta-value">'
#    author_index_end ='</span></div>'
    author_index_end =" "
    push_mark_index_start = '<span class="f1 hl push-tag">'
    push_index_start ='</span><span class="f3 hl push-userid">'+ID+'</span><span class="f3 push-content">:'
    push_index_end = '</span>' 
    
    push_time_index_start ='<span class="push-ipdatetime">'
    push_time_index_end = '</span>' 
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
        date_start = 0
        date_end = 0
        board_start =0
        board_end =0
        author_start=0
        author_end =0
        push_mark_start=0
        push_mark_end=0
        push_start=0
        push_end=0     
        push_time_start =0
        push_time_end = 0

        ID_push_len = len(ID_push)
        exception = False
        while exception != True:
            try:
                title_start = content.index(title_index_start,title_end) + len(title_index_start)
                title_end = content.index(title_index_end,title_start)
                title.append(content[title_start:title_end])
                ip_start = content.index(ip_index_start,ip_end)+len(ip_index_start)
                ip_end = content.index(ip_index_end,ip_start)
                ip.append(content[ip_start:ip_end].strip('\n'))
                
                date_start = content.index(date_index_start,date_end)+len(date_index_start)
                date_end = content.index(date_index_end,date_start)
                date.append(content[date_start:date_end])
                
                board_start=content.index(board_index_start,board_end)+len(board_index_start)
                board_end = content.index(board_index_end,board_start)
                board.append(content[board_start:board_end])

                author_start = content.index(author_index_start,author_end)+len(author_index_start)
                author_end = content.index(author_index_end,author_start)
                author.append(content[author_start:author_end])

                push_time_start = content.index(push_time_index_start,push_time_end) + len(push_time_index_start)
                push_time_end = content.index(push_time_index_end,push_time_start)
                push_time = content[push_time_start:push_time_end]

                push_start = content.index(push_index_start,push_end)
                push_mark_end = push_start
                push_start = push_start + len(push_index_start)
                push_end = content.index(push_index_end,push_start)
                push_mark_start = push_mark_end -2
                
                ID_push_content =  content[push_mark_start:push_mark_end]+ID+":"+content[push_start:push_end]+'      '+push_time
     #           print(ID_push_content,type(push_start),push_end)
                ID_push.append(ID_push_content)
 #                print(content[title_start:title_end])
                

            except ValueError:
                exception = True
                if ID_push_len == len(ID_push):
                    ID_push.append("None")
            ID_push_content = ID_push[len(ID_push)-1]
            
            if ID == author[len(author)-1]:
                ID_content.append('post')
            elif ID_push_content == "None":
                ID_content.append('None')
            elif ID_push_content == ID_content[len(ID_content)-1]:
                pass
            else:
                ID_content.append(ID_push_content)
            
                        
    end_time =time.time()
    time_cost=end_time-start_time
    print("analysis:",time_cost)
    
    '''
    content = content_list[0]
    author_start = content.index(author_index_start,author_end)+len(author_index_start)
    author_end = content.index(author_index_end,author_start)
    
    print('eeeeeeeeeeeeeeeeeeeeeee')
    print(content[author_start:author_end])
    print('eeeeeeeeeeeeeeeeeeeeeee')
    '''

#    return title,len(title),ip,len(ip),ID_content,len(ID_content),date,len(date),board,len(board)

    return title,ip,author,ID_content,date,board,ID_push

def analysis_content_improve(content_list):
    start_time = time.time()
    all_list = []
    ID_push_time = None
    ID = 'heaviest'

    title_index_start ='<span class="article-meta-tag">標題</span><span class="article-meta-value">' 
    title_index_end = "</span>"
    ip_index_start='<span class="f2">※ 發信站: 批踢踢實業坊(ptt.cc), 來自: ' 
    ip_index_end='</span>' 
    date_index_start ='時間</span><span class="article-meta-value">'
    date_index_end = '</span></div>'
    board_index_start ='看板</span><span class="article-meta-value">'
    board_index_end = '</span></div>'
    author_index_start = '作者</span><span class="article-meta-value">'
#    author_index_end ='</span></div>'
    author_index_end =" "
    push_mark_index_start = 'push-tag">'
    push_mark_index_end = '</span><span class="f3 hl push-userid">'


    push_ID_index_start = '</span><span class="f3 hl push-userid">'
    push_ID_index_end = '</span><span class="f3 push-content">'

    push_index_start = push_ID_index_end
    push_index_end = '</span>' 
    
    push_time_index_start ='<span class="push-ipdatetime">'
    push_time_index_end = '</span>' 
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
        date_start = 0
        date_end = 0
        board_start =0
        board_end =0
        author_start=0
        author_end =0
        push_mark_start=0
        push_mark_end=0
        push_start=0
        push_end=0     
        push_time_start =0
        push_time_end = 0
        push_ID_start = 0
        push_ID_end = 0        

        push_mark = None
    
        temp_list = []    
        
        is_content = True
        try:
        
            title_start = content.index(title_index_start,title_end) + len(title_index_start)
            title_end = content.index(title_index_end,title_start)
            title =  content[title_start:title_end]               

            temp_list.append(title)
                
            ip_start = content.index(ip_index_start,ip_end)+len(ip_index_start)
            ip_end = content.index(ip_index_end,ip_start)
            ip = content[ip_start:ip_end].strip('\n')

            temp_list.append(ip)
               
                
            date_start = content.index(date_index_start,date_end)+len(date_index_start)
            date_end = content.index(date_index_end,date_start)
            date = content[date_start:date_end]

            temp_list.append(date)
                
            board_start=content.index(board_index_start,board_end)+len(board_index_start)
            board_end = content.index(board_index_end,board_start)
            board = content[board_start:board_end]
            temp_list.append(board)

            author_start = content.index(author_index_start,author_end)+len(author_index_start)
            author_end = content.index(author_index_end,author_start)
            author = content[author_start:author_end]
            temp_list.append(author)
        except ValueError:
            temp_list.append("not content")
            is_content = False

        if is_content:
            try:   #now only craw one push content
                push_ID = None
                
                while(push_ID != ID):    

                    push_ID_start = content.index(push_ID_index_start,push_ID_end) +len(push_ID_index_start)
                    push_ID_end = content.index(push_ID_index_end,push_ID_start)
                    push_ID = content[push_ID_start:push_ID_end].strip()


                push_mark_start = content.rindex(push_mark_index_start,0,push_ID_start) +len(push_mark_index_start)
                push_mark_end = content.index(push_mark_index_end,push_mark_start)
                push_mark = content[push_mark_start:push_mark_end]

                print('push_ID_site:',push_ID_start,push_ID_end)
                print("push_mark_site",push_mark_start,push_mark_end)


                push_start = content.index(push_index_start,push_ID_end)
                push_start = push_start + len(push_index_start)
                push_end = content.index(push_index_end,push_start)
                push = content[push_start:push_end].strip("\n")

                push_time_start = content.index(push_time_index_start,push_end) + len(push_time_index_start)
                push_time_end = content.index(push_time_index_end,push_time_start)
                push_time = content[push_time_start:push_time_end]

    
                ID_push_content =push_mark+ push_ID +push+push_time
                temp_list.append(ID_push_content)
 
            except ValueError:
                ID_push_content = "None"
                temp_list.append(ID_push_content)

            
            if ID == author:
                temp_list.append('post')
            else:
                temp_list.append(ID_push_content)
            
        all_list.append(temp_list)

    end_time =time.time()
    time_cost=end_time-start_time
    print("analysis:",time_cost)
    
    '''
    content = content_list[0]
    author_start = content.index(author_index_start,author_end)+len(author_index_start)
    author_end = content.index(author_index_end,author_start)
    
    print('eeeeeeeeeeeeeeeeeeeeeee')
    print(content[author_start:author_end])
    print('eeeeeeeeeeeeeeeeeeeeeee')
    '''

#    return title,len(title),ip,len(ip),ID_content,len(ID_content),date,len(date),board,len(board)
    return all_list



def test():
    n = '\n'
    content,link_data = crawler_content_improve(google_custom_search_crawler("heaviest",3,5))
    title,ip,author,ID_content,date,board,ID_push = analysis_content(content)
    f = open("./test.log",'w')
    for i in range(0,len(title)):
        write_down = title[i]+n+ip[i]+n+author[i]+n+ID_content[i]+n+date[i]+n+board[i]+n+ID_push[i]+n+link_data[i]+n+n+n
        f.write(write_down)
    len_write = str(len(title))+str(len(ip))+str(len(author))+str(len(ID_content))+str(len(date))+str(len(board))+str(len(ID_push))
    f.write(len_write)

def test_analysis_improve():
    n = '\n'
    test_link = ['http://www.ptt.cc/bbs/PC_Shopping/M.1488717900.A.525.html']
    content,link_data = crawler_content_improve(google_custom_search_crawler("heaviest",10,20))
    all_list = analysis_content_improve(content)
#    content,link_data= crawler_content_improve(test_link)
#    all_list = analysis_content_improve(content)
 #   print(all_list)
    f = open("./test.log",'w')
    for i  in range (0,len(all_list)):
        f.write(n+n+n)
        f.write(link_data[i]+n)
        for now in all_list[i]:
            f.write(now)
            f.write(n)



#f = open("./content.html","w")
#f.write(crawler_content(google_custom_search_crawler("heaviest",1)))
start_time = time.time()
#analysis_content(crawler_content_improve(google_custom_search_crawler("heaviest",10)))
#print(analysis_content(crawler_content_improve(google_custom_search_crawler("heaviest",1))))
#test()
test_analysis_improve()
end_time = time.time()
time_cost=end_time-start_time
print("sum:",time_cost)
