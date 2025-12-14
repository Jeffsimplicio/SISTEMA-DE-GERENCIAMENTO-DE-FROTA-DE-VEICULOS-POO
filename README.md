# SISTEMA-DE-GERENCIAMENTO-DE-FROTA-DE-VEICULOS-POO

[Nome do Membro 1]	Domínio: Classes Veiculo, Herança, Mixins (AbastecivelMixin, ManutenivelMixin).
[Nome do Membro 2]	Infraestrutura: Repositórios (JsonRepository), Leitura de settings.json.
[Nome do Membro 3]	Serviço/Aplicação: FrotaService, Validações de CNH e Estados, Relatórios.

   Sistema de Gerenciamento de Frota de Veículos (UFCA - ADS)
   
Este projeto implementa um Sistema de Gerenciamento de Frota de Veículos utilizando Python e aplicando conceitos avançados de Programação Orientada a Objetos (POO), herança (simples e múltipla) e padrões de projeto para desacoplar a persistência e a lógica de negócios.
   
   Requisitos Técnicos e Ferramentas
•	Linguagem: Python
•	POO Avançada: Encapsulamento, Herança (simples e múltipla/Mixins), Métodos Especiais (__str__, __eq__, etc.).
•	Persistência: JSON (Opção de extensão para SQLite).
•	Interface: CLI (Linha de Comando) ou API mínima (FastAPI/Flask - opcional).
•	Configurações: settings.json para regras de negócio configuráveis.

   Estrutura do Projeto (Decisões de Design)
•	O sistema é dividido em três camadas principais para garantir o desacoplamento e a aplicação do padrão Repository.
--	1. Camada de Domínio (Entidades e Mixins)
•	Contém a lógica central e os dados.

Classe                   -	Descrição                                         -	Principais Atributos                      - Herança/Mixins Aplicados
Pessoa	                 - Classe base para pessoas.                          - _nome, _cpf	
Motorista                - Gerencia dados e histórico do motorista.	          -_categoria_cnh, _tempo_experiencia	        - Herda de Pessoa 
Veiculo	                 - Classe base para todos os veículos (Abstrata).	    - _placa, _modelo, _status, _quilometragem	
Carro / Moto / Caminhao  - Classes concretas de veículos.	                    - Herdam de Veiculo	                        - Herdam de Veiculo
AbastecivelMixin	       - Adiciona funcionalidades de registro de consumo.	  - Histórico de Abastecimentos	              - Herança Múltipla 
ManutenivelMixin	       - Adiciona controle de status (ATIVO/MANUTENCAO).	  - Histórico de Manutenções	                - Herança Múltipla 

--  2. Camada de Infraestrutura (Persistência)
Gerencia a leitura e escrita de dados.
•	Padrão Repository: Utilizamos o padrão Repository para abstrair a fonte de dados do domínio.
•	Repository (Interface): Define os métodos CRUD (Criar, Ler, Atualizar, Excluir).
•	JsonRepository: Implementação que utiliza arquivos JSON para persistência dos dados.

--  3. Camada de Serviço/Aplicação
Contém a lógica de negócios, validações e coordenação.
•	Configuracoes: Carrega parâmetros de settings.json, como limite_km_revisao e cnh_minima_por_tipo_veiculo.
•	FrotaService: Responsável por aplicar as Regras de Negócio:
  o	Validação de compatibilidade de CNH com o tipo de veículo.
  o	Bloqueio de alocação se o veículo estiver em manutenção.
  o	Cálculo e geração de Relatórios (custos médios, ranking de eficiência).

Regras de Negócio Essenciais
O sistema aplica as seguintes políticas configuráveis:
•	Compatibilidade CNH: A alocação é bloqueada se a categoria da CNH não for compatível com o tipo de veículo (Ex: Moto exige "A", Carro exige "B").
•	Revisão Preventiva: Gera um alerta se a quilometragem ultrapassar o limite configurado em settings.json (padrão: 10.000 km).
•	Consumo Fora da Faixa: Veículos com consumo médio fora da faixa configurada geram um alerta de desempenho.
•	Transição de Estados: O status do veículo segue o fluxo: ATIVO ↔ MANUTENCAO, ou ATIVO → INATIVO.

Explicação do Diagrama UML
Este diagrama ilustra como os principais conceitos de POO serão aplicados no projeto:
•	Herança Simples:
  o	Motorista herda atributos e métodos de Pessoa.
  o	Carro, Moto, e Caminhao herdam as propriedades básicas de gerenciamento de frotas de Veiculo.
•	Herança Múltipla (Mixins):
  o	As classes de veículos concretas (Carro, Moto, Caminhao) herdam de Veiculo e também utilizam os Mixins:
    .	ManutenivelMixin: Adiciona a funcionalidade de registro de manutenção e controle de status.
    .	AbastecivelMixin: Adiciona a funcionalidade de registro de abastecimentos e cálculo de consumo.
•	Associação:
  o	As classes de registro de eventos (Manutencao, Abastecimento) estão associadas a Veiculo.
•	Padrão Repository:
  o	O JsonRepository implementa a interface Repository.
