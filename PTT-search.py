from flask import Flask
from searchPTT_object import *
import time
app = Flask(__name__)


@app.route('/query/<ID>')
def print_result(ID):
    
    start_time = time.time()

    queryNum = 10
    page = 1

    PTT = PTT_ID_searcher(ID,int(queryNum))
    
    link_data = PTT.google_crawler(int(page))
    
    for link in link_data:
        print(link)
        content = PTT.content_crawler(link)
        analyst = content_analyst(content,ID)
        data_dict = analyst.run()

    end_time = time.time()
    run_time = end_time - start_time
    print(run_time)
 
    return str(data_dict)

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=4769)
