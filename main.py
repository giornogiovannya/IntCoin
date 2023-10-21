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

    if (search != None):
        print(123)
        goodsList = db.selectSearch(filter, value, search)
    elif (filter != None and value != None):
        print(456)
        goodsList = db.selectWithFilter(filter, value)
    else:
        print(789)
        goodsList = db.selectAll()

    goodsJson = []

    print(goodList)

    for good in goodsList:
        print(good)
        g = {}
        g["goods_hash"] = good[1]
        g["goods_category"] = good[2]
        g["goods_title"] = good[3]
        g["goods_description"] = good[4]
        g["goods_merch_size"] = good[5]
        g["goods_count"] = good[6]
        g["goods_cost"] = good[7]
        g["goods_photo"] = good[8]

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

