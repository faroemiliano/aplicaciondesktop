# para hacer este pequeno proyecto fue utilizado las siguientes herramientas, Biblioteca tkinter (ya viene en python3), luego para guardar los 
# datos utilizaremos la base de datos SQLite3, y la interfaz a utilizar para manipular la base de datos tendremos que instalar "DB BROWSER FOR SQLite "

from tkinter import ttk
from tkinter import *

import sqlite3 #este modulo aqui no es la base de datos, es solo un modulo para coneccion 

class Product:

    db_name = "database.db"

    def __init__(self, window):
        self.wind = window
        self.wind.title("Aplicacion de productos")

#crear un contenedor utilizando labelFrame
        frame = LabelFrame(self.wind, text= "Registrar nuevo producto")
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        Label(frame, text='Nombre: ').grid(row=1, column=0)
        self.nombre = (Entry(frame))
        self.nombre.grid(row=1, column=1)
        self.nombre.focus()

        Label(frame, text='Precio: ').grid(row=2, column=0)
        self.precio = (Entry(frame))
        self.precio.grid(row=2, column=1)

        #crear un boton
        ttk.Button(frame, text='Guardar producto', command=self.add_product).grid(row=3, columnspan=2, sticky= W + E)

        #output messages

        self.message = Label(text='', fg='red')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        #crear tabla

        self.tree = ttk.Treeview(height=10, columns=2)
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading('#0', text='Nombre', anchor= CENTER)
        self.tree.heading('#1', text='Precio', anchor= CENTER)

        #buttons
        ttk.Button(text='Eliminar', command= self.delete_product).grid(row=5, column=0, sticky= W+E)
        ttk.Button(text='Editar', command= self.edit_product).grid(row=5, column=1, sticky= W+E)


        self.get_products()

    def ejecuta_consulta(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
         cursor = conn.cursor()
         result = cursor.execute(query, parameters)
         conn.commit()
        return result
    
    def get_products(self):
      #limoiando la tabla
      records = self.tree.get_children() #get children es para obtener todos los elementos de la tabla
      for element in records:
         self.tree.delete(element)
    #consultando los datos
      query = 'SELECT * FROM product ORDER BY name DESC'
      deb_rows = self.ejecuta_consulta(query)
      #rellenando los datos
      for row in deb_rows:
         self.tree.insert('', 0, text= row[1], values= row[2])

    #.gett, solo para agarrar la info del usuario
    def validatios(self):
     return len(self.nombre.get())!= 0 and len(self.precio.get())!= 0 
    

    def add_product(self):
       if self.validatios():
         query = 'INSERT INTO product VALUES(NULL, ?, ?)'
         parametros = (self.nombre.get(), self.precio.get())
         self.ejecuta_consulta(query, parametros)
         self.message['text'] = 'El producto {} se ha ingresado correctamente'.format(self.nombre.get())
         self.nombre.delete(0, END)
         self.precio.delete(0, END)
       else: 
         self.message['text'] = 'Ambos campos deben ser completados'
       self.get_products()

    def delete_product(self):
       self.message['text'] = ''
       try:
        self.tree.item(self.tree.selection())['text'][0]
       except IndexError as e:
          self.message['text'] = 'Por favor seleccionar un elemento'
          return
       name = self.tree.item(self.tree.selection())['text']
       query = 'DELETE FROM product WHERE name = ?' 
       self.ejecuta_consulta(query, (name,))
       self.message['text'] = 'El producto {} fue eliminado correctamente'.format(name)
       self.get_products()
         

    def edit_product(self):
       self.message['text'] = ''
       try:
        self.tree.item(self.tree.selection())['text'][0]
       except IndexError as e:
          self.message['text'] = 'Por favor seleccionar un elemento'
          return
       name = self.tree.item(self.tree.selection())['text']
       old_precio = self.tree.item(self.tree.selection())['values'][0]
       #TopLevel() crea una nueva ventana
       self.editWind = Toplevel()
       self.editWind.title = 'Editar producto'
         #buttons
       

       #old name
       Label(self.editWind, text='Nombre anterior').grid(row=0, column=1)
       Entry(self.editWind, textvariable= StringVar(self.editWind, value=name), state='readonly').grid(row=0, column=2)
       #old price
       Label(self.editWind, text='Precio anterior').grid(row=2, column=1)
       Entry(self.editWind, textvariable= StringVar(self.editWind, value=old_precio), state='readonly').grid(row=2, column=2)
       #new name
       Label(self.editWind, text='Nuevo nombre').grid(row=1, column=1)
       new_name= Entry(self.editWind)
       new_name.grid(row=1, column=2)
       #new price
       Label(self.editWind, text='Nuevo precio').grid(row=3, column=1)
       new_price= Entry(self.editWind)
       new_price.grid(row=3, column=2)
       

       Button(self.editWind, text='Editar', command= lambda: self.edit_records(new_name.get(), name, new_price.get(), old_precio)).grid(row=4, column=2, sticky= W + E)

    def edit_records(self, new_name, name, new_price, old_precio):
     
       query = 'UPDATE product SET name = ?, precio = ? WHERE name = ? AND precio = ?'
       parametros = (new_name, new_price, name, old_precio)
       self.ejecuta_consulta(query, parametros)
       self.editWind.destroy()
       self.message['text'] = 'El producto {} se ha editado correctamente'.format(name)
       self.get_products()
        
       
      

       
          
if __name__ == '__main__':
    window = Tk() #ejecuta Tk() y me devuelve la ventana al iniciar nuestra App
    application = Product(window)
    window.mainloop()