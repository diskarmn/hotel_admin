import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, url_for, redirect, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")
client = MongoClient(MONGODB_URI)
db=client[DB_NAME]
# client = MongoClient(
#     "mongodb://diskarmn:Diska123@ac-sjiapka-shard-00-00.3lnlkgx.mongodb.net:27017,ac-sjiapka-shard-00-01.3lnlkgx.mongodb.net:27017,ac-sjiapka-shard-00-02.3lnlkgx.mongodb.net:27017/?ssl=true&replicaSet=atlas-vnije0-shard-0&authSource=admin&retryWrites=true&w=majority"
# )
# db = client.hotel


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/edit")
def edit():
    return render_template("edit.html")
@app.route('/tampiledit',methods=['GET'])
def tampiledit():
    semua=list(db.kamar.find({},{'_id':False}))
    return jsonify({'semua':semua})
@app.route("/remaining", methods=["GET"])
def remaining():
    room = list(db.remaining.find({}, {"_id": False}))
    return jsonify({"room": room})
@app.route('/updateremaining',methods=['POST'])
def updateremaining():
    regular=request.form['regular']
    diska=request.form['diska']
    special=request.form['special']
    db.remaining.update_one({}, {'$set': {
        'regular': int(regular),
        'diska': int(diska),
        'special': int(special)
    }})
    return jsonify({'pesan':'success update remaining room'})


@app.route('/statuschange',methods=['POST'])
def statuschange():
    nomor=request.form['no']

    status=request.form['status']
    db.kamar.update_one(
        {'no':int(nomor)},
        {'$set':{'status':status}})
    return jsonify({'pesan':'berhasil ubah status'})

@app.route('/tampil',methods=['GET'])
def tampil():
    semua=list(db.guest.find({},{'_id':False}))
    return jsonify({'semua':semua})

@app.route('/ci',methods=['POST'])
def ci():
    selesai=request.form['nomor']
    db.guest.update_one(
        {'num':int(selesai)},
        {'$set':{'status':'ci'}})
    return jsonify({'pesan':'berhasil check in'})

@app.route('/co',methods=['POST'])
def co():
    selesai=request.form['nomor2']
    db.guest.update_one(
        {'num':int(selesai)},
        {'$set':{'status':'co'}})
    return jsonify({'pesan':'berhasil check out'})

@app.route('/del',methods=['POST'])
def hapusdel():
    hapus=request.form['nomor3']
    db.guest.delete_one(
        {'num':int(hapus)})    
    return jsonify({'pesan':'berhasil menghapus pesanan'})
# @app.route('/tambahin',methods=['POST'])
# def tambahin():
#     satu=request.form['satu']
#     dua=request.form['dua']
#     nomor=db.kamar.count_documents({})
#     urutan=nomor + 1
#     data={'no':urutan,
#           'kamar':satu,
#           'status':dua}
#     db.kamar.insert_one(data)
#     return jsonify({'pesan':'ok'})
if __name__ == "__main__":
    app.run("0.0.0.0", port=5001, debug=True)