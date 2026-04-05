from modelos_bd import sessao, Partida


class JogoDeXadrez:
    def __init__(self, id_partida):
        self.id_partida = id_partida
        self.tabuleiro = []
        self.turno_atual = "brancas"

        self.carregar_estado_da_base_dados()

    def carregar_estado_da_base_dados(self):
        partida = sessao.query(Partida).filter_by(id=self.id_partida).first()

        if partida:
            self.turno_atual = partida.turno_atual
            self.fen_para_matriz(partida.estado_fen)
        else:
            print("Erro: Partida não encontrada na base de dados!")

    def guardar_estado_na_base_dados(self):
        partida = sessao.query(Partida).filter_by(id=self.id_partida).first()

        if partida:
            partida.estado_fen = self.matriz_para_fen()
            partida.turno_atual = self.turno_atual

            sessao.commit()

    def fen_para_matriz(self, fen):
        self.tabuleiro = []
        linhas_fen = fen.split('/')

        for linha in linhas_fen:
            linha_matriz = []
            for char in linha:
                if char.isdigit():
                    for _ in range(int(char)):
                        linha_matriz.append('--')
                else:
                    linha_matriz.append(char)
            self.tabuleiro.append(linha_matriz)

    def matriz_para_fen(self):
        fen = ""
        for linha in self.tabuleiro:
            casas_vazias = 0
            for peca in linha:
                if peca == '--':
                    casas_vazias += 1
                else:
                    if casas_vazias > 0:
                        fen += str(casas_vazias)
                        casas_vazias = 0
                    fen += peca
            if casas_vazias > 0:
                fen += str(casas_vazias)
            fen += "/"

        return fen[:-1]

    def fazer_movimento(self, origem, destino):
        linha_origem, col_origem = origem
        linha_destino, col_destino = destino

        peca_movida = self.tabuleiro[linha_origem][col_origem]

        if peca_movida == '--':
            return False

        self.tabuleiro[linha_destino][col_destino] = peca_movida
        self.tabuleiro[linha_origem][col_origem] = '--'

        self.turno_atual = "pretas" if self.turno_atual == "brancas" else "brancas"

        self.guardar_estado_na_base_dados()

        return True