from tkinter import *
from pygame  import *
import os
import threading
from time import sleep
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
playlist = []
playlist_text = []
pos = 0
arquivos = []
total_musica = 0
parado = True
thread = True
th = threading.Thread(target=None, daemon=True)
mixer.init()#inicia a musica no pygame

def pastas():
    global pos, playlist, playlist_text, arquivos, th
    pasta = askopenfilename(title='Selecione', filetypes=[('arquivos', 'mp3')])  # escolhe o arquivo para executar
    caminho = os.path.dirname(pasta)  # ler o caminho do arquivo executado
    arquivos = os.listdir(caminho)  # ler todos os arquivos dentro do caminho

    for item in arquivos:#for item in arquivos:tira os itens dentro da lista e coloca na variavel 'item'
        filtro = item.endswith('mp3')#tem a funçao de ver as ultimas letras da sua escolha e confirma se existe.(aqui eu posso colocar mais compatibilidade de formatos)
        if filtro:
            playlist.append(caminho + '/' + item)#junta todos itens dentro da lista
            playlist_text.append(item) # adicionado uma playlist exclusiva para texto. foi necessario essa criaçao, para tirar os caminhos das pastas

    print(playlist[pos])
    nome = os.path.join(pasta)#mostra o caminho e o primeiro item executado. fiz isso apenas para usar junto com o index
    pos = playlist.index(nome)#aqui mostra a posiçao exata do primeiro arquivo executado pelo player
    print(pos)
    texto_limite(musica, playlist_text[pos], 34)
    tocar()
    if len(playlist) > 0:
        th = threading.Thread(target=auto_barra, daemon=True) ##executa uma tarefa extra, onde tem a necessidade de espera. as variaveis, target serve para marcar a variavel
        # e a daemon, serve para ativar a funçao de parar a thread quando as threads nao daemon(tarefas principais) terminarem. a variavel start, inicia a thread
        th.start()
        reiniciar_thread()

def tocar():
    global pos, playlist
    mixer.music.load(playlist[pos])#aqui executa o primeiro arquivo selecionado
    mixer.music.play()
    auto_musica()

def proximo():
    global pos, playlist, playlist_text, total_musica
    if pos < len(playlist) - 1:#fiz essa condiçao, para que o numero de execuçoes da funçao, nao seja maior do que o numero total de itens dentro da playlist
        pos += 1#o pos sempre vai começar pelo item selecionado, assim, cada vez que a funçao é executada, o pos é alterado. isso faz com que outra musica seja selencionada por meio da lista.
        total_musica = mixer.Sound(playlist[pos]).get_length()#essa funçao foi colocada aqui para mudar a variavel pos, e assim, por meio do global, o calculo da funçao auto_barra se ajusta para proxima musica tambem.
        tocar()
        texto_limite(musica, playlist_text[pos],34)
        if play['image'] == str(play_image):
            mixer.music.pause()
    else:
        print('funcionou')

def anterior():
    global pos, playlist, playlist_text, total_musica
    if pos > 0:
        pos -= 1
        total_musica = mixer.Sound(playlist[pos]).get_length()#essa funçao foi colocada aqui para mudar a variavel pos, e assim, por meio do global, o calculo da funçao auto_barra se ajusta para musica anterior tambem
        tocar()
        texto_limite(musica,playlist_text[pos], 34)
        if play['image'] == str(play_image):
            mixer.music.pause()
    else:
        print('funcionou')

def troca():
    if play['image'] == str(pause_image):#cada vez que a funçao é executada, ela se altera, fazendo que o if seja False ou True, assim mudando a foto por meio do else.
        mixer.music.pause()
        play.config(image=play_image)
    else:
        mixer.music.unpause()
        play.config(image=pause_image)

def texto_limite(label,texto,limite):#fiz essa funçao para determinar o limite de letras que vai aparecer na interface, invitando poluiçao da interface
    if len(texto) > limite:
        texto2 = texto[:limite] + '...'
        label.config(text=texto2)
    else:
        texto = texto[:]
        label.config(text=texto)

def auto_musica():#fiz essa funçao para, quando acabar a musica atual, começar outra automaticamente.
    global total_musica
    if play['image'] == str(pause_image):
        if not mixer.music.get_busy(): # Verifica se a música terminou
            init() #inicia os eventos do pygame
            proximo()  # toca a próxima música
            canvas2.coords(bola_progrecao, 15, 20, 25, 30)
    janela.after(1000,auto_musica)#verifica a cada 1 segundo se a musica acabou.

