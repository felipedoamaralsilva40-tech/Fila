class AFD:
    def __init__(self, estados, alfabeto, inicial, finais, transicoes, nome="AFD"):
        self.estados = set(estados)
        self.alfabeto = set(alfabeto)
        self.inicial = inicial
        self.finais = set(finais)
        self.transicoes = dict(transicoes)
        self.nome = nome

    def executar(self, palavra, mostrar_passos=False):
        estado = self.inicial
        passos = [estado]
        for caractere in palavra:
            destino = self.transicoes.get((estado, caractere))
            if destino is None:
                if mostrar_passos:
                    return False, passos, f"Não existe transição de {estado} lendo {caractere!r}."
                return False
            estado = destino
            passos.append(estado)
        aceita = estado in self.finais
        if mostrar_passos:
            motivo = "Entrada aceita." if aceita else f"A entrada terminou em {estado}, que não é estado final."
            return aceita, passos, motivo
        return aceita

    def tabela(self):
        simbolos = sorted(self.alfabeto)
        linhas = [f"AFD: {self.nome}", "Estado | " + " | ".join(simbolos)]
        for estado in sorted(self.estados):
            inicio = "-> " if estado == self.inicial else "   "
            final = " *" if estado in self.finais else ""
            destinos = [str(self.transicoes.get((estado, s), "-")) for s in simbolos]
            linhas.append(inicio + estado + final + " | " + " | ".join(destinos))
        return "\n".join(linhas)

    # Estados: início, depois da letra, depois de 1, 2 e 3 dígitos, e erro.
estados_senha = ["q0", "q1", "q2", "q3", "q4", "erro"]
alfabeto_senha = set("PN0123456789?")
transicoes_senha = {}

transicoes_senha[("q0", "P")] = "q1"
transicoes_senha[("q0", "N")] = "q1"
for c in alfabeto_senha - {"P", "N"}:
    transicoes_senha[("q0", c)] = "erro"

for c in "0123456789":
    transicoes_senha[("q1", c)] = "q2"
    transicoes_senha[("q2", c)] = "q3"
    transicoes_senha[("q3", c)] = "q4"

for estado in ["q1", "q2", "q3"]:
    for c in alfabeto_senha:
        transicoes_senha.setdefault((estado, c), "erro")
for c in alfabeto_senha:
    transicoes_senha[("q4", c)] = "erro"
    transicoes_senha[("erro", c)] = "erro"

afd_senha = AFD(estados_senha, alfabeto_senha, "q0", {"q4"}, transicoes_senha, "Senha P000 ou N000")

def validar_senha(texto, mostrar_passos=False):
    # Caracteres desconhecidos são convertidos para ? para garantir rejeição.
    convertido = "".join(c if c in alfabeto_senha else "?" for c in texto)
    return afd_senha.executar(convertido, mostrar_passos)

print(afd_senha.tabela())
print("\nP042:", validar_senha("P042"))
print("N117:", validar_senha("N117"))
print("X042:", validar_senha("X042"))
print("P42:", validar_senha("P42"))