import tkinter as tk
import random
import time

class RachaCuca:
    # chamando o __init__ metodo especial de classe no python
    def __init__(self, root):
        # self é a instância da classe
        # root se refere a janela principal em aplicaçao com Tkinter
        self.root = root
        self.root.title("Racha Cuca - Quebra-Cabeça 15")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        self.tamanho = 4  # Tabuleiro 4x4
        self.tabuleiro = self.gerar_tabuleiro()
        self.tempo_inicial = time.time()
        
        # canvas é o widget do Tkinter, serve para fazer desenhos
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="black")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.clicar_bloco)

        self.cronometro_label = tk.Label(self.root, text="Tempo: 00:00", font=("Arial", 14))
        self.cronometro_label.pack()

        self.botao_reset = tk.Button(self.root, text="Reiniciar", command=self.reiniciar)
        self.botao_reset.pack()

        self.desenhar_tabuleiro()
        self.atualizar_cronometro()

    def gerar_tabuleiro(self):
        numeros = list(range(1, 16)) + [None]
        random.shuffle(numeros)
        return [numeros[i:i + 4] for i in range(0, 16, 4)]

    def desenhar_tabuleiro(self):
        self.canvas.delete("all")
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                numero = self.tabuleiro[i][j]
                if numero:
                    x0, y0 = j * 100, i * 100
                    x1, y1 = x0 + 100, y0 + 100
                    # self instancia o canvas para criar um retangulo e a fonte da letra do texto
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="blue", outline="black")
                    self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=str(numero), font=("Arial", 24), fill="white")

    def encontrar_vazio(self):
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                if self.tabuleiro[i][j] is None:
                    return i, j
        return None

    def mover_bloco(self, i, j):
        vazio_i, vazio_j = self.encontrar_vazio()
        if (abs(vazio_i - i) == 1 and vazio_j == j) or (abs(vazio_j - j) == 1 and vazio_i == i):
            self.tabuleiro[vazio_i][vazio_j], self.tabuleiro[i][j] = self.tabuleiro[i][j], self.tabuleiro[vazio_i][vazio_j]
            self.desenhar_tabuleiro()
            if self.verificar_vitoria():
                self.mostrar_vitoria()

    def clicar_bloco(self, event):
        j, i = event.x // 100, event.y // 100
        self.mover_bloco(i, j)

    def verificar_vitoria(self):
        esperado = [list(range(1 + i * 4, 5 + i * 4)) for i in range(4)]
        esperado[-1][-1] = None
        return self.tabuleiro == esperado

    def mostrar_vitoria(self):
        tempo_total = int(time.time() - self.tempo_inicial)
        minutos, segundos = divmod(tempo_total, 60)
        self.canvas.create_text(200, 200, text=f"🎉 Você venceu!\nTempo: {minutos:02}:{segundos:02}", font=("Arial", 20), fill="blue")

    def atualizar_cronometro(self):
        tempo_passado = int(time.time() - self.tempo_inicial)
        minutos, segundos = divmod(tempo_passado, 60)
        self.cronometro_label.config(text=f"Tempo: {minutos:02}:{segundos:02}")
        self.root.after(1000, self.atualizar_cronometro)

    def reiniciar(self):
        self.tabuleiro = self.gerar_tabuleiro()
        self.tempo_inicial = time.time()
        self.desenhar_tabuleiro()

if __name__ == "__main__":
    root = tk.Tk()
    jogo = RachaCuca(root)
    root.mainloop()

""""""