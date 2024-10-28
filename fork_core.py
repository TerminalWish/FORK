import os
from flask import jsonify, Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath(os.path.join('instance', 'fork.db'))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Set up the engine and scoped session
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"], echo=True)
Session = scoped_session(sessionmaker(bind=engine))

### Base Tables
class Menu(db.Model):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String, nullable=False)
    availability = db.Column(db.Boolean, default=True)

    # Useful for debugging
    def __repr__(self):
        return f'<Menu {self.name}>'

class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    menu = relationship('Menu', secondary='menu_ingredient', backref='ingredient')

    # Useful for debugging
    def __repr__(self):
        return f'<Ingredient {self.name}>'

### Relationship Tables
class MenuIngredient(db.Model):
    __tablename__ = 'menu_ingredient'
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    quantity = db.Column(db.Float, nullable=False)
    measurement = db.Column(db.String, nullable=False)

    # Useful for debugging
    def __repr__(self):
        return f'<MenuIngredient {self.menu_id, self.ingredient_id}>'

### Routing Methods
@app.route('/menu', methods=['GET'])
def get_menu():
    session = Session()

    menu_items = session.query(Menu).all()
    menu_list = [item.as_dict() for item in menu_items]

    session.close()

    return jsonify(menu_list)

# Help function to aid with jsonifying table data
def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

setattr(Menu, "as_dict", as_dict)

# Teardown to remove the session after each request
@app.teardown_appcontext
def remove_session(exception=None):
    Session.remove() # Ensures all sessions are closed after request

if __name__ == "__main__":
    app.run(debug=True, port=5000)