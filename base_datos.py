import mysql.connector as mysql
from PIL import Image
import io

class BaseDatos:

    def __init__(self):
        self.cn = mysql.connect(user='root', password='',host='127.0.0.1',
        database='si')
        
    def listar_imagenes(self):
        cursor=self.cn.cursor()
        query=("SELECT * FROM images")
        cursor.execute(query)
        return cursor.fetchall()

    def insertar_imagen(self,num,imagen,fecha,hora):
        cursor=self.cn.cursor()
        add_imagen=("INSERT INTO images VALUES (%s,%s,%s,%s)")
        data=(num,imagen,fecha,hora)
        cursor.execute(add_imagen,data)
        self.cn.commit()
        cursor.close()
        print "se actualizo la BASE de DATOS"

    def numRow(self):
        cursor=self.cn.cursor()
        query=("SELECT count(*) FROM images")
        cursor.execute(query)
        return cursor.fetchall()
    
    def buscar(self,num):
        cursor=self.cn.cursor()
        query=("SELECT * FROM images WHERE id="+str(num))
        cursor.execute(query)
        return cursor.fetchall()
    
    def cerrar_bd(self):
        self.cn.close()

#db=BaseDatos()
#print db.buscar(2)[0][2]
#lista=db.listar_imagenes()
#img='try.jpg'
#image_blob=open(img,'rb').read()
#hora=time.strftime("%H:%M:%S")
#fecha=time.strftime("%d/%m/%y")
#db.insertar_imagen(image_blob,fecha,hora)

#lista=db.listar_imagenes()
#for data in lista:
#    image = Image.open(io.BytesIO(data[1]))
#    image.show()
#image_data = lista[0][1]
#image = Image.open(io.BytesIO(image_data))
#image.show()

