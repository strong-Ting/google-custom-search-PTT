from flask import render_template,request,jsonify
from app import app
from app import searchPTT_object

@app.route('/')
def index():   
    return render_template('search.html')

@app.route('/query', methods=['POST'])
def query():
    queryID = request.form['query']
    page = request.form['page']
    perPage = request.form['perPage']

    PTT = searchPTT_object
    crawl = PTT.PTT_ID_searcher(queryID,int(perPage))
    link_data = crawl.google_crawler(int(page))

    data = {}
    
    num = 0
    for link in link_data:
        content = crawl.content_crawler(link)
        analyst = PTT.content_analyst(content,queryID)
        perData = analyst.run()

        if perData:
            perData['link'] = link
            data[num] = perData
            num = num +1
        else:
            print('noooooooooo')
#    print(queryID,page,perPage)
    print (data) 
#    return jsonify({'data':data},{'page':page},{'num':len(data)})
    return jsonify({'data':data,'page':page,'num':len(data)})



