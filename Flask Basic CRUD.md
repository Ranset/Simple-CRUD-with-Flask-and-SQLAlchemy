# Flask Basic CRUD

por Ranset Fleites
<!-- vscode-markdown-toc -->
* 1. [Creación de la aplicación](#Creacindelaaplicacin)
* 2. [Importando y configurando el ORM](#ImportandoyconfigurandoelORM)
* 3. [Creación de los modelos](#Creacindelosmodelos)
* 4. [Creación de las tablas mediante python](#Creacindelastablasmediantepython)
* 5. [Insertando datos](#Insertandodatos)
* 6. [Mensajes Flash](#MensajesFlash)
* 7. [Obteniendo los datos](#Obteniendolosdatos)
* 8. [Actualizando datos](#Actualizandodatos)
* 9. [Borrando Datos](#BorrandoDatos)
* 10. [Creando el Admin](#CreandoelAdmin)
* 11. [Registro de usuario con flask_login y flask_wtf](#Registrodeusuarioconflask_loginyflask_wtf)
* 12. [Login de usuario con flask_login y flask_wtf](#Logindeusuarioconflask_loginyflask_wtf)
* 13. [Logout de usuario con flask_login](#Logoutdeusuarioconflask_login)
* 14. [Bloquear endpoint para usuarios no registrados](#Bloquearendpointparausuariosnoregistrados)
* 15. [Protegiendo el admin con flask_login](#Protegiendoeladminconflask_login)
	* 15.1. [Para proteger la vista Home en el admin](#ParaprotegerlavistaHomeeneladmin)
* 16. [Agregando contenido al Home del Admin](#AgregandocontenidoalHomedelAdmin)
* 17. [Agregando una nueva vista al Admin](#AgregandounanuevavistaalAdmin)
* 18. [Controlando páginas de errores](#Controlandopginasdeerrores)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->


##  1. <a name='Creacindelaaplicacin'></a>Creación de la aplicación



```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug= True)
```

##  2. <a name='ImportandoyconfigurandoelORM'></a>Importando y configurando el ORM


```python
from flask_sqlalchemy import SQLAlchemy

# Después de app = Flask(__name__)
app.secret_key = 'MySecretKey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:''@localhost:3306/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Si no ponemos esto nos manda una advertencia

db = SQLAlchemy(app)
```

##  3. <a name='Creacindelosmodelos'></a>Creación de los modelos


```python
class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, name, email, phone) -> None:
        self.name = name
        self.email = email
        self.phone = phone
```

##  4. <a name='Creacindelastablasmediantepython'></a>Creación de las tablas mediante python


```python
# create_all.py
## Este archivo se ejecuta solo una vez para crear las tablas en la base de datos
from app import db, app

with app.app_context():
  db.create_all()
```

##  5. <a name='Insertandodatos'></a>Insertando datos


```python
from flask import request, redirect, url_for

@app.route('/insert', methods = ['POST']) # type: ignore
def insert():
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        my_data = Data(name, email, phone)
        db.session.add(my_data)
        db.session.commit()
        
        return redirect(url_for('index'))
```

##  6. <a name='MensajesFlash'></a>Mensajes Flash


```python
from flask import flash

@app.route('/insert', methods = ['POST']) # type: ignore
def insert():
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        my_data = Data(name, email, phone)
        db.session.add(my_data)
        db.session.commit()

        flash('Employee inserted successfully') # Insertar para el mensaje flask

        return redirect(url_for('index'))
```

Insertar en el HTML donde se quiera mostrar el mensaje flash.
```html
<!-- Successful message -->
{% with messages = get_flashed_messages()  %}

    {% if messages %}
        {% for message in messages %}
            {{message}}
        {% endfor %}
    {% endif %}
   
{% endwith %}
```

##  7. <a name='Obteniendolosdatos'></a>Obteniendo los datos

Guardamos todos los registros en la clave *"all_data"* del diccionario *context*


```python
@app.route('/')
def index():

    context = {
        "all_data" : Data.query.all()
    }

    return render_template('index.html', **context) # Agregar **context para pasar los datos
```

En el html hacerle un for a la variable *all_data*:

```html
{% for row in all_data %}
    <tr>
        <td>{{row.id}}</td>
    </tr>
{% endfor %}
```

##  8. <a name='Actualizandodatos'></a>Actualizando datos


```python
@app.route('/update', methods = ['GET','POST']) # type: ignore
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id')) # Se puede obtener también con get

        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']

        db.session.commit()

        flash('Employee updated successfully')

        return redirect(url_for('index'))
```

Modificar en el html para actualizar:

Por ejemplo, actualizar el registro a través de un formulario dentro de una ventana modal.
La ventana modal debe estar dentro del loop del for de la tabla para poder usar las variables de cada registro.
Al id de la ventana se le debe incluir el id del registro, y así crear un formulario por cada registro.
Ej:
```html
    <div id="modaledit{{row.id}}" class="modal fade" role="dialog">
```

En el botón que abre la ventana de actualización:
Agregar al parámetro *data-target* el id del registro
```html
    data-target="#modaledit{{row.id}}"
``` 

En el action del formulario poner el endpoint que ejecuta la actualización
Ej:
```html
    <form action="{{ url_for('update' ) }}" method="post">
```

##  9. <a name='BorrandoDatos'></a>Borrando Datos


```python
@app.route('/delete/<id>/', methods= ['GET','POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    flash('Employee deleted successfully')

    return redirect(url_for('index'))
```

Poner en el href del botón la dirección de este endpoint con el id del registro

href="/delete/{{row.id}}"

##  10. <a name='CreandoelAdmin'></a>Creando el Admin


```python
from flask_admin import Admin
from flask_admin.contrib.sqlamodel import ModelView

admin = Admin(app)
```

Dentro de las clases de los modelos de sobrescribir el método *__repr__* para mostrar lo que queramos en la tabla del Admin.


```python
def __repr__(self) -> str:
    return self.name
```

Agregamos los medelos a la *view* del Admin


```python
admin.add_view(ModelView(Data, db.session))
```

##  11. <a name='Registrodeusuarioconflask_loginyflask_wtf'></a>Registro de usuario con flask_login y flask_wtf

Podemos crear el formulario con *flask_wtf* para el registro de usuario. Podemos poner que confirme que los campos de password son iguales.


```python
# forms.py

from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo

class RegisterForm(FlaskForm):
    name = StringField('Nombre', validators=[InputRequired()])
    username = StringField('Usuario', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('confirm')])
    confirm = PasswordField('Confirmar', validators=[InputRequired()])
```

En el archivo principal:


```python
from flask_login import LoginManager, login_user, current_user, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from forms import RegisterForm

# (...)

login_manager = LoginManager(app)
```

Creamos el modelo de la base de datos donde se guardarán los usuarios de la aplicaión. Con herencia múltiple de *db.Model* y *__UserMixin__* para especificar que este modelo será usado para controlar los usuarios.

Le agregamos un método (check_password) que usaremos luego cuando el usuario se loguee verificar que el password es el correcto. Este método desemcripta el password de la base de datos y devuelve *True* si es el mismo que se le pasó en el parámetro al método.


```python
class User(db.Model, UserMixin):                                  
    id = db.Column(db.Integer, primary_key = True)                
    email = db.Column(db.String(100), unique = True)              
    username = db.Column(db.String(100))                          
    password = db.Column(db.String(400))                          
    name = db.Column(db.String(100))                              

    def check_password(self, password):                           
        return check_password_hash(self.password,password)
```

Podemos agregar también la tabla a la vista de administración. 


```python
admin.add_view(ModelView(User, db.session,name='Usuarios',))
```

Creamos el decorador *user_loader* que es obligatorio para que *flask_login* cargue el ususario. Debemos colocarlo en cualquier parte del código que se cargue primero.


```python
@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)
```

Creamos la ruta para ejecutar el formulario de registro.


```python
@app.route('/register', methods = ['GET', 'POST'])                          
def register():                                                             
    form = RegisterForm(meta={'csrf':False}) # Si queremos evitar comprobar csfr

    if form.validate_on_submit():                                           
        if User.query.filter_by(username=form.username.data).first():       
            print("El nombre de usuario ya existe")                         
        else:                                                               
            user = User()                                                   
            user.name = form.name.data                                      
            user.username = form.username.data                              
            user.password = generate_password_hash(form.password.data)      
            user.email = form.email.data                                    

            db.session.add(user)                                            
            db.session.commit()                                             

            login_user(user, remember=True)                                 

            return redirect(url_for('register'))                            

    if form.errors:                                                         
        print(form.errors)                                                  

    context = {                                                             
        "form": form                                                        
    }                                                                       

    return render_template('register.html', **context)
```

##  12. <a name='Logindeusuarioconflask_loginyflask_wtf'></a>Login de usuario con flask_login y flask_wtf

Podemos crear el formulario con *flask_wtf* para el login del usuario.


```python
# forms.py

# (...)

class LoginForm(FlaskForm):
    
    username = StringField('Usuario', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
```

Creamos la ruta para ejecutar el formulario de login.


```python
from forms import LoginForm

# (...)

@app.route('/login', methods = ['GET', 'POST'])                             
def login():                                                                
    form = LoginForm(meta={'csrf':False})                                   

    if form.validate_on_submit():                                           
        user = User.query.filter_by(username=form.username.data).first()    
        if user and user.check_password(form.password.data):                
            login_user(user, remember=True)                                 

            return redirect(url_for('index'))                               

    if form.errors:                                                         
        print(form.errors)                                                  

    context = {                                                             
        "form": form                                                        
    }                                                                       

    return render_template('login.html', **context)   
```

##  13. <a name='Logoutdeusuarioconflask_login'></a>Logout de usuario con flask_login

Creamos la ruta para el logout del usuario. Cualquier enlace a este endpoint cerrará la sesión del usuario.


```python
from flask_login import logout_user

# (...)

@app.route('/logout', methods = ['GET'])                                    
def logout():                                                               
    logout_user()                                                           
    flash('Sesión cerrada satisfactoriamente')

    return redirect(url_for('index'))
```

##  14. <a name='Bloquearendpointparausuariosnoregistrados'></a>Bloquear endpoint para usuarios no registrados

Agregamos el decorador *@login_required* al endpoint que queramos proteger.


```python
from flask_login import login_required

# (...)

@app.route('/delete/<id>/', methods= ['GET','POST']) #
@login_required # Agregamos este decorador al enpoint que queramos proteger.
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    flash('Employee deleted successfully')

    return redirect(url_for('index'))
```

Podemos usar el decorador *@login_manager.unauthorized_handler* para dispara la función cuando se da el error por necesitar estar el usuario autenticado.


```python
@login_manager.unauthorized_handler
def unauthorized():
    flash('Debe estar autenticado', 'error')
    return redirect(url_for('index'))
```

##  15. <a name='Protegiendoeladminconflask_login'></a>Protegiendo el admin con flask_login

Para proteger una vista específica en el admin, Por ejemplo en este caso la tabla Data creamos una clase de ModelView para sobreescirbir el método is_accessible().


```python
from flask_admin import AdminIndexView

class MyModelView(ModelView): 
    
    # Con esto la vista se muestra en el Admin solo si el usuario está autenticado.
    def is_accessible(self): 
        return current_user.is_authenticated # type: ignore
```

Cuando agregamos el modelo a la vista *admin* lo hacemos con la clase donde implementamos el *is_accessible(self)*.


```python
admin.add_view(MyModelView(Data, db.session))
```

También al *ModelView* personalizado podemos agregarle un método que se ejecuta cuando da error por el usuario no estar autenticado.


```python
def inaccessible_callback(self, name, **kwargs):
    flash('Debe estar autenticado', 'error')
    return redirect(url_for('index'))
```

###  15.1. <a name='ParaprotegerlavistaHomeeneladmin'></a>Para proteger la vista Home en el admin
Básica mente lo mismo que lo anterior pero en vez de heredar de *ModelView* hereda de *AdminIndexView* entonces por lo que creamos una clase de *AdminIndexView* para sobreescirbir el método *is_accessible()* de dicha clase.


```python
class MyAdminIndexView(AdminIndexView):

    def is_accessible(self):
        return current_user.is_authenticated # type: ignore
    
    def inaccessible_callback(self, name, **kwargs):
        flash('Debe estar autenticado', 'error')
        return redirect(url_for('index'))
```

Instanciamos el objeto *admin* con esta clase.


```python
admin = Admin(app , index_view=MyAdminIndexView(), name='MyApp') # Crear después de la clase MyAdminIndexView
```

##  16. <a name='AgregandocontenidoalHomedelAdmin'></a>Agregando contenido al Home del Admin
Se debe crear una carpeta con el nombre admin dentro templates y dentro el archivo *index.html* que sobre escribe el original se extiende de *master.html* y se pone contenido dentro del bloque *body*.

```html
{% extends 'admin/master.html' %}
 
 {% block body %}
   <h1>Hello world</h1>
 {% endblock %}
```

##  17. <a name='AgregandounanuevavistaalAdmin'></a>Agregando una nueva vista al Admin


```python
from flask_admin import BaseView, expose
```


```python
class MyNewView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/mynewview.html')
```


```python
admin.add_view(MyNewView(name='My view', endpoint='newview'))
```

##  18. <a name='Controlandopginasdeerrores'></a>Controlando páginas de errores
Utilizamos un decorador especial @app.errorhandler() que recibe como parámetro el código del error.


```python
@app.errorhandler(404)
def page_404(error):
    return render_template('404.html', error=error)
```

Dentro de la carpeta template creamos el archivo *404.html*.
Código de ejemplo para este archivo:

```html
{% extends "./base.html" %}

{% block content %}
    <h1>404</h1>
    <h2>La página no existe</h2>
    <p>{{error}}</p>
{% endblock %}
```
