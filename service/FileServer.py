from flask import Flask, render_template, request
from flask_cors import CORS
import minio
from mysql.mysql  import Mysql
import json

mysqlHandle = Mysql('./configs/mysql.yml')
cursor = mysqlHandle.getCursor('filedb')


minioHandle = minio.Minio('192.168.0.55:9000','adminminio','adminminio',secure=False)

app = Flask(__name__)
CORS(app)


def fileFilter(fileName,suffixStr):
    suffixStr=suffixStr.replace(' ','')
    sufs = suffixStr.split('|')

    fileName = fileName.lower()
    for suf in sufs:
        if fileName.endswith(suf.lower()):
            return True
    return False

@app.route("/imgList",methods=["POST"])
def imgList():
   
    data = request.data.decode("utf-8")
    
    print(data)

    form = json.loads(data)

    id = form['parentId']
    # bucketName = 'picture'
    # imgs = minioHandle.list_objects(bucketName,'/saigao/私定1万：性感套套牛奶主题丁字裤/')

    sql =  'select * from images WHERE parent_id = '+id

    # print(sql)
    
    cursor.execute(sql)

    imgs = cursor.fetchall()
    # print(imgs)
    srcList = []
    for img in imgs:
        if fileFilter(img['title'],'jpg|png|jpeg|bmp') :
            srcList.append({
                'url':img['rel_path'],
                'is_dir':False,
                'title':img['title']

            })
        # else:
        #     srcList.append({
        #         'url':img['rel_path'],
        #         'is_dir':True,
        #         'title':img['title']
        #     })

    sql =  'select * from dirs WHERE parent_id = '+id
    cursor.execute(sql)
    dirs = cursor.fetchall()

    for dir in dirs:
        srcList.append({
        'url':dir['rel_path'],
        'is_dir':True,
        'title':dir['title'],
        'id':str(dir['id'])
         })
    return  srcList



@app.route("/videoList",methods=["POST"])
def videoList():

    data = request.data.decode("utf-8")

    bucketName = 'video'
    videos = minioHandle.list_objects(bucketName,'虎牙不染ASMR福利合集【1asmr.top】/')
    print(videos)
    videoList = []
    for img in videos:
        if fileFilter(img.object_name,'mp4') :
            videoList.append(bucketName+'/'+img.object_name)

    return  videoList


if __name__ == '__main__':
   # mysql =  Mysql("./configs/mysql.yml")
   # cursor =  mysql.getCursor('upmdb')
   app.run(debug=True,port=10086,host='192.168.0.36')