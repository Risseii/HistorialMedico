from flask_app.config.mysqlconnection import connectToMySQL

import re #importamos expresiones regulares

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

from flask import flash #para mostrar los mensajes de validacion

class Vet:
    def __init__(self,data): #reviso mi tabla sql y considero los mismos nombres
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.place = data['place']
        self.cellphone = data['cellphone']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        self.type_of_user = data['type_of_user']
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO veterinarios (first_name,last_name,place,cellphone,email,password,type_of_user) VALUES (%(first_name)s,%(last_name)s,%(place)s,%(cellphone)s,%(email)s,%(password)s,%(type_of_user)s)"
        result = connectToMySQL('projet').query_db(query,data)
        return result
    
    @staticmethod
    def valida_veterinario(user):
        es_valido = True

        if len(user['first_name']) < 3:
            flash("Nombre debe de tener al menos 3 caracteres",'registrov')
            es_valido = False
            
        if len(user['last_name']) < 2:
            flash("Apellido debe de tener al menos 2 caracteres",'registrov')
            es_valido = False
        
        if not EMAIL_REGEX.match(user['email']): #no aceptaria un email de esta forma: a.com
            flash('E-mail inválido','registrov')
            es_valido = False
            
        if len(user['password']) < 6:
            flash('Contraseña debe de tener al menos 6 caracteres','registrov')
            es_valido = False
            
        if user['password'] != user['confirm']:
            flash('Contraseñas no coinciden','registrov')
            es_valido = False
            
        #crear validacion para el celular 9 numeros
        if len(user['cellphone']) < 9 or len(user['cellphone']) > 9:
            flash('El celular debe de tener 9 digitos','registrov')
            es_valido = False
        
        if len(user['place']) == 0 and user['type_of_user'] == 0:
            flash('Falta registrar el lugar de trabajo','registrov')
            es_valido = False
        
        #consulta si ya existe ese correo
        query = "SELECT * FROM veterinarios WHERE email = %(email)s" 
        results = connectToMySQL('projet').query_db(query,user)  
        if len(results) >= 1:
            flash('E-mail registrado previamente','registrov')
            es_valido = False
        return es_valido
    
    @classmethod
    def get_by_id(cls,data): #nos regresa el usuario en base al id
        query = "SELECT * FROM veterinarios WHERE id = %(id)s"
        result = connectToMySQL('projet').query_db(query,data)
        vet = cls(result[0]) #como nos regresa todo, lo obligo a que me muestre uno
        print(vet)
        return vet
    
    @classmethod
    def get_by_email(cls,data): #nos regresa el usuario en base al email
        #La data seria algo como {"email: "" ,"password:" "12"}
        query = "SELECT * FROM veterinarios WHERE email = %(email)s"
        result = connectToMySQL('projet').query_db(query,data) 
        
        if len(result) < 1: #No hubo un registro
            return False
        else:
            vet = cls(result[0])
            return vet