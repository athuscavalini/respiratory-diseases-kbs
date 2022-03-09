from experta import *



# Funções auxiliares:

def pergunta_sn(question, true_value=True, false_value=False):
    while True:
        answer = input("\n" + question + " [S/N] ").upper()
        if (answer == 'S'): return true_value
        if (answer == 'N'): return false_value
        print("Responda com Sim (S) ou Não (N).")

def pergunta_opt(question, options={1: ('Sim',True), 2: ('Não',False) } ):
    while True:
        enunciado = question + '\n'
        opcoes = ''.join(str(k) + ": " + v[0] + '\n' for k,v in options.items())
        answer = input("\n" + enunciado+opcoes + "Escolha uma opção: ")

        if (answer.isnumeric() and (int(answer) in options)): return options[int(answer)][1]
        print("\nEscolha uma opção válida.")



# Definindo tipos de fatos do dominio

class Sintoma(Fact):
    pass

class Subarvore(Fact): # classe auxiliar para definir doenca
    pass

class Doenca(Fact):
    pass


# Definindo regras do sistema 

class IdentificaDoenca(KnowledgeEngine):

    # Perguntas sobre os sintomas

    @Rule(NOT(Doenca(W())))
    def chiado(self):
        self.declare(Sintoma(chiado=pergunta_sn('Dificuldade de respirar (chiado no peito)?')))

    @Rule(AND (NOT(Doenca(W())), NOT(Subarvore(3))))
    def tosse(self):
        self.declare(Sintoma(tosse=pergunta_opt("Como está sua tosse?",{
                                  0: ('Seca.', 0),
                                  1: ('Produtiva.',1),
                              })))

    @Rule(AND (NOT(Doenca(W())), OR(Subarvore(1), AND(Subarvore(3), Sintoma(dor_no_peito=True)), Subarvore(6))))
    def tosse_sangue(self):
        self.declare(Sintoma(tossindo_sangue=pergunta_sn('Tosse apresenta sangue?')))

    @Rule(AND (NOT(Doenca(W())), OR(Sintoma(fuma=True), Subarvore(3), AND(Subarvore(2), Sintoma(febre=True)))))
    def dor_no_peito(self):
        self.declare(Sintoma(dor_no_peito=pergunta_sn('Possui dor no peito?')))

    @Rule(AND( NOT(Doenca(W())), Sintoma(chiado=True)))
    def fumante(self):
        self.declare(Sintoma(fuma=pergunta_sn('Fuma?')))

    @Rule(AND(NOT(Doenca(W())), OR(Sintoma(fuma=False), Subarvore(1))))
    def respiracao_rapida(self):
        self.declare(Sintoma(respiracao_rapida=pergunta_sn('Respiração rápida (cansaço)?')))

    @Rule(NOT(Doenca(W())), OR(Subarvore(2), AND(Subarvore(4),Sintoma(tosse=1))))
    def febre(self):
        self.declare(Sintoma(febre=pergunta_sn('Possui febre?')))

    @Rule(AND (NOT(Doenca(W())), Subarvore(4), Sintoma(febre=False)))
    def batimentos_acelerados(self):
        self.declare(Sintoma(batimentos_acelerados=pergunta_sn('Batimentos cardíacos acelerados?')))

    @Rule(AND ( NOT(Doenca(W())), OR(Subarvore(1), AND(Subarvore(2),Sintoma(febre=True),Sintoma(dor_no_peito=False))) ) )
    def olfato_paladar(self):
        self.declare(Sintoma(olfato_paladar=pergunta_sn('Apresentou perda de olfato ou paladar?')))

    # Identificando subarvore

    @Rule(Sintoma(chiado=False), Sintoma(tosse=0))
    def subarvore_1(self):
        self.declare(Subarvore(1))

    @Rule(Sintoma(chiado=False), Sintoma(tosse=1))
    def subarvore_2(self):
        self.declare(Subarvore(2))

    @Rule(Sintoma(chiado=True), Sintoma(fuma=False), Sintoma(respiracao_rapida=False))
    def subarvore_3(self):
        self.declare(Subarvore(3))
    
    @Rule(Sintoma(chiado=True), Sintoma(fuma=False), Sintoma(respiracao_rapida=True))
    def subarvore_4(self):
        self.declare(Subarvore(4))

    @Rule(Sintoma(chiado=True), Sintoma(fuma=True), Sintoma(dor_no_peito=False))
    def subarvore_5(self):
        self.declare(Subarvore(5))

    @Rule(Sintoma(chiado=True), Sintoma(fuma=True), Sintoma(dor_no_peito=True))
    def subarvore_6(self):
        self.declare(Subarvore(6))

    # Identificando doenças

    @Rule( AND( OR( AND(Subarvore(1), OR(Sintoma(tossindo_sangue=True), Sintoma(olfato_paladar=True))),
                    AND(Subarvore(2), Sintoma(febre=True), Sintoma(dor_no_peito=False), Sintoma(olfato_paladar=True)) ))
         )
    def covid(self):
        self.declare(Doenca('COVID-19'))
    
    @Rule(Subarvore(1), Sintoma(tossindo_sangue=False), Sintoma(olfato_paladar=False), Sintoma(respiracao_rapida=True))
    def influenza(self):
        self.declare(Doenca('Influenza (Gripe Comum)'))

    @Rule( AND( Sintoma(olfato_paladar=False),
                OR( AND(Subarvore(1), Sintoma(tossindo_sangue=False), Sintoma(respiracao_rapida=False)),
                    AND(Subarvore(2), Sintoma(febre=True), Sintoma(dor_no_peito=False)) ))
         )
    def laringite(self):
        self.declare(Doenca('Laringite'))

    @Rule(Subarvore(2), Sintoma(febre=False))
    def rinosinusite(self):
        self.declare(Doenca('Rinosinusite'))

    @Rule(Subarvore(2), Sintoma(febre=True), Sintoma(dor_no_peito=True))
    def tuberculose(self):
        self.declare(Doenca('Tuberculose'))

    @Rule(Subarvore(3), Sintoma(dor_no_peito=False))
    def resfriado(self):
        self.declare(Doenca('Resfriado'))

    @Rule(Subarvore(3), Sintoma(dor_no_peito=True), Sintoma(tossindo_sangue=False))
    def bronquite_aguda(self):
        self.declare(Doenca('Bronquite'))

    @Rule(Subarvore(3), Sintoma(dor_no_peito=True), Sintoma(tossindo_sangue=True))
    def bronquiectasia(self):
        self.declare(Doenca('Bronquiectasia'))

    @Rule( AND (Subarvore(4),
                OR (Sintoma(tosse=0),
                    AND(Sintoma(tosse=1), NOT(Sintoma(febre=True)), Sintoma(batimentos_acelerados=True)) ))
         )
    def asma(self):
        self.declare(Doenca('Asma'))

    @Rule( AND (Subarvore(4), Sintoma(tosse=1),
                OR ( Sintoma(febre=True),
                     AND ( Sintoma(febre=False), Sintoma(batimentos_acelerados=False))))
         )
    def fibrose(self):
        self.declare(Doenca('Fibrose Cística'))

    @Rule(Subarvore(5), Sintoma(tosse=0))
    def bronquiolite(self):
        self.declare(Doenca('Bronquiolite'))

    @Rule(Subarvore(5), Sintoma(tosse=1))
    def dpoc(self):
        self.declare(Doenca('Doença Pulmonar Obstrutiva Crônica (DPOC)'))

    @Rule(Subarvore(6), Sintoma(tossindo_sangue=False), Sintoma(tosse=0))
    def doenca_pulmonar_ocupacional(self):
        self.declare(Doenca('Doença Pulmonar Ocupacional'))

    @Rule(Subarvore(6), Sintoma(tossindo_sangue=False), Sintoma(tosse=1))
    def pneumonia(self):
        self.declare(Doenca('Pneumonia'))

    @Rule(Subarvore(6), Sintoma(tossindo_sangue=True))
    def cancer_de_lingua(self):
        self.declare(Doenca('Câncer de Pulmão'))

    # Indicando diagnóstico
    @Rule(Doenca(MATCH.name))
    def diagnostico(self, name):
        print("\nVocê pode estar com: %s.\nEsta é uma ferramenta de estudos, se possuir sintomas procure atendimento médico.\n" % (name))




engine = IdentificaDoenca()
engine.reset()  # Preapara a engine para execução.
engine.run()  # Executa!

