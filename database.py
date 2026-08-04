import sqlite3

def conectar():
    """Cria a conexão com o banco de dados SQLite."""
    # O arquivo biblioteca.db será criado automaticamente se não existir
    conexao = sqlite3.connect("biblioteca.db")
    return conexao

def criar_tabelas():
    """Cria as tabelas necessárias para o sistema da biblioteca."""
    conexao = conectar()
    cursor = conexao.cursor()

    # 1. Tabela de Livros
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            ano_publicacao INTEGER,
            qtd_total INTEGER NOT NULL,
            qtd_disponivel INTEGER NOT NULL
        )
    ''')

    # 2. Tabela de Usuários (Ajustada para o projeto)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            identificacao TEXT NOT NULL,
            contato TEXT
        )
    ''')

    # 3. Tabela de Empréstimos
    # O status vai indicar se está "Ativo" (emprestado) ou "Devolvido"
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_livro INTEGER NOT NULL,
            id_usuario INTEGER NOT NULL,
            data_emprestimo TEXT NOT NULL,
            data_devolucao TEXT,
            status TEXT NOT NULL, 
            FOREIGN KEY (id_livro) REFERENCES livros (id),
            FOREIGN KEY (id_usuario) REFERENCES usuarios (id)
        )
    ''')

    # Salva as alterações e fecha a conexão
    conexao.commit()
    conexao.close()
    print("Banco de dados e tabelas criados com sucesso!")

# Este bloco faz com que as tabelas sejam criadas caso você rode este arquivo diretamente
if __name__ == "__main__":
    criar_tabelas()