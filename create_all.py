## sec 4 #############
## Este archivo se ejecuta solo una vez para crear las tablas en la base de datos
from app import db, app

with app.app_context():
  db.create_all()