from flask import render_template,request,redirect,session,flash
from flask_app import app
from flask_app.models.historial import Historia
from flask_app.models.mascota import Mascota
from flask_app.models.vet import Vet

@app.route("/new/historial/<int:id>")
def new_historial(id):
    if 'veterinario_id' not in session:
        return redirect('/')
    
    data = {
        "id": id
    }
    
    mascota = Mascota.get_by_id(data)
    
    historial = Historia.get_all()
    
    return render_template('historial.html',mascota=mascota,historial=historial)

@app.route("/create/historial",methods=['POST'])
def create_historial():
    if 'veterinario_id' not in session:
        return redirect('/')
    
    Historia.savehistorial(request.form)
    return redirect('/dashboard') 


