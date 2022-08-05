from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades, Usuarios
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

#USUARIOS = {
#    'Jorge':'123',
#    'Luiz':'321'
#}

#@auth.verify_password
#def verificacao(login, senha):
#    if not(login, senha):
#        return False
#    else:
#        return USUARIOS.get(login) == senha

@auth.verify_password
def verificacao(login, senha):
    if not(login, senha):
        return False
    else:
        return Usuarios.query.filter_by(login=login, senha=senha).first()


class Pessoa(Resource):
    @auth.login_required
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        try:
            response = {
                'nome':pessoa.nome,
                'idade':pessoa.idade,
                'id':pessoa.id
            }
        except AttributeError:
            response = {
                'status':'error',
                'mensagem':'pessoa nao encontrada'
            }
        return response

    def put(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        dados = request.json
        if 'nome' in dados:
            pessoa.nome = dados['nome']
        if 'idade' in dados:
            pessoa.idade = dados['idade']
        pessoa.save()
        response = {
            'id':pessoa.id,
            'nome':pessoa.nome,
            'idade':pessoa.idade
        }
        return response

    def delete(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        mensagem = 'Pessoa {} excluida com sucesso'.format(pessoa.nome)
        pessoa.delete()
        return {
            'status':'suceso',
            'mensagem':mensagem

        }

class ListaPessoas(Resource):
    @auth.login_required
    def get(self):
        pessoas = Pessoas.query.all()
        #for i in pessoas:
        #    lista.append('nome':i.nome)
        response = [{'id':i.id, 'nome':i.nome, 'idade':i.idade} for i in pessoas]
        return response

    def post(self):
        dados = request.json
        pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
        pessoa.save()
        response = {
            'id': pessoa.id,
            'nome': pessoa.nome,
            'idade': pessoa.idade
        }
        return response

class ListaAtividades(Resource):
    def get(self):
        #dados = request.json
        #atividade = Atividades.query.filter_by(id=0).first()
        #atividade = Atividades.query.filter_by(id=1).first()
        #atividade = Atividades(nome=dados['nome'], pessoa=pessoa)
        atividades = Atividades.query.all()
        response = [{'id':i.id, 'nome':i.nome, 'pessoa':i.pessoa.nome} for i in atividades]
        #response = {
        #    'pessoa': atividade.pessoa.nome,
        #    'nome': atividade.nome,
        #    'id': atividade.id
        #}
        return response

    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
        atividade = Atividades(nome=dados['nome'], pessoa=pessoa)
        atividade.save()
        response = {
            'pessoa': atividade.pessoa.nome,
            'nome': atividade.nome,
            'id': atividade.id
        }
        return response

class Atividade(Resource):
    def delete(self, id):
        atividade = Atividades.query.filter_by(id=id).first()
        mensagem = 'Atividade {} excluida com sucesso'.format(atividade.id)
        atividade.delete()
        return {
            'status':'suceso',
            'mensagem':mensagem

        }

api.add_resource(Pessoa, '/pessoa/<string:nome>/')
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(Atividade, '/atividades/<int:id>/')
api.add_resource(ListaAtividades, '/atividades/')


if __name__ == '__main__':
    app.run(debug=True)