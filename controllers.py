from database import conectar
from datetime import date

# ================= ÁREA DE LIVROS =================
def cadastrar_livro(titulo, autor, ano_publicacao, qtd_total):
    if not titulo or not autor:
        return False, "Título e Autor são obrigatórios!"
    if int(qtd_total) <= 0:
        return False, "A quantidade deve ser maior que zero!"

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        qtd_disponivel = qtd_total
        sql = "INSERT INTO livros (titulo, autor, ano_publicacao, qtd_total, qtd_disponivel) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(sql, (titulo, autor, ano_publicacao, qtd_total, qtd_disponivel))
        conexao.commit()
        return True, "Livro cadastrado com sucesso!"
    except Exception as e:
        return False, f"Erro no banco de dados: {e}"
    finally:
        conexao.close()

def buscar_livros(termo_busca=""):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        if termo_busca == "":
            cursor.execute("SELECT * FROM livros")
        else:
            sql = "SELECT * FROM livros WHERE titulo LIKE ? OR autor LIKE ? OR ano_publicacao LIKE ?"
            parametro = f"%{termo_busca}%"
            cursor.execute(sql, (parametro, parametro, parametro))
        return True, cursor.fetchall()
    except Exception as e:
        return False, f"Erro ao buscar: {e}"
    finally:
        conexao.close()


# ================= ÁREA DE USUÁRIOS =================
def cadastrar_usuario(nome, identificacao, contato):
    if not nome or not identificacao:
        return False, "Nome e Identificação são obrigatórios!"
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = "INSERT INTO usuarios (nome, identificacao, contato) VALUES (?, ?, ?)"
        cursor.execute(sql, (nome, identificacao, contato))
        conexao.commit()
        return True, "Usuário cadastrado com sucesso!"
    except Exception as e:
        return False, f"Erro ao cadastrar usuário: {e}"
    finally:
        conexao.close()

def listar_usuarios():
    """Busca todos os usuários para preencher a caixa de seleção na interface."""
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome FROM usuarios")
        return True, cursor.fetchall()
    except Exception as e:
        return False, f"Erro ao listar usuários: {e}"
    finally:
        conexao.close()

# ================= ÁREA DE EMPRÉSTIMOS E DEVOLUÇÕES =================
def emprestar_livro(id_livro, id_usuario):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        cursor.execute("SELECT qtd_disponivel FROM livros WHERE id = ?", (id_livro,))
        resultado = cursor.fetchone()
        
        if not resultado:
            return False, "Erro: Livro não encontrado no sistema."
        
        if resultado[0] <= 0:
            return False, "Aviso: Nenhuma cópia disponível no momento."
            
        data_hoje = date.today().strftime("%d/%m/%Y")
        cursor.execute("INSERT INTO emprestimos (id_livro, id_usuario, data_emprestimo, status) VALUES (?, ?, ?, 'Ativo')", (id_livro, id_usuario, data_hoje))
        cursor.execute("UPDATE livros SET qtd_disponivel = qtd_disponivel - 1 WHERE id = ?", (id_livro,))
        
        conexao.commit()
        return True, "Empréstimo realizado com sucesso!"
    except Exception as e:
        return False, f"Erro no empréstimo: {e}"
    finally:
        conexao.close()

def devolver_livro(id_livro, id_usuario):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        cursor.execute("SELECT id FROM emprestimos WHERE id_livro = ? AND id_usuario = ? AND status = 'Ativo'", (id_livro, id_usuario))
        resultado = cursor.fetchone()
        
        if not resultado:
            return False, "Nenhum empréstimo ativo encontrado."
            
        id_emprestimo = resultado[0]
        data_hoje = date.today().strftime("%d/%m/%Y")
        
        cursor.execute("UPDATE emprestimos SET status = 'Devolvido', data_devolucao = ? WHERE id = ?", (data_hoje, id_emprestimo))
        cursor.execute("UPDATE livros SET qtd_disponivel = qtd_disponivel + 1 WHERE id = ?", (id_livro,))
        
        conexao.commit()
        return True, "Devolução confirmada com sucesso!"
    except Exception as e:
        return False, f"Erro na devolução: {e}"
    finally:
        conexao.close()


# ================= ÁREA DE RELATÓRIOS =================
def relatorio_livros_disponiveis():
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT id, titulo, autor, qtd_disponivel FROM livros WHERE qtd_disponivel > 0")
        return True, cursor.fetchall()
    except Exception as e:
        return False, f"Erro: {e}"
    finally:
        conexao.close()

def relatorio_livros_emprestados():
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = '''
            SELECT e.id, l.titulo, u.nome, e.data_emprestimo 
            FROM emprestimos e
            JOIN livros l ON e.id_livro = l.id
            JOIN usuarios u ON e.id_usuario = u.id
            WHERE e.status = 'Ativo'
        '''
        cursor.execute(sql)
        return True, cursor.fetchall()
    except Exception as e:
        return False, f"Erro: {e}"
    finally:
        conexao.close()