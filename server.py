from flask_app import app
#importacion de archivos de controladores
from flask_app.controllers import mascotas,vets,historial

if __name__=="__main__":
    app.run(debug=True)