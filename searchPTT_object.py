import json
import requests
from googleapiclient.discovery import build
import time


def google_custom_search_crawler(query_ID,one_query_num,page_limit):

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
    q ="&q="+query_ID
    cse_tok = "&cse_tok=ahl74mxjun1-rdpgntn7igqyvwtn:1502359101089"
    sort = "&sort=date"   #sort by 

    for npage in range(0,page_limit):

        temp =requests.get(query_url+ key+results_num+language+Print+source+sig+start+str(result_index)+cx+q+cse_tok+sort)
        response.append(temp.text)
        result_index = result_index +one_query_num
    
    for page in range(0,page_limit): #take every data of  page from response

        page_data = response[page] 
        page_data_dict = eval(page_data)
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


def crawler_content_improve(link_data): #path should rename content_link

    start_time = time.time()
    content = [] 

    for link in link_data:
        payload = {"from":  link , "yes": "yes"}
        start_requests = time.time()
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


def analysis_content_improve(content_list,query_ID):

    start_time = time.time()
    all_list = []
    ID_push_time = None

    title_index_start ='<span class="article-meta-tag">標題</span><span class="article-meta-value">' 
    title_index_end = "</span>"

    ip_index_start='<span class="f2">※ 發信站: 批踢踢實業坊(ptt.cc), 來自: ' 
    ip_index_end='</span>' 

    date_index_start ='時間</span><span class="article-meta-value">'
    date_index_end = '</span></div>'

    board_index_start ='看板</span><span class="article-meta-value">'
    board_index_end = '</span></div>'

    author_index_start = '作者</span><span class="article-meta-value">'
    author_index_end =" "

    push_mark_index_start = 'push-tag">'
    push_mark_index_end = '</span><span class="f3 hl push-userid">'

    push_ID_index_start = '</span><span class="f3 hl push-userid">'
    push_ID_index_end = '</span><span class="f3 push-content">'

    push_index_start = push_ID_index_end
    push_index_end = '</span>' 
    
    push_time_index_start ='<span class="push-ipdatetime">'
    push_time_index_end = '</span>' 

       
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
                
                while(push_ID != query_ID):    

                    push_ID_start = content.index(push_ID_index_start,push_ID_end) +len(push_ID_index_start)
                    push_ID_end = content.index(push_ID_index_end,push_ID_start)
                    push_ID = content[push_ID_start:push_ID_end].strip()


                push_mark_start = content.rindex(push_mark_index_start,0,push_ID_start) +len(push_mark_index_start)
                push_mark_end = content.index(push_mark_index_end,push_mark_start)
                push_mark = content[push_mark_start:push_mark_end]



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

            
            if query_ID == author:
                temp_list.append('post')
            else:
                temp_list.append(ID_push_content)
            
        all_list.append(temp_list)

    end_time =time.time()
    time_cost=end_time-start_time
    print("analysis:",time_cost)
    
    return all_list

def test_analysis_improve():

    n = '\n'
    test_link = ['http://www.ptt.cc/bbs/PC_Shopping/M.1488717900.A.525.html']
    ID = "heaviest"
    content,link_data = crawler_content_improve(google_custom_search_crawler(ID,10,20))
    all_list = analysis_content_improve(content,ID)
    f = open("./test.log",'w')

    for i  in range (0,len(all_list)):

        f.write(n+n+n)
        f.write(link_data[i]+n)

        for now in all_list[i]:

            f.write(now)
            f.write(n)

'''
start_time = time.time()

test_analysis_improve()

end_time = time.time()
time_cost=end_time-start_time

print("sum:",time_cost)

'''

class PTT_ID_searcher(object):
    
    def __init__(self,queryID,queryNum):
    #queryNum is how many reuslt which one query
        self.__queryID = queryID
        self.__queryNum =  queryNum
    
    #use google custom search to get link
    def google_crawler(self,page):
    # page which you want to locate

        start_time = time.time()
        link_data=[]
   
        query_url = "https://www.googleapis.com/customsearch/v1element?"
        key = "key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY"
        rsz ="&rsz=filtered_cse" #no use
        results_num = "&num="+str(self.__queryNum)
        language = "&hl=zh_TW"
        Print = "&prettyPrint=true"
        source = "&source=gcsc&gss=.com"
        sig = "&sig=01d3e4019d02927b30f1da06094837dc"
        start ="&start="# +str(result_index)
        cx="&cx=013003672663057511130:ewkefht62rk"
        q ="&q="+self.__queryID
        cse_tok = "&cse_tok=ahl74mxjun1-rdpgntn7igqyvwtn:1502359101089"
        sort = "&sort=date"   #sort by 


        temp =requests.get(query_url+ key+results_num+language+Print+source+sig+start+str(page)+cx+q+cse_tok+sort)
        response = temp.text
    
     #take every data of  page from response

        page_data = response
        page_data_dict = eval(page_data)
        try:
            query_data = page_data_dict['results'] # take value of key:item

            for each_data in query_data: #take value of key:link
                link_data.append(each_data["unescapedUrl"])

        except KeyError:
            print("have error")

        end_time = time.time()
        time_cost = end_time - start_time
        print("custom:",time_cost)

        return link_data #link_data type is list

    def content_crawler(self,link):
    #type of link is  string!
        start_time = time.time()
    

        
        payload = {"from":  link , "yes": "yes"}
        start_requests = time.time()
        VERIFY = True
        res = requests.get(url=link, cookies={'over18': '1'}, verify=VERIFY)      
        end_requests = time.time()
        time_request = end_requests - start_requests
        print("requsets:",time_request)
        res.encoding = 'usf8'
        content = res.text

        end_time = time.time()
        time_cost = end_time - start_time
        print("crawler_content:",time_cost)

        return content #type of content is string!

