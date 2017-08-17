from flask import Flask
from searchPTT_object import *
import time
app = Flask(__name__)


@app.route('/query/<ID>')
def print_result(ID):
    start_time = time.time()
    content,link_data = crawler_content_improve(google_custom_search_crawler(ID,5,1))
    all_list = analysis_content_improve(content,ID)
    n = '</br>'
    result = ''
    for i in range(0,len(all_list)):
        result = result+n+n+n+link_data[i]+n
        for now in all_list[i]:
            result = result + now + n
    end_time = time.time()
    spend_time = end_time -start_time
    print(spend_time)
    return result

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=4769)
