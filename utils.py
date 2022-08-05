from models import Pessoas

def insere_pessoa():
    pessoa = Pessoas(nome='Luiz', idade=39)
    print(pessoa)
    pessoa.save()

def consulta_pessoa():
    #pessoa = Pessoas.query.filter_by(nome='Luiz').first()
    pessoa = Pessoas.query.all()
    print(pessoa)
    #print(pessoa.idade)

def altera_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Luiz').first()
    pessoa.idade = 50
    pessoa.save()

def exclui_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Jorge').first()
    pessoa.delete()

if __name__ == '__main__':
    insere_pessoa()
    #altera_pessoa()
    #exclui_pessoa()
    consulta_pessoa()