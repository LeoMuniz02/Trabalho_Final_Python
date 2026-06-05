"""
Sistema de Registro de Notas
Disciplina: Desenvolvimento Rápido de Aplicações em Python
Curso: CCP / ADS
"""

import tkinter as tk
from tkinter import ttk, messagebox
import database as db


# ─── Paleta de cores — Seleção Brasileira 🇧🇷 ──────────────────────────────────
BG        = "#0a3d0a"   # verde escuro principal (fundo)
PANEL     = "#0f5c0f"   # verde médio (painéis/cards)
ACCENT    = "#FFD700"   # amarelo ouro (destaques, títulos)
ACCENT2   = "#1a5cb8"   # azul CBF (seleção de linha na tabela)
SUCCESS   = "#00c41c"   # verde vivo (aprovado / botão Cadastrar)
DANGER    = "#e63030"   # vermelho (reprovado / botão Excluir)
WARNING   = "#FFD700"   # amarelo ouro (recuperação / botão Buscar)
TEXT      = "#fffde7"   # branco-amarelado (texto principal)
MUTED     = "#a5d6a7"   # verde claro (labels secundários)
BORDER    = "#1e7a1e"   # verde borda
ENTRY_BG  = "#0a3d0a"   # mesmo fundo para os campos


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Registro de Notas")
        self.geometry("1000x680")
        self.resizable(True, True)
        self.configure(bg=BG)

        db.inicializar_banco()
        self._build_ui()
        self.listar_alunos()

    # ── Layout principal ──────────────────────────────────────────────────────
    def _build_ui(self):
        # Cabeçalho
        header = tk.Frame(self, bg=PANEL, height=64)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text="🇧🇷  Sistema de Registro de Notas",
            font=("Courier New", 16, "bold"),
            bg=PANEL, fg=ACCENT
        ).pack(side="left", padx=24, pady=14)

        tk.Label(
            header, text=db.BACKEND_LABEL,
            font=("Courier New", 10),
            bg=PANEL, fg=MUTED
        ).pack(side="right", padx=24)

        # Container principal
        main = tk.Frame(self, bg=BG)
        main.pack(fill="both", expand=True, padx=20, pady=16)

        # Formulário (esquerda)
        self._build_form(main)

        # Tabela (direita)
        self._build_table(main)

        # Botões de ação
        self._build_actions(main)

    # ── Formulário ────────────────────────────────────────────────────────────
    def _build_form(self, parent):
        form = tk.Frame(parent, bg=PANEL, bd=0, relief="flat")
        form.pack(side="left", fill="y", padx=(0, 16), pady=0, ipadx=16, ipady=16)

        tk.Label(form, text="DADOS DO ALUNO", font=("Courier New", 11, "bold"),
                 bg=PANEL, fg=ACCENT).grid(row=0, column=0, columnspan=2,
                                           pady=(8, 16), sticky="w", padx=8)

        campos = [
            ("Nome completo", "entry_nome"),
            ("Matrícula",     "entry_matricula"),
            ("Disciplina",    "entry_disciplina"),
            ("Nota 1",        "entry_nota1"),
            ("Nota 2",        "entry_nota2"),
            ("Nota 3",        "entry_nota3"),
        ]

        for i, (label, attr) in enumerate(campos, start=1):
            tk.Label(form, text=label, font=("Courier New", 10),
                     bg=PANEL, fg=MUTED).grid(
                row=i, column=0, sticky="w", padx=8, pady=4)

            entry = tk.Entry(form, bg=ENTRY_BG, fg=TEXT,
                             insertbackground=ACCENT,
                             relief="flat", bd=0,
                             font=("Courier New", 11),
                             highlightthickness=1,
                             highlightbackground=BORDER,
                             highlightcolor=ACCENT,
                             width=22)
            entry.grid(row=i, column=1, padx=8, pady=4, ipady=4)
            setattr(self, attr, entry)

        # Média (somente leitura)
        tk.Label(form, text="Média", font=("Courier New", 10),
                 bg=PANEL, fg=MUTED).grid(
            row=len(campos)+1, column=0, sticky="w", padx=8, pady=4)

        self.lbl_media = tk.Label(
            form, text="—", font=("Courier New", 13, "bold"),
            bg=PANEL, fg=ACCENT, width=10, anchor="w")
        self.lbl_media.grid(row=len(campos)+1, column=1,
                            padx=8, pady=4, sticky="w")

        # Atualiza média ao sair dos campos de nota
        for attr in ("entry_nota1", "entry_nota2", "entry_nota3"):
            getattr(self, attr).bind("<FocusOut>", self._atualizar_media_preview)

        # ID oculto do registro selecionado
        self.id_selecionado = None

        # Busca
        sep = tk.Frame(form, bg=BORDER, height=1)
        sep.grid(row=len(campos)+2, column=0, columnspan=2,
                 sticky="ew", padx=8, pady=12)

        tk.Label(form, text="BUSCAR", font=("Courier New", 11, "bold"),
                 bg=PANEL, fg=ACCENT).grid(
            row=len(campos)+3, column=0, columnspan=2,
            sticky="w", padx=8, pady=(0, 6))

        self.entry_busca = tk.Entry(
            form, bg=ENTRY_BG, fg=TEXT,
            insertbackground=ACCENT, relief="flat", bd=0,
            font=("Courier New", 11),
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT,
            width=22)
        self.entry_busca.grid(row=len(campos)+4, column=0,
                              columnspan=2, padx=8, pady=4, ipady=4, sticky="ew")

        tk.Button(
            form, text="🔍  Buscar", command=self.buscar_aluno,
            bg=WARNING, fg=BG, activebackground="#d97706",
            font=("Courier New", 10, "bold"),
            relief="flat", cursor="hand2", bd=0, pady=6
        ).grid(row=len(campos)+5, column=0, columnspan=2,
               padx=8, pady=(6, 0), sticky="ew")

        tk.Button(
            form, text="↺  Mostrar todos", command=self.listar_alunos,
            bg=BORDER, fg=TEXT, activebackground="#475569",
            font=("Courier New", 10),
            relief="flat", cursor="hand2", bd=0, pady=5
        ).grid(row=len(campos)+6, column=0, columnspan=2,
               padx=8, pady=(4, 0), sticky="ew")

    # ── Tabela ────────────────────────────────────────────────────────────────
    def _build_table(self, parent):
        right = tk.Frame(parent, bg=BG)
        right.pack(side="left", fill="both", expand=True)

        colunas = ("id", "nome", "matricula", "disciplina",
                   "nota1", "nota2", "nota3", "media", "situacao")

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Custom.Treeview",
                        background=PANEL,
                        foreground=TEXT,
                        rowheight=28,
                        fieldbackground=PANEL,
                        borderwidth=0,
                        font=("Courier New", 10))
        style.configure("Custom.Treeview.Heading",
                        background=BORDER,
                        foreground=ACCENT,
                        font=("Courier New", 10, "bold"),
                        borderwidth=0)
        style.map("Custom.Treeview",
                  background=[("selected", ACCENT2)],
                  foreground=[("selected", BG)])

        self.tree = ttk.Treeview(right, columns=colunas,
                                 show="headings", style="Custom.Treeview")

        headers = {
            "id": ("ID", 40),
            "nome": ("Nome", 180),
            "matricula": ("Matrícula", 90),
            "disciplina": ("Disciplina", 130),
            "nota1": ("N1", 50),
            "nota2": ("N2", 50),
            "nota3": ("N3", 50),
            "media": ("Média", 60),
            "situacao": ("Situação", 80),
        }
        for col, (text, width) in headers.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor="center")

        self.tree.column("nome", anchor="w")
        self.tree.column("disciplina", anchor="w")

        sb = ttk.Scrollbar(right, orient="vertical",
                           command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)

        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="left", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        # Tags de cor para situação
        self.tree.tag_configure("aprovado",  foreground=SUCCESS)
        self.tree.tag_configure("reprovado", foreground=DANGER)
        self.tree.tag_configure("recuperacao", foreground=WARNING)

    # ── Botões de ação ────────────────────────────────────────────────────────
    def _build_actions(self, parent):
        bar = tk.Frame(self, bg=BG)
        bar.pack(fill="x", padx=20, pady=(0, 16))

        btns = [
            ("➕  Cadastrar",  self.cadastrar,  SUCCESS,   "#009915"),
            ("✏️  Atualizar",  self.atualizar,  ACCENT2,   "#1348a0"),
            ("🗑️  Excluir",    self.excluir,    DANGER,    "#cc2020"),
            ("🧹  Limpar",     self.limpar,     "#1e7a1e",  "#276b27"),
        ]
        for text, cmd, bg, hover in btns:
            b = tk.Button(bar, text=text, command=cmd,
                          bg=bg, fg=ACCENT,
                          activebackground=hover,
                          font=("Courier New", 11, "bold"),
                          relief="flat", cursor="hand2",
                          bd=0, padx=20, pady=8)
            b.pack(side="left", padx=(0, 10))

    # ── CRUD ─────────────────────────────────────────────────────────────────
    def _coletar_dados(self):
        nome       = self.entry_nome.get().strip()
        matricula  = self.entry_matricula.get().strip()
        disciplina = self.entry_disciplina.get().strip()
        try:
            n1 = float(self.entry_nota1.get().replace(",", "."))
            n2 = float(self.entry_nota2.get().replace(",", "."))
            n3 = float(self.entry_nota3.get().replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro", "As notas devem ser números válidos.")
            return None

        if not all([nome, matricula, disciplina]):
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios.")
            return None

        for n in (n1, n2, n3):
            if not (0 <= n <= 10):
                messagebox.showerror("Erro", "As notas devem estar entre 0 e 10.")
                return None

        return nome, matricula, disciplina, n1, n2, n3

    def cadastrar(self):
        dados = self._coletar_dados()
        if not dados:
            return
        db.inserir_aluno(*dados)
        messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")
        self.limpar()
        self.listar_alunos()

    def atualizar(self):
        if not self.id_selecionado:
            messagebox.showwarning("Atenção", "Selecione um aluno na tabela.")
            return
        dados = self._coletar_dados()
        if not dados:
            return
        db.atualizar_aluno(self.id_selecionado, *dados)
        messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")
        self.limpar()
        self.listar_alunos()

    def excluir(self):
        if not self.id_selecionado:
            messagebox.showwarning("Atenção", "Selecione um aluno na tabela.")
            return
        nome = self.entry_nome.get()
        if not messagebox.askyesno("Confirmar", f"Excluir o aluno '{nome}'?"):
            return
        db.excluir_aluno(self.id_selecionado)
        messagebox.showinfo("Sucesso", "Aluno removido.")
        self.limpar()
        self.listar_alunos()

    def listar_alunos(self):
        self._preencher_tabela(db.listar_alunos())

    def buscar_aluno(self):
        termo = self.entry_busca.get().strip()
        if not termo:
            self.listar_alunos()
            return
        self._preencher_tabela(db.buscar_alunos(termo))

    # ── Tabela helpers ────────────────────────────────────────────────────────
    def _preencher_tabela(self, registros):
        self.tree.delete(*self.tree.get_children())
        for r in registros:
            # r = (id, nome, matricula, disciplina, n1, n2, n3, media, situacao)
            sit = r[8].lower() if r[8] else ""
            tag = "aprovado" if "aprovado" in sit else (
                  "reprovado" if "reprovado" in sit else "recuperacao")
            self.tree.insert("", "end", values=r, tags=(tag,))

    def _on_select(self, _event=None):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], "values")
        # vals: id, nome, matricula, disciplina, n1, n2, n3, media, situacao
        self.id_selecionado = vals[0]

        for entry, val in zip(
            (self.entry_nome, self.entry_matricula, self.entry_disciplina,
             self.entry_nota1, self.entry_nota2, self.entry_nota3),
            vals[1:7]
        ):
            entry.delete(0, "end")
            entry.insert(0, val)

        self._atualizar_media_preview()

    def _atualizar_media_preview(self, _event=None):
        try:
            notas = [float(getattr(self, f"entry_nota{i}").get().replace(",", "."))
                     for i in range(1, 4)]
            media = round(sum(notas) / 3, 2)
            cor = SUCCESS if media >= 7 else (WARNING if media >= 5 else DANGER)
            self.lbl_media.config(text=f"{media:.2f}", fg=cor)
        except ValueError:
            self.lbl_media.config(text="—", fg=MUTED)

    def limpar(self):
        self.id_selecionado = None
        for attr in ("entry_nome", "entry_matricula", "entry_disciplina",
                     "entry_nota1", "entry_nota2", "entry_nota3",
                     "entry_busca"):
            getattr(self, attr).delete(0, "end")
        self.lbl_media.config(text="—", fg=MUTED)
        self.tree.selection_remove(self.tree.selection())


if __name__ == "__main__":
    App().mainloop()
