from flask import Flask, render_template, request
import db, config

host = config.host

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', host=host)

@app.get('/goods')
def goods():
    goodList = []

    filter = request.args.get('filter')
    value = request.args.get('value')
    search = request.args.get('search')

    print(filter)

    if (search != None):
        goodsList = db.selectSearch(filter, value, search)
    elif (filter != None and value != None):
        goodsList = db.selectWithFilter(filter, value)
    else:
        goodsList = db.selectAll()

    goodsJson = []

    for good in goodsList:
        g = {}
        g["id"] = good[0]
        g["name"] = good[1]
        g["price"] = good[2]
        g["description"] = good[3]
        g["type"] = good[4]
        g["img_link"] = good[5]
        goodsJson.append(g)

    return goodsJson

@app.post("/goods")
def addGoods():
    goods = request.get_json()
    return db.addGoods(goods)

@app.put("/goods")
def updateGoods():
    data = request.get_json()
    updates = data["updates"]
    filters = data["filters"]
    return db.updateGoods(updates, filters)

@app.delete("/goods")
def deleteGoods():
    filters = str(request.query_string, 'UTF-8').split("&")
    return db.deleteGoods(filters)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

