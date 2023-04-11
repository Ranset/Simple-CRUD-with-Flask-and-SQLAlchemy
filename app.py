# sec 1 Creaci'on de la aplicaci'on
# sec 2 Importando y configurando el ORM
# sec 3 Creaci'on de los modelos
# sec 4 Creaci'on de las tablas mediante python
# sec 5 Insertando datos
# sec 6 Mensajes Flash
# sec 7 Obteniendo los datos
# sec 8 Actualizando datos
# sec 9 Borrando Datos


from flask import Flask, render_template ## sec 1
from flask_sqlalchemy import SQLAlchemy ## sec 2
from flask import request, redirect, url_for ## sec 5
from flask import flash ## sec 6


app = Flask(__name__) ## sec 1
app.secret_key = 'MySecretKey' ## sec 2

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:''@localhost:3306/crud' ## sec 2
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False ## sec 2 / Si no ponemos esto nos manda una advertencia

db = SQLAlchemy(app) ## sec 2

class Data(db.Model): ## sec 3
    id = db.Column(db.Integer, primary_key = True) ## sec 3
    name = db.Column(db.String(100)) ## sec 3
    email = db.Column(db.String(100)) ## sec 3
    phone = db.Column(db.String(100)) ## sec 3

    def __init__(self, name, email, phone) -> None: ## sec 3
        self.name = name ## sec 3
        self.email = email ## sec 3
        self.phone = phone ## sec 3


@app.route('/') ## sec 1
def index(): ## sec 1

    context = { ## sec 7
        "all_data" : Data.query.all() ## sec 7
    }

    # Sec 7
    # En el html hacerle un for a la variable all_data
    # Ejemplo:
    #     {% for row in all_data %}
    # <tr>
    #     <td>{{row.id}}</td>
    # </tr>

    return render_template('index.html', **context) ## sec 1 ## **context en sec 7

@app.route('/insert', methods = ['POST']) # type: ignore ## sec 5
def insert(): ## sec 5
    if request.method == 'POST': ## sec 5

        name = request.form['name'] ## sec 5
        email = request.form['email'] ## sec 5
        phone = request.form['phone'] ## sec 5

        my_data = Data(name, email, phone) ## sec 5
        db.session.add(my_data) ## sec 5
        db.session.commit() ## sec 5

        flash('Employee inserted successfully') ## sec 6

        # Sec 6 insertar en el html para mostrar el mensaje
        # <!-- Successful Employee added message -->
        # {% with messages = get_flashed_messages()  %}
        #
        #     {% if messages %}
        #         {% for message in messages %}
        #            {{message}}
        #         {% endfor %}
        #     {% endif %}
        #    
        # {% endwith %}

        return redirect(url_for('index')) ## sec 5
    

@app.route('/update', methods = ['GET','POST']) # type: ignore ## sec 8
def update(): ## sec 8
    if request.method == 'POST': ## sec 8
        my_data = Data.query.get(request.form.get('id')) ## sec 8 # Se puede obtener tambi'en con get

        my_data.name = request.form['name'] ## sec 8
        my_data.email = request.form['email'] ## sec 8
        my_data.phone = request.form['phone'] ## sec 8

        db.session.commit() ## sec 8

        flash('Employee updated successfully') ## sec 8

        # Sec 8 modificar en el html para actualizar
        # Por ejemplo, actualizar el registro a trav'es de un formulario
        # dentro de una ventana modal.
        # La ventana modal debe estar dentro del loop del for de la tabla
        # para poder usar las variables de cada registro.
        # Al id de la ventana se le debe incluir el id del registro,
        # Y as'i crear un formulario por cada registro. Ej:
        # <div id="modaledit{{row.id}}" class="modal fade" role="dialog">
        # 
        # En el bot'on que abre la ventana de actualizaci'on:
        # Agregar al par'ametro data-target el id del registro
        # 
        # data-target="#modaledit{{row.id}}"
        # 
        # En el action del formulario poner el endpoint que ejecuta la actualizaci'on
        # Ej:
        # <form action="{{ url_for('update' ) }}" method="post">

        return redirect(url_for('index')) ## sec 8
    

@app.route('/delete/<id>/', methods= ['GET','POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    flash('Employee deleted successfully')

    # Poner en el href del bot'on la direcci'o'n de este endpoint con el id del registro
    # href="/delete/{{row.id}}"

    return redirect(url_for('index'))

if __name__ == "__main__": ## sec 1
    app.run(debug= True) ## sec 1