def auto_barra():
    global playlist, pos,total_musica, parado
    if len(playlist) > 0: # só vai ser executada essa funçao, quando o len de playlist for maior que 0, assim, evitando error.
        print('funcionou a barra')
        total_musica = mixer.Sound(playlist[pos]).get_length()#pega a duraçao total da musica
        linha_inicial = 20# informações da linha criada com canva. o uso disso é importante para o calculo do movimento da bolinha
        linha_final = 310
        while parado:
            pos_musica = mixer.music.get_pos() / 1000 #pega a posição atual que a musica esta sendo executada
            progresso = pos_musica / total_musica # aqui realiza uma fraçao, onde determina entre 0 e 1, a porcentagem do progresso da musica

            bolinha_x = linha_inicial + progresso * (linha_final - linha_inicial) #aqui é realizado o calculo para o movimento da bolinha de acordo com a musica
            canvas2.coords(bola_progrecao, bolinha_x - 5, 20, bolinha_x + 5, 30)#aqui, com a ajuda do loop, o canvas vai calculando a posiçao e redesenhando a bolinha de acordo com a posiçao atual da musica

            sleep(0.05)#esse sleep foi criado para evitar sobrecarregamento. Eu poderia usar uma janela.after(ms,auto_barra), mas isso provoca uma sobrecarga no codigo mesmo aumentando o ms.
            if pos_musica >= total_musica:#Quando a música termina, a variavel parado recebe False, fazendo um loop com a mesma variavel global parada que recebe True, assim o loop é interrompido ao final da musica, mas recomeça denovo
                parado = False
            if not parado: # tava tendo bug  que interrompia a barra no meio da musica, achei que eras as threads, mas finalmente descobrir que o problema era o while que recebia False no meio da musica ao executar o comando proximo. de alguma maneira o while se interrompia mas nao começava de novo
                parado = True

def reiniciar_thread(): #fiz essa funçao para evitar sobrecarga de threads em execução. consiste assim, criei a variavel global th com uma thread vazia. outra thread dentro de pastas é iniciada
    global th
    if len(playlist) > 0: #só executa quando len de playlist for maior que 0, evitando essa função de ser ativada antes de selecionar as musicas e colocar dentro de playlist
        if not th.is_alive(): #essa condiçao de escolha, verifica se ainda tem thread rodando, caso tenha, ela não é executada.
            print('A thread parou, reiniciando...')
            th = threading.Thread(target=auto_barra, daemon=True)#caso não tenha, é criado uma nova thread, assim evitando o sobrecarregamento de threads no codigo
            th.start()

def mudar_volume(Event):
    slider_pos = Event.x
    volume = max(0.0, min(1.0, slider_pos / 200)) # Calcula o volume em uma escala de 0 a 100
    mixer.music.set_volume(volume)
    print(f"Volume: {volume}%")


def volume_som():
    canvas = Canvas(janela, width=200, height=50, highlightthickness=0)
    canvas.pack()

    # Desenho da linha representando a trilha do volume
    line = canvas.create_line(10, 25, 190, 25, width=4, fill="gray")

    # Desenho do botão redondo para deslizar
    botao_circular = canvas.create_oval(90, 15, 110, 35, fill='gray')

    def mover(Event):
        x = Event.x
        if 20 <= x <= 180:  # Limita o botão à área da linha
            canvas.coords(botao_circular, x - 15, 10, x + 15, 40)
            mudar_volume(Event)

    canvas.tag_bind(botao_circular, "<B1-Motion>", mover)

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
som_image = PhotoImage(file='volume.png')

play = Button(janela,image=pause_image,command=troca,bd=0)
prox = Button(janela,image=prox_image,bd=0,command=proximo)
ant = Button(janela,image=ant_image,bd=0,command=anterior)
carregar = Button(janela,image=carregar_image,bd=0,command=pastas)
som = Button(janela,image=som_image,bd=0,command=volume_som)

play.place(x=160, y=by, width=80, height=70)
prox.place(x=260, y=by, width=largura, height=altura)
ant.place(x=90, y=by, width=largura, height=altura)
carregar.place(x=30, y=by, width=largura, height=altura)
som.place(x=173, y=0, width=largura, height=altura)
#imagens
openbanner = Image.open('gifbanner.gif')
banner = openbanner.resize((500,300))
bannertk = ImageTk.PhotoImage(banner)
canva = Canvas(janela,width=10,height=10,bg='black')
canva.place(x=60,y=60,width=280,height=280)
canva.create_image(135,135,image=bannertk)
#funcionalidades

canvas2 = Canvas(janela, width=312, height=35)
canvas2.place(x=35,y=365)
barra_progrecao = canvas2.create_line(20, 25, 312, 25, fill="gray", width=4)
bola_progrecao = canvas2.create_oval(15, 20, 25, 30, fill="gray")



'''"O problema não estava nas threads, mas sim no while da função auto_barra. Para corrigir isso, criei uma variável de controle chamada parado e a utilizei dentro do while. 
Se parado for True, o loop da auto_barra começa e só para quando a estrutura de condiçao: if pos_musica > total_musica: é executada com parado recebendo False, assim reinicia o loop com ajuda da tag global parada recebendo True novamente. 
Além disso, adicionei um outro if para evitar que a barra ficasse travada no meio da música quando a função proximo é executada, pois de alguma forma o while se tornava False e o processo parava de funcionar."'''

#preciso otimizar o codigo e deixar mais dinamico, vou separar melhor as funções e remover o uso do global e troca para self, deixando o codigo mais limpo e dinamico
#preciso adicionar o botao de volume
#melhorar a aparencia do player
#adicionar funçao de personalizar os botoes e banners
#deixar a barra clicavel


janela.mainloop()