from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ok@localhost/book'
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)
# Object of Api class
api = Api(app)
#configure the app to solve the access control error
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', 'http://localhost:4200')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Credentials', 'true');
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,UPDATE,OPTIONS')
  return response
class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    price = db.Column(db.String(255))
    description = db.Column(db.String(255))

    def json(self):
        return {'id': self.id,'name':self.name, 'price': self.price, 'description':self.description}
    def add_book(_name, _price, _description):
        '''function to add book to database using _name, _price, _description
        as parameters'''
        # creating an instance of our Movie constructor
        new_book = Book(name=_name, price=_price, description=_description)
        db.session.add(new_book)  # add new movie to database session
        db.session.commit()

    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description

    
    def __repr__(self):
        return '%s/%s/%s%s' % (self.id,self.name, self.price, self.description)



@app.route('/add', methods=['POST'])
def add_book():
    
    # POST a data to database
    if request.method == 'POST':
        body = request.get_json()
        name = body['name']
        price = body['price']
        description = body['description']


        data = Book(name, price, description)
        db.session.add(data)
        db.session.commit()

        return jsonify({
            'status': 'book is posted to PostgreSQL!',
            'name': name,
            'price': price,
            'description': description
        })
 
    # GET all data from database & sort by id
@app.route('/book', methods=['GET'])
def book():
    
    if request.method == 'GET':
              return jsonify([book.json() for book in Book.query.order_by(Book.id).all()])

        # data = User.query.all()
 #       data = Book.query.order_by(Book.id).all()
 #       for i in range(len(data)): 
 #       for book in data:
#          book_ob[i]={
#          'id': book.id,
 #         'name': book.name,
 #         'price': book.price,
  #       'description': book.description
   #     } 
#     print(data)
 #       dataJson = []
      #  for i in range(len(data)):
       #     # print(str(data[i]).split('/'))
        #    dataDict = {
         #       'id': str(data[i]).split('/')[0],
          #      'name': str(data[i]).split('/')[1],
           #     'price': str(data[i]).split('/')[2],
            #    'description': str(data[i]).split('/')[3],

            #}
        #dataJson.append(book_ob)
        #return dataJson
     #  return jsonify(dataJson)

@app.route('/book/<string:id>', methods=['GET'])
def onebook(id):

    # GET a specific data by id
    if request.method == 'GET':
      return jsonify(Book.json(Book.query.filter_by(id=id).first()))
#        data = Book.query.get(id)
#        print(data)
#        dataDict = {
#            'name': str(data).split('/')[0],
#            'price': str(data).split('/')[1],
#            'description': str(data).split('/')[2],
#    
#        }
#        return jsonify(dataDict)
@app.route('/delete/<string:id>', methods=['DELETE'])
def deletebook(id):        
    # DELETE a data
    if request.method == 'DELETE':
        delData = Book.query.filter_by(id=id).first()
        db.session.delete(delData)
        db.session.commit()
        return jsonify({'status': 'Book '+id+' is deleted from PostgreSQL!'})

@app.route('/update/<string:id>', methods=['PUT'])
def updatebook(id): 
    # UPDATE a data by id
    if request.method == 'PUT':
        body = request.get_json()
        newName = body['name']
        newPrice = body['price']
        newDescription = body['description']
        editData = Book.query.filter_by(id=id).first()
        editData.name = newName
        editData.price = newPrice
        editData.description = newDescription
        db.session.commit()
        return jsonify({'status': 'Book '+id+' is updated from PostgreSQL!'})


     
if __name__ == '__main__':
    app.debug = True
    app.run()

