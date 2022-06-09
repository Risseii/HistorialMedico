from crypt import methods
from flask import render_template,request,redirect,session,flash
from flask_app import app
from flask_app.models.vet import Vet
from flask_app.models.mascota import Mascota

#Para subir imagenes
from werkzeug.utils import secure_filename
import os

@app.route("/new/mascota")
def new_mascota():
    if 'veterinario_id' not in session:
        return redirect('/')
    
    data = {
        "id": session['veterinario_id']
    }
    
    vet = Vet.get_by_id(data) #Se realiza una instancia de vet
    
    return render_template('new.html',vet=vet)

@app.route("/create/mascota",methods=['POST'])
def create_mascota():
    if 'veterinario_id' not in session:
        return redirect('/')
    
    if not Mascota.valida_mascota(request.form): 
        return redirect('/new/mascota')
    
    #Para agregar imagenes
    if 'image' not in request.files:
        flash('Imagen no encontrada','mascota')
        return redirect('/new/mascota')
    
    image = request.files['image']
    #Comparo el nombre del archivo
    if image.filename == '':
        flash('Nombre de imagen vacio','mascota')
        return redirect('/new/mascota')
    
    nombre_imagen = secure_filename(image.filename)
    
    image.save(os.path.join(app.config['UPLOAD_FOLDER'],nombre_imagen))
    
    formulario = {
        "name" : request.form['name'],
        "propietario": request.form['propietario'],
        "type" : request.form['type'],
        "age" : request.form['age'],
        "gender": request.form['gender'],
        "breed": request.form['breed'],
        "birth_date": request.form['birth_date'],
        "weight": request.form['weight'],
        "veterinario_id": request.form['veterinario_id'],
        "image": nombre_imagen
    }
    
    Mascota.save(formulario)  #en save se guarda tmb el vterinario_id y la imagen
    return redirect('/dashboard')

# Editar mascota
@app.route("/edit/mascota/<int:id>")
def edit_mascota(id):
    if 'veterinario_id' not in session:
        return redirect('/')
    
    data = {
        "id": session['veterinario_id']
    }
    
    vet = Vet.get_by_id(data)
    
    data_mascota = {
        "id": id
    }
    
    mascota = Mascota.get_by_id(data_mascota) 
    return render_template('edit.html',vet=vet,mascota=mascota)

# Guardar el edit 
@app.route("/update/mascota",methods=['POST'])
def update_mascota():
    if 'veterinario_id' not in session:
        return redirect('/')
    
    if not Mascota.valida_mascota(request.form): 
        return redirect('/edit/mascota/'+request.form['id']) #se refiere al segundo id del edit - hidden
    
    Mascota.update(request.form)
    return redirect("/dashboard")
    
@app.route("/delete/mascota/<int:id>")
def delete_recipe(id):
    if 'veterinario_id' not in session:
        return redirect('/')
    
    data = {
        "id": id
    }
    
    Mascota.delete(data)
    return redirect("/dashboard")

