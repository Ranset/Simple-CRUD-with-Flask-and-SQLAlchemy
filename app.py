# sec 1 Creación de la aplicación
# sec 2 Importando y configurando el ORM
# sec 3 Creación de los modelos
# sec 4 Creación de las tablas mediante python
# sec 5 Insertando datos
# sec 6 Mensajes Flash
# sec 7 Obteniendo los datos
# sec 8 Actualizando datos
# sec 9 Borrando Datos
# sec10 Creando el Admin
# sec11 Registro de usuario con flask_login y flask_wtf
# sec12 Login de usuario con flask_login y flask_wtf
# sec13 Logout de usuario con flask_login
# sec14 Bloquear endpoint para usuarios no registrados
# sec15 Protegiendo el admin con flask_login
# sec16 Agregando contenido al Home del Admin
# sec17 Agregando una nueva vista al Admin


from flask import Flask, render_template ## sec 1
from flask_sqlalchemy import SQLAlchemy ## sec 2
from flask import request, redirect, url_for ## sec 5
from flask import flash ## sec 6

from flask_admin import Admin ## sec10
from flask_admin import BaseView, expose ## sec17
from flask_admin.contrib.sqlamodel import ModelView ## sec10
from flask_admin import AdminIndexView ## sec15
from flask_login import LoginManager, login_user, current_user, UserMixin ## sec11
from flask_login import logout_user ## sec13
from flask_login import login_required ## sec14
from werkzeug.security import check_password_hash, generate_password_hash ## sec11

from forms import RegisterForm ## sec11
from forms import LoginForm ## sec12


app = Flask(__name__) ## sec 1
app.secret_key = 'MySecretKey' ## sec 2

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:''@localhost:3306/crud' ## sec 2
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False ## sec 2 / Si no ponemos esto nos manda una advertencia

# Configuraciones
db = SQLAlchemy(app) ## sec 2
# admin = Admin(app) ## sec10
login_manager = LoginManager(app) ## sec11

class Data(db.Model): ## sec 3
    id = db.Column(db.Integer, primary_key = True) ## sec 3
    name = db.Column(db.String(100)) ## sec 3
    email = db.Column(db.String(100)) ## sec 3
    phone = db.Column(db.String(100)) ## sec 3

    def __init__(self, name, email, phone) -> None: ## sec 3
        self.name = name ## sec 3
        self.email = email ## sec 3
        self.phone = phone ## sec 3

    def __repr__(self) -> str: ## sec10
        return self.name ## sec10


## Todo este modelos es de ## sec11 ###############################
class User(db.Model, UserMixin):                                  #
    id = db.Column(db.Integer, primary_key = True)                #
    email = db.Column(db.String(100), unique = True)              #
    username = db.Column(db.String(100))                          #
    password = db.Column(db.String(400))                          #
    name = db.Column(db.String(100))                              #

    def check_password(self, password):                           #
        return check_password_hash(self.password,password)        # Hasta aquí

# #sec15 Para proteger una vista espec'ifica en el admin, Por ejemplo en este caso la
# tabla Data creamos una clase de ModelView para sobreescirbir el m'etodo is_accessible().
class MyModelView(ModelView): ## sec15
    # Con esto la tabla Data se muestra en el Admin solo si el usuario está autenticado.
    def is_accessible(self): ## sec15
        return current_user.is_authenticated # type: ignore ## sec15
    
    # función que se ejecuta cuando se da el error por necesitar estar el usuario autenticado
    def inaccessible_callback(self, name, **kwargs): ## sec15
        flash('Debe estar autenticado', 'error') ## sec15
        return redirect(url_for('index')) ## sec15
    

# #sec15 Para proteger la vista Home en el admin
# creamos una clase de AdminIndexView para sobreescirbir el m'etodo is_accessible().
class MyAdminIndexView(AdminIndexView): ## sec15
    # Con esto se muestra el Home en el Admin solo si el usuario está autenticado.
    def is_accessible(self): ## sec15
        return current_user.is_authenticated # type: ignore ## sec15
    
    # función que se ejecuta cuando se da el error por necesitar estar el usuario autenticado
    def inaccessible_callback(self, name, **kwargs): ## sec15
        flash('Debe estar autenticado', 'error') ## sec15
        return redirect(url_for('index')) ## sec15
    