class content_analyst(object):
    def __init__(self,content,queryID): 
        self.__content = content
        self.__queryID = queryID

    def title(self):

        content = self.__content

        title_start =0
        title_end = 0

        title_index_start ='<span class="article-meta-tag">標題</span><span class="article-meta-value">' 
        title_index_end = "</span>"

        try:            
            title_start = content.index(title_index_start,title_end) + len(title_index_start)
            title_end = content.index(title_index_end,title_start)
            title =  content[title_start:title_end]       
        except ValueError:  
            title = None
            
        return title       
    
    def ip(self):
        
        content = self.__content

        ip_start = 0
        ip_end = 0

        ip_index_start='<span class="f2">※ 發信站: 批踢踢實業坊(ptt.cc), 來自: ' 
        ip_index_end='</span>' 

        try:
            ip_start = content.index(ip_index_start,ip_end)+len(ip_index_start)
            ip_end = content.index(ip_index_end,ip_start)
            ip = content[ip_start:ip_end].strip('\n')
        except ValueError:
            ip = None
        
        return ip

    def date(self):

        content = self.__content

        date_start = 0
        date_end = 0

        date_index_start ='時間</span><span class="article-meta-value">'
        date_index_end = '</span></div>'

        try:
            date_start = content.index(date_index_start,date_end)+len(date_index_start)
            date_end = content.index(date_index_end,date_start)
            date = content[date_start:date_end]

        except ValueError:
            date = None

        return date 

    def board(self):
        
        content = self.__content

        board_start =0
        board_end = 0

        board_index_start ='看板</span><span class="article-meta-value">'
        board_index_end = '</span></div>'
    
        try:
            board_start=content.index(board_index_start,board_end)+len(board_index_start)
            board_end = content.index(board_index_end,board_start)
            board = content[board_start:board_end]
        except ValueError:
            board = None

        return board 

    def author(self):
    
        content = self.__content

        author_start = 0
        author_end = 0

        author_index_start = '作者</span><span class="article-meta-value">'
        author_index_end =" "

        try:
            author_start = content.index(author_index_start,author_end)+len(author_index_start)
            author_end = content.index(author_index_end,author_start)
            author = content[author_start:author_end]
        except ValueError:
            author = None
    
        return author
    
    def push(self):

        content = self.__content
        ID =  self.__queryID

        push_mark_start=0
        push_mark_end=0
        push_start=0
        push_end=0     
        push_time_start =0
        push_time_end = 0
        push_ID_start = 0
        push_ID_end = 0        

        push_mark = None
 
        ID_push_content_list = []

        push_mark_index_start = 'push-tag">'
        push_mark_index_end = '</span><span class="f3 hl push-userid">'

        push_ID_index_start = '</span><span class="f3 hl push-userid">'
        push_ID_index_end = '</span><span class="f3 push-content">'

        push_index_start = push_ID_index_end
        push_index_end = '</span>' 
    
        push_time_index_start ='<span class="push-ipdatetime">'
        push_time_index_end = '</span>'

        exception = False

        while exception != True:
            
            try:
                push_ID = None
                while(push_ID != ID):    

                    push_ID_start = content.index(push_ID_index_start,push_ID_end) +len(push_ID_index_start)
                    push_ID_end = content.index(push_ID_index_end,push_ID_start)
                    push_ID = content[push_ID_start:push_ID_end].strip()


                push_mark_start = content.rindex(push_mark_index_start,0,push_ID_start) +len(push_mark_index_start)
                push_mark_end = content.index(push_mark_index_end,push_mark_start)
                push_mark = content[push_mark_start:push_mark_end]


                push_start = content.index(push_index_start,push_ID_end)
                push_start = push_start + len(push_index_start)
                push_end = content.index(push_index_end,push_start)
                push = content[push_start:push_end].strip("\n")

                push_time_start = content.index(push_time_index_start,push_end) + len(push_time_index_start)
                push_time_end = content.index(push_time_index_end,push_time_start)
                push_time = content[push_time_start:push_time_end]

    
                ID_push_content =push_mark+ push_ID +push+push_time
            except ValueError:
                exception = True
                ID_push_content = None
            
            ID_push_content_list.append(ID_push_content)

        return ID_push_content_list

    #the post of content
    def post_content(self,date): 
    #date must be str!    
        content = self.__content
      
        post_content_start = 0
        post_content_end = 0

        try:
            post_content_index_start = date +'</span></div>' 
            post_content_index_end = '<span class="f2">'

        
        
            post_content_start = content.index(post_content_index_start)+len(post_content_index_start)
            post_content_end = content.index(post_content_index_end,post_content_start)
            post_content = content[post_content_start:post_content_end]

        except ValueError:
            post_content = None
        except TypeError:
            post_content = None

        return post_content
               

def test(ID,queryNum,page):
    PTT = PTT_ID_searcher(ID,int(queryNum))
    
    link_data = PTT.google_crawler(int(page))
    
    for link in link_data:
        print(link)
        content = PTT.content_crawler(link)
        analyst = content_analyst(content,ID)
        title = analyst.title()
        ip = analyst.ip()
        board = analyst.board()
        author = analyst.author()
        date = analyst.date()
        ID_push = analyst.push()
        post_content = analyst.post_content(date)
    #    print(title,ip,board,author)
        print(post_content)
test('heaviest',10,1)


'''
ID = input("search_ID:")
query_num = input("query_num:")
page = input("page:")

'''
