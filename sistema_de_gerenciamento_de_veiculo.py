import json
# Importação do módulo json

class ManutenivelMixin:

    def __init__(self):
        # Lista que armazena o histórico de manutenções realizadas
        self._historico_manutencao = []
        # Status atual do objeto (ATIVO ou MANUTENÇÃO)
        self._status = "ATIVO"

    @property
    def status(self):
        # Propriedade para acesso controlado ao status do objeto
        return self._status

     # Criação de um dicionário contendo dados da manutenção
    def registrar_manutencao(self, data, tipo, custo, descricao):

         # Adiciona ao histórico de manutenções
        registro = {"data": data, "tipo": tipo, "custo": custo, "descrição": descricao}
        self._historico_manutencao.append(registro)

        self._status = "MANUTENÇÃO"

    def finalizar_manutencao(self):

        self._status = "ATIVO"

class AbastecivelMixin:

    def __init__(self, consumo_estimado):
        self._historico_abastecimentos = []
        self._consumo_estimado = consumo_estimado

class Veiculo(ManutenivelMixin, AbastecivelMixin):

    def __init__(self, placa, modelo, km, consumo_estimado):
        ManutenivelMixin.__init__(self)
        AbastecivelMixin.__init__(self, consumo_estimado)
        self._placa = placa
        self._modelo = modelo
        self._quilometragem = max(0, km)

    @property
    def placa(self):
        return self._placa
    
    @property
    # Propriedade para acesso ao atributo modelo
    def modelo(self):
        return self._modelo

    def __str__(self):
        return f"[{self._status}] {self._modelo} ({self._placa})"

class Carro(Veiculo):
    def __init__(self, placa, modelo, km, consumo_estimado):
        # Chamada construtor da classe base
        super().__init__(placa, modelo, km, consumo_estimado)
        # Identificação do tipo de veículo
        self.tipo = "Carro"
        # Categoria de CNH exigida
        self.cnh_requerida = "B"

class Moto(Veiculo):
    def __init__(self, placa, modelo, km, consumo_estimado):
        # Chamada construtor da classe base
        super().__init__(placa, modelo, km, consumo_estimado)
        # Identificação do tipo de veículo
        self.tipo = "Moto"
        # Categoria de CNH exigida
        self.cnh_requerida = "A"

class Pessoa:  

    def __init__(self, nome, cpf):
        # Atributos privados da pessoa
        self._nome = nome
        self._cpf = cpf

class Motorista(Pessoa):
    pass



