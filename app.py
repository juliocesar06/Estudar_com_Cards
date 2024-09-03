from flask import Flask,render_template,url_for,request,redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from wikipedia import wikipedia as wiki

# instanciando flask
app = Flask(__name__)

# criando banco de dados 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
db = SQLAlchemy(app)

#tabela db
class  Cards(db.Model):
    __name__ = 'Cards'
    id =  db.Column(db.Integer,primary_key=True,autoincrement=True)
    tema= db.Column(db.String(30))
    sub_tema= db.Column(db.String(30))
    resumo= db.Column(db.String(100))
    link1= db.Column(db.String(30))

 
    def __init__(self,tema,sub_tema,resumo,link1):
        self.tema= tema
        self.sub_tema = sub_tema
        self.resumo = resumo
        self.link1 = link1



    


#pagina inicial
@app.route('/')
def index():
    c = Cards.query.all()
    indice = 0
    return render_template('index.html',cards=c,indice=indice)

# receber o form e colocar no banco de dados
@app.route('/busca',methods=['GET','POST'])
def buscar():
    
    if request.method =='POST':
        print('post')
        tema = request.form['tema']
        tema = tema.replace(' ','_')
        if tema != None:
            wiki.set_lang('Pt')
            busca = wiki.search(f'{tema}')
            page = wiki.page(busca[0])
            sub_tema = page.title
            link = page.url
            resumo = page.summary
            #item para banco de dados
            add_new = Cards(tema,sub_tema,resumo,link)
        try:
            db.session.add(add_new)
            db.session.commit()
            return redirect('/busca')
        except:
            print('erro')
            return render_template('index.html')
    else:
        print('get')
    return render_template('busca.html')






if __name__=='__main__':
    
    with app.app_context():
        db.create_all()
    app.run(debug=True)