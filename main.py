from flask import Flask, render_template, request
import db, config

host = config.host

app = Flask(__name__)

@app.get("/tasks")
def web_get_tasks():
    tasks_list = []

    filter = request.args.get('filter')
    value = request.args.get('value')
    search = request.args.get('search')

    if (search != None):
        tasks_list = db.select_tasks_with_search(filter, value, search)
    elif (filter != None and value != None):
        tasks_list = db.select_tasks_with_filter(filter, value)
    else:
        tasks_list = db.select_all_tasks()

    tasks_json = []

    print(tasks_list)

    for task in tasks_list:
        t = {}
        t["task_title"] = task[1]
        t["task_category"] = task[2]
        t["task_description"] = task[3]
        t["task_cost"] = task[4]

        tasks_json.append(t)

    return tasks_json

@app.post("/tasks")
def web_add_tasks():
    tasks = request.get_json()
    return db.add_tasks(tasks)

@app.put("/tasks")
def web_update_tasks():
    data = request.get_json()
    updates = data["updates"]
    filters = data["filters"]
    return db.update_tasks(updates, filters)

@app.delete("/tasks")
def web_delete_tasks():
    filters = str(request.query_string, 'UTF-8').split("&")
    return db.delete_tasks(filters)

@app.route('/')
def index():
    activate = request.args.get("activate")
    return render_template('index.html', host=host, activate=activate)

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

