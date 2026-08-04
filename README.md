# 📚 Sistema Integrado de Biblioteca

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey.svg)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-orange.svg)

Este é um sistema de gerenciamento de biblioteca desenvolvido como Projeto Integrador para o curso Ciência de Dados na Anhanguera. 

O objetivo do projeto é aplicar conceitos de Programação Orientada a Objetos (POO), arquitetura de software (MVC) e manipulação de banco de dados relacional usando apenas bibliotecas nativas do Python.

---

## ✨ Funcionalidades

O sistema atende a todos os requisitos acadêmicos propostos, incluindo:

- **Cadastro de Livros:** Inserção de novos títulos com informações de autor, ano e quantidade de exemplares em estoque.
- **Cadastro de Usuários:** Registro de leitores com nome, número de identificação (matrícula/CPF) e contato.
- **Controle de Empréstimos:** 
  - Seleção dinâmica de livros e usuários.
  - Validação automática de disponibilidade em estoque.
  - Baixa automática da quantidade de cópias disponíveis ao realizar o empréstimo.
- **Controle de Devoluções:** Restauração da quantidade de exemplares em estoque quando o livro é devolvido.
- **Consultas Dinâmicas:** Busca de livros por título ou autor usando uma interface de tabela atualizada em tempo real.
- **Relatórios:** Telas dedicadas para visualização instantânea de livros com cópias disponíveis e histórico de empréstimos ativos.

---

## 🛠️ Tecnologias Utilizadas

O projeto foi construído focando em leveza e uso de bibliotecas padrão (Standard Library) do Python, dispensando a necessidade de instalar dependências externas complexas (sem necessidade de `pip install`).

* **Linguagem:** Python 3
* **Interface Gráfica (GUI):** Tkinter (com módulo `ttk` e tema "clam" para design moderno e responsivo)
* **Banco de Dados:** SQLite3 (banco de dados local, integrado no próprio projeto)

---

## 🏗️ Arquitetura do Projeto

O código foi estruturado inspirado no padrão **MVC (Model-View-Controller)**, dividindo responsabilidades para aplicar as boas práticas de Engenharia de Software:

```text
/
├── main.py           # (Controller principal) Inicia a aplicação e conecta a Interface com o Backend.
├── database.py       # (Model/DB) Responsável por criar e conectar ao banco de dados SQLite.
├── controllers.py    # (Regras de Negócio) Executa as lógicas de validação, empréstimos e queries SQL.
└── views.py          # (View) Contém apenas os elementos visuais (janelas, botões, tabelas) em Tkinter.
