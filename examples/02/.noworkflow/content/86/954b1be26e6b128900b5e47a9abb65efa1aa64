class Turma:
    def __init__(self,codigo, disciplina, professor, periodo):
        self.codigo = codigo
        self.disciplina = disciplina
        self.professor=professor
        self.periodo = periodo
        self.alunos = []

    def listaAlunos(self):
        print ("Alunos da turma ", self.codigo, self.disciplina.getNome())
        for a in self.alunos:
            print (a.getNome())

    def adicionaAluno(self, aluno):
        self.alunos+= [aluno]

    def teste(self, aux):
        print(aux.getNome())


class IdUff:
    def __init__(self):
        self.disciplinas = []
        self.alunos = []
        self.turmas = []


    def cadastraAluno(self, aluno):
        self.alunos += [aluno]

    def cadastraDisciplina(self, disc):
        self.disciplinas += [disc]

    def cadastraTurma(self, turma, aux):
        print(aux)
        self.turmas += [turma]

    def geraCrid(self, aluno):
        pass

    def inscreveAluno(self, aluno, turma):
        turma.adicionaAluno(aluno)

    def listaAlunos(self):
        print ("\n---------------------------------")
        for a in self.alunos:
            print (a.getNome(), a.getDre())
        print ("\n---------------------------------")

    def teste(self, aux):
        print(aux.getNome())


class Disciplina:
    def __init__(self, nome, codigo, creditos):
        self.__nome = nome
        self.__codigo = codigo
        self.__creditos = creditos

    def getNome(self):
        return self.__nome

    def getCodigo(self):
        return self.__codigo

    def getCreditos(self):
        return self.__creditos

class Aluno:
    def __init__(self, dre, nome):
        self.__dre = dre
        self.__nome = nome
        self.__inscricoes = []
    def getNome(self):
        return self.__nome
    def getDre(self):
        return self.__dre
    def getInscricoes(self):
        return self.__inscricoes
    def __str__(self):
        return str("Aluno nome: "+ self.__nome + " DRE: "+ self.__dre)



def desloga():
    print ("Usuário deslogado")

def sair():
    desloga()
    print ("Conexão terminada")

aluno1 = Aluno("001", "Daniel")

disciplina1 = Disciplina("e-science", "001", 4)
turma1 = Turma("001" , disciplina1, "Vanessa", "1")
#turma1.adicionaAluno(aluno1)
#turma1.adicionaAluno(aluno2)
#turma1.adicionaAluno(aluno3)

iduff_conn = IdUff()
iduff_conn.cadastraAluno(aluno1)

iduff_conn.cadastraDisciplina(disciplina1)

iduff_conn.cadastraTurma(turma1, "7384")

iduff_conn.inscreveAluno(aluno1, turma1)

turma1.listaAlunos()

iduff_conn.listaAlunos()

turma1.teste(aluno1)
iduff_conn.teste(disciplina1)

sair()
