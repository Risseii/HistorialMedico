from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from .historial import Historia

class Mascota:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.type = data['type']
        self.age = data['age']
        self.gender = data['gender']
        self.breed = data['breed']
        self.birth_date = data['birth_date']
        self.weight = data['weight']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.veterinario_id = data["veterinario_id"] #Identifico al veterinario que atenderá a la mascota
        self.propietario = data["propietario"]
        
        self.historial = []
        self.image = data['image']
        
    @classmethod
    def save(cls,data):
        #data = {}
        query = "INSERT INTO mascotas (name,propietario,type,age,gender,breed,birth_date,weight,veterinario_id,image) VALUES (%(name)s,%(propietario)s,%(type)s,%(age)s,%(gender)s,%(breed)s,%(birth_date)s,%(weight)s,%(veterinario_id)s,%(image)s)" 
        result = connectToMySQL("projet").query_db(query,data)
        print(result)
        return result
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM mascotas WHERE id = %(id)s"
        return connectToMySQL('projet').query_db(query,data)
    
    @staticmethod
    def valida_mascota(formulario):
        es_valido = True
        if len(formulario['name']) < 3:
            flash("El name debe de tener al menos 3 caracteres",'mascota')
            es_valido = False
        
        if len(formulario['type']) < 3:
            flash("El tipo de la mascota debe de tener al menos 3 caracteres",'mascota')
            es_valido = False
        
        return es_valido
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM mascotas" #no necesita data xk no estoy interpolando
        results = connectToMySQL('projet').query_db(query)
        print(results)
        mascotas = []
        for r in results:
            mascotas.append(cls(r))
        return mascotas
        
    @classmethod
    def update(cls,data): #el id se encuentra en el edit
        query = "UPDATE mascotas SET name=%(name)s,propietario=%(propietario)s,type=%(type)s,age=%(age)s,gender=%(gender)s,breed=%(breed)s,birth_date = %(birth_date)s,weight = %(weight)s WHERE id = %(id)s"
        mascotas = connectToMySQL('projet').query_db(query,data)
        return mascotas
    
    @classmethod
    def get_by_id(cls,data): #nos regresa el usuario en base al id
        query = "SELECT * FROM mascotas WHERE id = %(id)s"
        result = connectToMySQL('projet').query_db(query,data)
        mascota = cls(result[0]) #como nos regresa todo, lo obligo a que me muestre uno
        print(mascota)
        return mascota

    #Obtener todos los atributos dell historial cuando haga match con el id de la mascota
    @classmethod
    def obtener_id(cls,data):
        query = "SELECT * FROM mascotas LEFT JOIN hmedicos ON mascotas.id= hmedicos.mascotas_id WHERE mascotas.id = %(id)s"
        results = connectToMySQL("projet").query_db(query,data)
        print(results)
        mascota = cls(results[0])
        
        for r in results:
            historial_data = {
                'id': r['hmedicos.id'],
                'tipo_v': r['tipo_v'],
                'date_v': r['date_v'],
                'producto_v': r['producto_v'],
                'producto_a': r['producto_a'],
                'date_a': r['date_a'],
                'producto_anti': r['producto_anti'],
                'date_anti': r['date_anti'],
                'diagnostico': r['diagnostico'],
                'date_diag': r['date_diag'],
                'medicamento': r['medicamento'],
                'cantidad': r['cantidad'],
                'frecuencia': r['frecuencia'],
                'duracion': r['duracion'],
                'instruction': r['instruction'],
                'mascotas_id': r['mascotas_id'],
            }
            
            final = Historia(historial_data)
            mascota.historial.append(final)
            
        return mascota
        
        
    
        

