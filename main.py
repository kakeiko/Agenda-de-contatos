from tkinter import *
from tkinter import ttk
import sqlite3 as sq

corFundo='#33605a'
corFrame='#e9e0d1'
corBorda='#91a398'
corbotao='#68462b'
janela = Tk()

class funcao():
    def limpa_tela(self):
        self.id_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.numero_entry.delete(0, END)
        self.email_entry.delete(0, END)
    def conecta_bd(self):
        self.conn = sq.connect("contatos.db")
        self.cursor = self.conn.cursor()
    def desconecta_bd(self):
        self.conn.close()
    def monta_tabelas(self):
        self.conecta_bd()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS contatos (
                cod INTEGER PRIMARY KEY,
                nome CHAR(40) NOT NULL,
                numero INTEGER(20),
                email CHAR(40)
            );
        """)
        self.conn.commit()
        self.desconecta_bd()
    def variaveis(self):
        self.id = self.id_entry.get()
        self.nome = self.nome_entry.get()
        self.numero = self.numero_entry.get()
        self.email = self.email_entry.get()
    def add_contato(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" INSERT INTO contatos (nome, numero, email)
            VALUES (?, ?, ?)""", (self.nome, self.numero, self.email))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()
    def select_lista(self):
        self.lista_cont.delete(*self.lista_cont.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, nome, numero, email FROM contatos
            ORDER BY nome ASC; """)
        for i in lista:
            self.lista_cont.insert("", END, values=i)
        self.desconecta_bd()
    def onDoubleClick(self, event):
        self.limpa_tela()
        self.lista_cont.selection()

        for n in self.lista_cont.selection():
            col1, col2, col3, col4 = self.lista_cont.item(n, 'values')
            self.id_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.numero_entry.insert(END, col3)
            self.email_entry.insert(END, col4)
    def deleta_contato(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM contatos WHERE cod = ? """, [self.id])
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()
    def editar_contato(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE contatos SET nome = ?, numero = ?, email = ?
            WHERE cod = ? """, (self.nome, self.numero, self.email, self.id))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()
    def busca_contato(self):
        self.conecta_bd()
        self.lista_cont.delete(*self.lista_cont.get_children())

        self.nome_entry.insert(END, '%')
        nome = self.nome_entry.get()
        self.cursor.execute(""" SELECT cod, nome, numero, email FROM contatos
            WHERE nome LIKE '%s' ORDER BY nome ASC""" % nome)
        buscarnome_cont = self.cursor.fetchall()
        for i in buscarnome_cont:
            self.lista_cont.insert('', END, values=i)

        self.limpa_tela()
        self.desconecta_bd()


class aplicativo(funcao):
    def __init__(self):
        self.janela = janela
        self.janelaop()
        self.frames_da_janela()
        self.gadgets()
        self.lista_frame_baixo()
        self.monta_tabelas()
        self.select_lista()
        self.menus()
        janela.mainloop()
    def janelaop(self):
        self.janela.title('Agenda de contatos')
        self.janela.configure(bg= corFundo)
        self.janela.geometry("700x500")
        self.janela.resizable(True, True)
        self.janela.maxsize(width=900, height=700)
        self.janela.minsize(width=600, height=400)
    def frames_da_janela(self):
        self.frame_cima = Frame(self.janela, bd=4, bg= corFrame, highlightbackground=corBorda, highlightthickness=3)
        self.frame_cima.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame_baixo = Frame(self.janela, bd=4, bg= corFrame, highlightbackground=corBorda, highlightthickness=3)
        self.frame_baixo.place(relx=0.02, rely=0.51, relwidth=0.96, relheight=0.46)
    def gadgets(self):
        self.b_buscar = Button(self.frame_cima,command=self.busca_contato, text='Buscar', bg=corbotao, fg=corFrame, font=('Ivy 10 bold'))
        self.b_buscar.place(relx=0.2, rely=0.15, relwidth=0.1, relheight=0.1)
        self.b_limpar = Button(self.frame_cima,command= self.limpa_tela, text='Limpar', bg=corbotao, fg=corFrame, font=('Ivy 10 bold'))
        self.b_limpar.place(relx=0.32, rely=0.15, relwidth=0.1, relheight=0.1)
        self.b_novo = Button(self.frame_cima,command= self.add_contato, text='Novo', bg=corbotao, fg=corFrame, font=('Ivy 10 bold'))
        self.b_novo.place(relx=0.6, rely=0.15, relwidth=0.1, relheight=0.1)
        self.b_excluir = Button(self.frame_cima,command=self.deleta_contato, text='Excluir', bg=corbotao, fg=corFrame, font=('Ivy 10 bold'))
        self.b_excluir.place(relx=0.72, rely=0.15, relwidth=0.1, relheight=0.1)
        self.b_editar = Button(self.frame_cima,command=self.editar_contato, text='Editar', bg=corbotao, fg=corFrame, font=('Ivy 10 bold'))
        self.b_editar.place(relx=0.84, rely=0.15, relwidth=0.1, relheight=0.1)

        self.lb_id = Label(self.frame_cima, text='ID', font='verdana 12 bold', bg=corFrame)
        self.lb_id.place(relx=0.06, rely=0.05)
        self.lb_nome = Label(self.frame_cima, text='Nome', font='verdana 12 bold', bg=corFrame)
        self.lb_nome.place(relx=0.06, rely=0.35)
        self.lb_numero = Label(self.frame_cima, text='Número', font='verdana 12 bold', bg=corFrame)
        self.lb_numero.place(relx=0.06, rely=0.65)
        self.lb_email = Label(self.frame_cima, text='E-mail', font='verdana 12 bold', bg=corFrame)
        self.lb_email.place(relx=0.5, rely=0.65)

        self.id_entry = Entry(self.frame_cima)
        self.id_entry.place(relx=0.06, rely=0.16, relwidth= 0.12)
        self.nome_entry = Entry(self.frame_cima)
        self.nome_entry.place(relx=0.06, rely=0.46, relwidth= 0.6)
        self.numero_entry = Entry(self.frame_cima)
        self.numero_entry.place(relx=0.06, rely=0.76, relwidth= 0.3)
        self.email_entry = Entry(self.frame_cima)
        self.email_entry.place(relx=0.5, rely=0.76, relwidth= 0.4)
    def lista_frame_baixo(self):
        self.lista_cont = ttk.Treeview(self.frame_baixo, height= 3, column=('col1', 'col2', 'col3','col4'))
        self.lista_cont.heading('#0', text='')
        self.lista_cont.heading('#1', text='Id')
        self.lista_cont.heading('#2', text='Nome')
        self.lista_cont.heading('#3', text='Número')
        self.lista_cont.heading('#4', text='E-mail')

        self.lista_cont.column('#0', width=1)
        self.lista_cont.column('#1', width=50)
        self.lista_cont.column('#2', width=175)
        self.lista_cont.column('#3', width=125)
        self.lista_cont.column('#4', width=150)

        self.lista_cont.place(relx=0.02, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scrool_lista = Scrollbar(self.frame_baixo, orient='vertical')
        self.lista_cont.configure(yscroll=self.scrool_lista.set)
        self.scrool_lista.place(relx=0.96, rely=0.1, relwidth=0.02, relheight=0.85)
        self.lista_cont.bind("<Double-1>", self.onDoubleClick)
    def menus(self):
        menubar = Menu(self.janela)
        self.janela.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def quit(): self.janela.destroy()

        menubar.add_cascade(label= "Opções", menu= filemenu)

        filemenu.add_command(label="Sair", command= quit)
        filemenu.add_command(label="Limpar", command= self.limpa_tela)




aplicativo()