class MyNewView(BaseView): ## sec17
    @expose('/') ## sec17
    def index(self): ## sec17
        return self.render('admin/mynewview.html') ## sec17

admin = Admin(app , index_view=MyAdminIndexView(), name='MyApp') ## sec15 Crear después de la clase MyAdminIndexView
# admin.add_view(ModelView(Data, db.session)) ## sec10
admin.add_view(MyNewView(name='My view', endpoint='newview')) ## sec17
admin.add_view(MyModelView(Data, db.session)) ## sec15
admin.add_view(ModelView(User, db.session,name='Usuarios',)) ## sec11

# Este decorador es obligatorio para que flask_login cargue el ususario
@login_manager.user_loader ## sec11
def user_loader(user_id): ## sec11
    return User.query.get(user_id) ## sec11

# Este decorador dispara la función cuando se da el error por necesitar estar el usuario autenticado
@login_manager.unauthorized_handler ## sec14
def unauthorized(): ## sec14
    flash('Debe estar autenticado', 'error') ## sec14
    return redirect(url_for('index')) ## sec14


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
        # Y así crear un formulario por cada registro. Ej:
        # <div id="modaledit{{row.id}}" class="modal fade" role="dialog">
        # 
        # En el botón que abre la ventana de actualización:
        # Agregar al par'ametro data-target el id del registro
        # 
        # data-target="#modaledit{{row.id}}"
        # 
        # En el action del formulario poner el endpoint que ejecuta la actualización
        # Ej:
        # <form action="{{ url_for('update' ) }}" method="post">

        return redirect(url_for('index')) ## sec 8
    

@app.route('/delete/<id>/', methods= ['GET','POST']) ## sec 9
@login_required ## sec14
def delete(id): ## sec 9
    my_data = Data.query.get(id) ## sec 9
    db.session.delete(my_data) ## sec 9
    db.session.commit() ## sec 9

    flash('Employee deleted successfully') ## sec 9

    # Poner en el href del botón la direcció'n de este endpoint con el id del registro
    # href="/delete/{{row.id}}"

    return redirect(url_for('index')) ## sec 9

## Todo este modelos es de ## sec11 #########################################
@app.route('/register', methods = ['GET', 'POST'])                          #
def register():                                                             #
    form = RegisterForm(meta={'csrf':False})                                #

    if form.validate_on_submit():                                           #
        if User.query.filter_by(username=form.username.data).first():       #
            print("Usuario duplicado")                                      #
        else:                                                               #
            user = User()                                                   #
            user.name = form.name.data                                      #
            user.username = form.username.data                              #
            user.password = generate_password_hash(form.password.data)      #
            user.email = form.email.data                                    #

            db.session.add(user)                                            #
            db.session.commit()                                             #

            login_user(user, remember=True)                                 #

            return redirect(url_for('register'))                            #

    if form.errors:                                                         #
        print(form.errors)                                                  #

    context = {                                                             #
        "form": form                                                        #
    }                                                                       #

    return render_template('register.html', **context)                      # Hasta aquí la sec11

## Todo este modelos es de ## sec12 #########################################
@app.route('/login', methods = ['GET', 'POST'])                             #
def login():                                                                #
    form = LoginForm(meta={'csrf':False})                                   #

    if form.validate_on_submit():                                           #
        user = User.query.filter_by(username=form.username.data).first()    #
        if user and user.check_password(form.password.data):                #
            login_user(user, remember=True)                                 #

            return redirect(url_for('index'))                               #

    if form.errors:                                                         #
        print(form.errors)                                                  #

    context = {                                                             #
        "form": form                                                        #
    }                                                                       #

    return render_template('login.html', **context)                         # Hasta aquí la sec12

## Todo este código es de ## sec13 #########################################
@app.route('/logout', methods = ['GET'])                                    #
def logout():                                                               #
    logout_user()                                                           #
    flash('Sesión cerrada satisfactoriamente')

    return redirect(url_for('index'))                                       # Hasta aquí la sec13

#################### sec16 #############################
# Se debe crear una carpeta con el nombre admin dentro templates
# y dentro el archivo index.html que sobre escribe el original
# Se extiende master.html y se pone contenido dentro del bloque body
# 
# {% extends 'admin/master.html' %}
# 
# {% block body %}
#   <h1>Hello world</h1>
# {% endblock %}

if __name__ == "__main__": ## sec 1
    app.run(debug= True) ## sec 1