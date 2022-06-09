from flask import render_template,request,redirect,session,flash
from flask_app import app
from flask_app.models.vet import Vet
from flask_app.models.mascota import Mascota
from flask_app.models.historial import Historia

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/registrovet')
def registro():
    return render_template('registrov.html')

@app.route('/register',methods = ['POST'])
def register():
    print(request.form)
    if not Vet.valida_veterinario(request.form):
        return redirect('/registrovet')
    
    pwd = bcrypt.generate_password_hash(request.form['password'])
    
    formulario = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'place': request.form['place'],
        'cellphone': request.form['cellphone'],
        'email': request.form['email'],
        'password': pwd,
        'type_of_user':request.form['type_of_user']
    }
    
    id = Vet.save(formulario)
    session['veterinario_id'] = id #
    session['type_of_user'] = request.form['type_of_user']
    
    return redirect('/dashboard') #sin html porque es un redirect

@app.route('/login',methods = ['POST'])
def login():
    vet = Vet.get_by_email(request.form) 
    
    if not vet:
        flash("E-mail no encontrado",'login') #Si el correo no existe sale el mensaje
        return redirect('/')
    
    if not bcrypt.check_password_hash(vet.password,request.form['password']): #Se realiza un match del password ingresado y el encriptado
        flash("Password incorrecto",'login')
        return redirect('/')
    
    session['veterinario_id'] = vet.id
    session['type_of_user'] = vet.type_of_user
    
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'veterinario_id' not in session:
        return redirect('/')
    
    print(session['type_of_user'])
    
    data = {
        "id": session['veterinario_id']
    }
    vet = Vet.get_by_id(data)  #el veterinario que ha entrado a sesión
    
    mascota = Mascota.get_all() #Llamo de la clase Mascota todas los campos de mascota
    
    historial = Historia.get_all() #Llamo de la clase Historia todas los campos de historia, REVISAR
    
    if session['type_of_user'] == 0:
        return render_template('dashboard.html',vet=vet,mascota=mascota,historial=historial)
    else:
        return render_template('dashboard2.html',vet=vet,mascota=mascota,historial=historial)

@app.route('/show/historialmedico/<int:id>')
def mostrar_medico(id):
    data = {
        "id": id,
    }
    
    historiald = Mascota.obtener_id(data)
    mascota1 = Mascota.get_by_id(data) 
    return render_template('dashboard3.html', historiald = historiald,mascota1=mascota1)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
