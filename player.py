from tkinter import *
from tkinter.filedialog import askopenfilename
import pygame
from pygame  import *
import os
from PIL import Image, ImageTk
playlist = []
pos = 0
def pastas():
    global pos, playlist
    pasta = askopenfilename(title='Selecione', filetypes=[('arquivos', 'mp3')])
    caminho = os.path.dirname(pasta)
    arquivos = os.listdir(caminho)
    for item in arquivos:
        filtro = item.endswith('mp3')
        if filtro:
            playlist.append(caminho + '/' + item)
    print(playlist)
    nome = os.path.join(pasta)
    pos = playlist.index(nome)
    print(pos)
    texto_limite(musica, playlist[pos], 44)
    tocar()

def tocar():
    global pos, playlist
    mixer.init()
    mixer.music.load(playlist[pos])
    mixer.music.play()
    auto_musica()

def proximo():
    global pos, playlist
    if pos < len(playlist) - 1:
        pos += 1
        tocar()
        texto_limite(musica, playlist[pos],44)
        if play['image'] == str(play_image):
            mixer.music.pause()
    else:
        print('funcionou')

def anterior():
    global pos, playlist
    if pos > 0:
        pos -= 1
        tocar()
        texto_limite(musica,playlist[pos],44)
        if play['image'] == str(play_image):
            mixer.music.pause()
    else:
        print('funcionou')

def troca():
    if play['image'] == str(pause_image):
        mixer.music.pause()
        play.config(image=play_image)
    else:
        mixer.music.unpause()
        play.config(image=pause_image)

def texto_limite(label,texto,limite):
    if len(texto) > limite:
        texto2 = texto[22:limite] + '...'
        label.config(text=texto2)
    else:
        texto = texto[22:]
        label.config(text=texto)

def auto_musica():
    if play['image'] == str(pause_image):
        if not pygame.mixer.music.get_busy():
            pygame.init()
            proximo()
    janela.after(5000,auto_musica)
#janela
janela = Tk()
janela.title('Player')
janela.geometry('400x500')
janela.resizable(False,False)
#Textos
musica = Label(janela,text='Songs',font='monospace')
musica.config(text='Songs')
musica.place(x=58,y=340)
#Botões
largura= 50
altura = 70
by = 410
espaco = 20

play_image = PhotoImage(file='play.png')
pause_image = PhotoImage(file='pause.png')
prox_image = PhotoImage(file='Next32.png')
ant_image = PhotoImage(file='ant32.png')
carregar_image = PhotoImage(file='folder32.png')

play = Button(janela,image=pause_image,command=troca,bd=0)
prox = Button(janela,image=prox_image,bd=0,command=proximo)
ant = Button(janela,image=ant_image,bd=0,command=anterior)
carregar = Button(janela,image=carregar_image,bd=0,command=pastas)

play.place(x=160, y=by, width=80, height=70)
prox.place(x=260, y=by, width=largura, height=altura)
ant.place(x=90, y=by, width=largura, height=altura)
carregar.place(x=173, y=0, width=largura, height=altura)
#imagens
openbanner = Image.open('gifbanner.gif')
banner = openbanner.resize((500,300))
bannertk = ImageTk.PhotoImage(banner)
canva = Canvas(janela,width=10,height=10,bg='black')
canva.place(x=60,y=60,width=280,height=280)
canva.create_image(135,135,image=bannertk,)

janela.mainloop()
#JDG