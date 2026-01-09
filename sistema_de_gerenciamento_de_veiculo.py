import json


class ManutenivelMixin:
    # MIXIN PARA ADICIONAR FUNCIONALIDADES DE REGISTRO DE MANUTENÇÃO E CONTROLE DE STATUS.
    def __init__(self):
        self._historico_manutencao = []
        self._status = "ATIVO"

    @property
    def status(self):
        return self._status

    def registrar_manutencao(self, data, tipo, custo, descricao):
        # REGISTRA UMA MANUTENÇÃO E ALTERA O STATUS DO VEÍCULO
        registro = {"data": data, "tipo": tipo, "custo": custo, "descricao": descricao}
        self._historico_manutencao.append(registro)
        # SE A MANUTENÇÃO FOR PREVENTIVA OU CORRETIVA, O VEÍCULO FICA EM MANUTENÇÃO.
        self._status = "MANUTENCAO"

    def finalizar_manutencao(self):
        # RETORNA O VEÍCULO AO ESTADO ATIVO APÓS O SERVIÇO.
        self._status = "ATIVO"

class AbastecivelMixin:
    # MIXIN PARA ADICIONAR FUNCIONALIDADES DE REGISTRO DE ABASTECIMENTOS E CONSUMO.
    def __init__(self, consumo_estimado):
        self._historico_abastecimentos = []
        self._consumo_estimado = consumo_estimado

#  CAMADA DE DOMÍNIO (ENTIDADES E REGRAS DE NEGÓCIO)

class Veiculo(ManutenivelMixin, AbastecivelMixin):
    
    #CLASSE BASE PARA TODOS OS VEÍCULOS.
    
    def __init__(self, placa, modelo, km, consumo_estimado):
        ManutenivelMixin.__init__(self)
        AbastecivelMixin.__init__(self, consumo_estimado)
        self._placa = placa
        self._modelo = modelo
        self._quilometragem = max(0, km)

    @property
    def placa(self): return self._placa
    
    @property
    def modelo(self): return self._modelo

    def __str__(self):
        return f"[{self._status}] {self._modelo} ({self._placa})"

class Carro(Veiculo):
    def __init__(self, placa, modelo, km, consumo_estimado):
        super().__init__(placa, modelo, km, consumo_estimado)
        self.tipo = "Carro"
        self.cnh_requerida = "B"

class Moto(Veiculo):
    def __init__(self, placa, modelo, km, consumo_estimado):
        super().__init__(placa, modelo, km, consumo_estimado)
        self.tipo = "Moto"
        self.cnh_requerida = "A"

class Pessoa:  
    # CLASSE BASE PARA PESSOAS (APLICANDO HERANÇA SIMPLES).
    def __init__(self, nome, cpf):
        self._nome = nome
        self._cpf = cpf

class Motorista(Pessoa):
    # GERENCIA DADOS DO MOTORISTA E VALIDAÇÕES DE ALOCAÇÃO.
    def __init__(self, nome, cpf, categoria_cnh):
        super().__init__(nome, cpf)
        self._categoria_cnh = categoria_cnh.upper()

    @property
    def categoria_cnh(self): return self._categoria_cnh

    def pode_dirigir(self, veiculo):
        
        #REGRA DE NEGÓCIO: VALIDA SE O MOTORISTA TEM A CNH CORRETA PARA O VEÍCULO.
        #TAMBÉM BLOQUEIA SE O VEÍCULO ESTIVER EM MANUTENÇÃO.
        
        # 1. VALIDAÇÃO DE STATUS DO VEÍCULO
        if veiculo.status == "MANUTENCAO":
            return False, "VEÍCULO EM MANUTENÇÃO. ALOCAÇÃO BLOQUEADA."

        # 2. VALIDAÇÃO DE CATEGORIA DE CNH (SIMPLIFICADA)
        if self._categoria_cnh == veiculo.cnh_requerida:
            return True, "ALOCAÇÃO AUTORIZADA."
        
        return False, f"CNH CATEGORIA '{self._categoria_cnh}' INCOMPATÍVEL COM O VEÍCULO."
    
#  CAMADA DE INFRAESTRUTURA (PERSISTÊNCIA) 
class JsonRepository: 
    # GERENCIA O SALVAMENTO DE DADOS EM ARQUIVO JSON.
    def __init__(self, arquivo="frota.json"):
        self.arquivo = arquivo

    def salvar_alocacao(self, motorista, veiculo):
        # SIMULA O SALVAMENTO DE UMA VIAGEM OU ALOCAÇÃO.
        autorizado, mensagem = motorista.pode_dirigir(veiculo)
        
        if autorizado:
            dados = {
                "motorista": motorista._nome,
                "veiculo": veiculo.placa,
                "status": "SUCESSO"
            }
            with open(self.arquivo, 'a', encoding='utf-8') as arquivo:
                json.dump(dados, arquivo, indent=4, ensure_ascii=False)
                arquivo.write('\n')
        
        return autorizado, mensagem

# TESTE 
if __name__ == "__main__":
    # 1. CADASTRO DE VEÍCULOS
    meu_carro = Carro("BRA2E19", "COROLLA", 20000, 12.0)
    minha_moto = Moto("UFC-2024", "HONDA CB500", 5000, 22.0)

    # 2. CADASTRO DE MOTORISTAS
    motorista_carro = Motorista("JOÃO SILVA", "123.456.789-00", "B")
    motorista_moto = Motorista("ANA COSTA", "987.654.321-11", "A")

    print("--- TESTES DE VALIDAÇÃO DE ALOCAÇÃO ---")

    # TESTE 1: ALOCAÇÃO CORRETA (CARRO -> CNH B)
    ok, msg = motorista_carro.pode_dirigir(meu_carro)
    print(f"MOTORISTA {motorista_carro._nome} -> {meu_carro.modelo}: {msg}")

    # TESTE 2: ALOCAÇÃO INCORRETA (MOTO -> CNH B)
    ok, msg = motorista_carro.pode_dirigir(minha_moto)
    print(f"MOTORISTA {motorista_carro._nome} -> {minha_moto.modelo}: {msg}")

    # TESTE 3: VEÍCULO EM MANUTENÇÃO
    print("\n--- TESTE DE MANUTENÇÃO ---")
    minha_moto.registrar_manutencao("2025-12-28", "preventiva", 300, "TROCA DE PNEU")
    ok, msg = motorista_moto.pode_dirigir(minha_moto)
    print(f"MOTORISTA {motorista_moto._nome} -> {minha_moto.modelo}: {msg}")

    # 3. PERSISTÊNCIA NO JSON
    repo = JsonRepository()
    repo.salvar_alocacao(motorista_carro, meu_carro)
    print("\nLOG DE ALOCAÇÃO SALVO NO ARQUIVO JSON COM SUCESSO.")