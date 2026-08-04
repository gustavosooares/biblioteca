import tkinter as tk
import database
import controllers
from views import LivroView

class BibliotecaController:
    """
    Ponte entre a Interface Gráfica (views) e o Banco de Dados (controllers).
    Nenhuma regra de negócio é feita aqui, ele apenas repassa os dados.
    """
    
    # --- LIVROS ---
    def adicionar_livro(self, titulo, autor, ano, qtd_total):
        # Se deixarem a quantidade vazia, dá erro. Para evitar que o sistema quebre,
        # tentamos converter para int. Se não conseguir, mandamos erro.
        try:
            qtd_num = int(qtd_total)
        except ValueError:
            return False, "A quantidade deve ser um número válido!"
            
        return controllers.cadastrar_livro(titulo, autor, ano, qtd_num)

    def buscar_livros(self, termo):
        status, resultados = controllers.buscar_livros(termo)
        if status:
            livros_formatados = []
            for linha in resultados:
                # O banco envia: (id, titulo, autor, ano, qtd_total, qtd_disponivel)
                # Vamos enviar para a interface apenas as colunas que importam:
                livros_formatados.append((linha[0], linha[1], linha[2], linha[3], linha[5]))
            return livros_formatados
        return []
    def obter_lista_livros(self):
        """Retorna uma lista formatada 'ID - Título' para o Combobox"""
        status, resultados = controllers.buscar_livros("")
        if status:
            return [f"{linha[0]} - {linha[1]}" for linha in resultados]
        return []

    def obter_lista_usuarios(self):
        """Retorna uma lista formatada 'ID - Nome' para o Combobox"""
        status, resultados = controllers.listar_usuarios()
        if status:
            return [f"{linha[0]} - {linha[1]}" for linha in resultados]
        return []

    # --- USUÁRIOS ---
    def adicionar_usuario(self, nome, ident, contato):
        return controllers.cadastrar_usuario(nome, ident, contato)

    # --- EMPRÉSTIMOS E DEVOLUÇÕES ---
    def registrar_emprestimo(self, id_livro, id_usuario):
        return controllers.emprestar_livro(id_livro, id_usuario)

    def registrar_devolucao(self, id_livro, id_usuario):
        return controllers.devolver_livro(id_livro, id_usuario)

    # --- RELATÓRIOS ---
    def gerar_relatorio_disponiveis(self):
        return controllers.relatorio_livros_disponiveis()

    def gerar_relatorio_emprestados(self):
        return controllers.relatorio_livros_emprestados()


def main():
    # 1. Cria o banco de dados e as tabelas caso não existam
    database.criar_tabelas()

    # 2. Cria a janela do Tkinter
    root = tk.Tk()

    # 3. Inicia o controlador e a View
    app_controller = BibliotecaController()
    app = LivroView(root, controller=app_controller)

    # 4. Mantém o sistema rodando
    root.mainloop()

if __name__ == "__main__":
    main()