from flask import Flask
from searchPTT import *
app = Flask(__name__)


@app.route('/query/<ID>')
def print_result(ID):
 
    content,link_data = crawler_content_improve(google_custom_search_crawler(ID,3,4))
    all_list = analysis_content_improve(content,ID)
    n = '</br>'
    result = ''
    for i in range(0,len(all_list)):
        result = result+n+n+n+link_data[i]+n
        for now in all_list[i]:
            result = result + now + n
    return result

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=4769)
