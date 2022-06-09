from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Historia:
    def __init__(self,data):
        self.id = data['id'],
        
        self.tipo_v = data['tipo_v'],
        self.date_v = data['date_v'],
        self.producto_v = data['producto_v'],
        self.producto_a = data['producto_a'],
        self.date_a = data ['date_a'],
        self.producto_anti = data ['producto_anti'],
        self.date_anti = data ['date_anti'],
        self.diagnostico = data ['diagnostico'],
        self.date_diag = data['date_diag'],
        self.medicamento = data['medicamento'],
        self.cantidad = data['cantidad'],
        self.frecuencia = data['frecuencia'],
        self.duracion = data['duracion'],
        self.instruction = data['instruction']
        
        self.mascotas_id = data['mascotas_id'] 
    
    @classmethod
    def get_by_id(cls,data): #nos regresa el historial en base al id
        query = "SELECT * FROM hmedicos WHERE hmedicos.id = %(id)s"
        result = connectToMySQL('projet').query_db(query,data)
        historia = cls(result[0]) 
        print(historia)
        return historia
    
    @classmethod
    def savehistorial(cls,data):
        #data = {}
        query = "INSERT INTO hmedicos(tipo_v,date_v,producto_v,producto_a,date_a,producto_anti,date_anti,diagnostico,date_diag,medicamento,cantidad,frecuencia,duracion,instruction,mascotas_id) VALUES (%(tipo_v)s,%(date_v)s,%(producto_v)s,%(producto_a)s,%(date_a)s,%(producto_anti)s,%(date_anti)s,%(diagnostico)s,%(date_diag)s,%(medicamento)s,%(cantidad)s,%(frecuencia)s,%(duracion)s,%(instruction)s,%(mascotas_id)s)" 
        result = connectToMySQL("projet").query_db(query,data)
        return result
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM hmedicos"
        results = connectToMySQL('projet').query_db(query)
        hmedico = []
        for r in results:
            hmedico.append(cls(r))
        return hmedico
    
    @classmethod
    def update(cls,data): #el id se encuentra en el edit
        query = "UPDATE hmedicos SET tipo_v=%(tipo_v)s, date_v=%(date_v)s,producto_v=%(producto_v)s,producto_a=%(producto_a)s,date_a=%(date_a)s,producto_anti = %(producto_anti)s,date_anti = %(date_anti)s,diagnostico = %(diagnostico)s, date_diag = %(date_diag)s, medicamento = %(medicamento)s, cantidad = %(cantidad)s, frecuencia = %(frecuencia)s, duracion = %(duracion)s, instruction = %(instruction)s, mascotas_id = %(mascotas_id)s WHERE id = %(id)s"
        result = connectToMySQL('projet').query_db(query,data)
        return result
    
    
        
    
    


