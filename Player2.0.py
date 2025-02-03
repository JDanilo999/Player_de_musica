from tkinter import *
from pygame  import *
import os
import threading
from tkinter.ttk import Notebook, Treeview
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
pasta = ''
caminho = ''
cont2 = 0
pos_musica = 0
def pastas():
    global pos, playlist, playlist_text, arquivos, th, pasta,caminho,cont2
    try:
        pasta = askopenfilename(title='Selecione', filetypes=[('arquivos', 'mp3')])  # escolhe o arquivo para executar
        print(pasta)
        caminho = os.path.dirname(pasta)  # ler o caminho do arquivo executado
        arquivos = os.listdir(caminho)  # ler todos os arquivos dentro do caminho
    except FileNotFoundError:
        print('A pasta está vazia cara, selecione a musica agora!!!!!!')
    cont = 0
    for item in arquivos:#for item in arquivos:tira os itens dentro da lista e coloca na variavel 'item'
        filtro = item.endswith('mp3')#tem a funçao de ver as ultimas letras da sua escolha e confirma se existe.(aqui eu posso colocar mais compatibilidade de formatos)
        if filtro:
            if len(playlist) == cont: #fiz isso, para que essas variaveis sejam executadas apenas uma vez, para evitar adiçao desnecessarias de itens na playlist quando a funçao(pastas) é executada varias vezes
                playlist.append(caminho + '/' + item)#junta todos itens dentro da lista
                playlist_text.append(item) # adicionado uma playlist exclusiva para texto. foi necessario essa criaçao, para tirar os caminhos das pastas
                cont += 1
    print(f'O total de itens presente dentro da lista é {len(playlist)}') #exibir informações afim de obter um monitoramento, para no futuro, criar novas funções com base nessas informaçoes
    nome = os.path.join(pasta)#mostra o caminho e o primeiro item executado. fiz isso apenas para usar junto com o index
    try:
        pos = playlist.index(nome)#aqui mostra a posiçao exata do primeiro arquivo executado pelo player
    except ValueError:
        print('o pos(posição) está vazio, selecione a musica!!!!')

    try:
        texto_limite(musica, playlist_text[pos])
    except IndexError:
        print('não funcionou porque a playlist_text está vazia, porfavor selecione a musica >:|')
    cont2 += 1  # evita a criaçao de tree desnecessaria dentro da playlist apos uma nova execuçao da funçao pastas. Alias, eu sei que se o cara adicionar uma musica dentro da pasta quando o app estiver rodando, ela so vai aparecer se fechar o player e abrir dnv
    if cont2 < 2:
        plist()
    if play['image'] == str(play_image):#fiz isso apenas para mudar o botão para a imagem pause, caso esteja com a imagem de play quando executar essa funçao
        play.config(image=pause_image)

    if len(playlist) > 0:
        th = threading.Thread(target=auto_barra, daemon=True) ##executa uma tarefa extra, onde tem a necessidade de espera. as variaveis, target serve para marcar a variavel
        # e a daemon, serve para ativar a funçao de parar a thread quando as threads nao daemon(tarefas principais) terminarem. a variavel start, inicia a thread
        th.start()
        reiniciar_thread()
    tocar()

def tocar():
    global pos, playlist
    try:
        mixer.music.load(playlist[pos])#aqui executa o primeiro arquivo selecionado
        mixer.music.play()
    except IndexError:
        print('caso a playlist esteja vazia, essa frase vai aparecer :<> ')#exibir informações afim de obter um monitoramento, para no futuro, criar novas funções com base nessas informaçoes
        print('Selecione a musica agora!!!!!!, se não essas mensagens vão aparecer novamente ]:()')
    auto_musica()

def proximo():
    global pos, playlist, playlist_text, total_musica
    if pos < len(playlist) - 1:#fiz essa condiçao, para que o numero de execuçoes da funçao, nao seja maior do que o numero total de itens dentro da playlist
        pos += 1#o pos sempre vai começar pelo item selecionado, assim, cada vez que a funçao é executada, o pos é alterado. isso faz com que outra musica seja selencionada por meio da lista.
        total_musica = mixer.Sound(playlist[pos]).get_length()#essa funçao foi colocada aqui para mudar a variavel pos, e assim, por meio do global, o calculo da funçao auto_barra se ajusta para proxima musica tambem.
        tocar()
        texto_limite(musica, playlist_text[pos])
        if play['image'] == str(play_image):
            mixer.music.pause()
    else:
        print('Não tem mais musicas para passar')#exibir informações afim de obter um monitoramento, para no futuro, criar novas funções com base nessas informaçoes

def anterior():
    global pos, playlist, playlist_text, total_musica
    if pos > 0:
        pos -= 1
        total_musica = mixer.Sound(playlist[pos]).get_length()#essa funçao foi colocada aqui para mudar a variavel pos, e assim, por meio do global, o calculo da funçao auto_barra se ajusta para musica anterior tambem
        tocar()
        texto_limite(musica,playlist_text[pos])
        if play['image'] == str(play_image):
            mixer.music.pause()
    else:
        print('Você está no começo, porfavor, escute a musica ou pule :()')#exibir informações afim de obter um monitoramento, para no futuro, criar novas funções com base nessas informaçoes

def troca():
    if play['image'] == str(pause_image):#cada vez que a funçao é executada, ela se altera, fazendo que o if seja False ou True, assim mudando a foto por meio do else.
        mixer.music.pause()
        play.config(image=play_image)
    else:
        mixer.music.unpause()
        play.config(image=pause_image)

def texto_limite(label,texto):#fiz essa funçao para determinar o limite de letras que vai aparecer na interface, invitando poluiçao da interface
    limite = 34
    if len(texto) > limite:
        texto2 = texto[:limite] + '...'
        label.config(text=texto2)
    else:
        texto = texto[:]
        label.config(text=texto)

def auto_musica():#fiz essa funçao para, quando acabar a musica atual, começar outra automaticamente.
    global total_musica, playlist
    if len(playlist) > 0:
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

def mudar_volume(Event): #tenho que melhorar essa funçao :(
    slider_pos = Event.x
    volume = max(0.0, min(1.0, slider_pos / 200)) # Calcula o volume em uma escala de 0 a 100
    mixer.music.set_volume(volume)
    print(f"Volume: {volume}%") #exibir informações afim de obter um monitoramento, para no futuro, criar novas funções com base nessas informaçoes

def volume_som():
    canvas = Canvas(aba1, width=200, height=50, highlightthickness=0)
    canvas.pack()
    canvas.create_line(10, 25, 190, 25, width=4, fill="gray")# Desenho da linha representando a trilha do volume
    botao_circular = canvas.create_oval(90, 15, 110, 35, fill='gray') # Desenho do botão redondo para deslizar

    def mover(Event):#ultilizei a variavel Event, para capta o tipo de evento que esta sendo executado, que no caso é o evento da posiçao exata do mouse
        x = Event.x
        if 20 <= x <= 180:  # Limita o botão à área da linha
            canvas.coords(botao_circular, x - 15, 10, x + 15, 40)
            mudar_volume(Event)
    canvas.tag_bind(botao_circular, "<B1-Motion>", mover)

def item_clicado(Event):
    global caminho, pos_musica
    item = musicas.selection()# Obtém o ID do item selecionado
    if item:
        music = musicas.item(item, "values")
        music_sele = " ".join(str(item) for item in music)# Pega as musicas #transforma a tupla em uma string(claro, a tupla em si não sofre mudança, apenas criou-se uma string com base na tupla e no join
        texto = music_sele.replace(caminho,'')#fiz isso para obter apenas o nome da musica sem aparecer o caminho
        texto2 = texto[1:]#gambiarra pra tirar a / que ficou :(
        texto_limite(musica, texto2)#funçao responsavel pelo controle dos textos que aparecem
        if len(music_sele) > 0:#aqui só vai ser executar quando o item selecionado por meio da bind, tiver o numero de letras maior que zero, evitando que a execuçao seja executada de maneira errada
            if mixer.get_busy():#aqui só vai ser executado quando tiver tocando alguma musica
                mixer.music.pause()
                mixer.music.load(music_sele)
                mixer.music.play()

            else:
                mixer.music.load(music_sele)
                mixer.music.play()

            if play['image'] == str(play_image):
                play.config(image=pause_image)

def plist():
    global playlist,musicas
    quantidade = 0
    for i in playlist:
            musicas.insert("","end",values=i)
            quantidade = len(musicas.get_children())#ler a quantidade de itens dentro da tree e retorna o total. fiz isso apenas para fins de monitoramento e atribuir funçoes futuras
    print(f'A quandtidade de tree é {quantidade}')

def delete():
    item = musicas.selection()  # Obtém o ID do item selecionado
    if item:
        music = musicas.item(item, "values") #talvez o pycharm mostre um erro, isso é porque o tipo de item aceito por ele é apenas string nessa funçao.
        music_sele = " ".join(str(item) for item in music)
        musicas.delete(item)
        os.remove(music_sele)
        sleep(1)
#janela
janela = Tk()
janela.title('Player')
janela.geometry('400x500')
janela.resizable(False,False)
#abas
abas = Notebook(janela)
abas.pack(fill="both", expand=True) #os parametros dentro dessa funçao, tem a funçao de expandir e preencher toda tela da interface
aba1 = Frame(abas)
aba2 = Frame(abas)
abas.add(aba1)
abas.add(aba2)
#Textos
musica = Label(aba1,text='Songs',font='monospace')
musica.config(text='Songs')
musica.place(x=58,y=340)
#medidas
largura= 50
altura = 70
by = 410
espaco = 20
#Imagens
play_image = PhotoImage(file='play32.png')
pause_image = PhotoImage(file='pause_button32.png')
prox_image = PhotoImage(file='Next32.png')
ant_image = PhotoImage(file='ant32.png')
carregar_image = PhotoImage(file='folder32.png')
som_image = PhotoImage(file='volume.png')
lista_image = PhotoImage(file='add-to-playlist.png')
#Botões
play = Button(aba1,image=pause_image,command=troca,bd=0)
prox = Button(aba1,image=prox_image,bd=0,command=proximo)
ant = Button(aba1,image=ant_image,bd=0,command=anterior)
carregar = Button(aba1,image=carregar_image,bd=0,command=pastas)
som = Button(aba1,image=som_image,bd=0,command=volume_som)
lista = Button(aba1,image=lista_image,bd=0,command=lambda:abas.select(aba2))
#coodernadas
play.place(x=160, y=by, width=80, height=70)
prox.place(x=260, y=by, width=largura, height=altura)
ant.place(x=90, y=by, width=largura, height=altura)
carregar.place(x=30, y=by, width=largura, height=altura)
som.place(x=173, y=0, width=largura, height=altura)
lista.place(x=320, y=by, width=largura, height=altura)
#Banners
openbanner = Image.open('gifbanner.gif')
banner = openbanner.resize((500,300))
bannertk = ImageTk.PhotoImage(banner)
canva_banner = Canvas(aba1,width=10,height=10,bg='black')
canva_banner.place(x=60,y=60,width=280,height=280)
canva_banner.create_image(135,135,image=bannertk)
#funcionalidades
canvas2 = Canvas(aba1, width=312, height=35)
canvas2.place(x=35,y=365)
barra_progrecao = canvas2.create_line(20, 25, 312, 25, fill="gray", width=4)
bola_progrecao = canvas2.create_oval(15, 20, 25, 30, fill="gray")
#segunda aba
#tree
musicas = Treeview(aba2,columns=('nomes'),show='headings') #cria uma tree para armazenar as musicas
musicas.heading('nomes',text='Playlist')#aqui coloquei o id e o nome do tree
musicas.pack(padx=10,pady=70,fill="both",expand=True)
musicas.bind("<Button-1>",item_clicado)#quando houver um clique no tree, a funçao é executada(obs: o <Button-1> é o botão esquerdo do mouse)
#imagem
voltar_imagem = PhotoImage(file='backward.png')
delete_image = PhotoImage(file='delete.png')
#Botão
voltar = Button(aba2,image=voltar_imagem,bd=0,command=lambda:abas.select(aba1))
voltar.place(x=173, y=0, width=largura, height=altura)

deletar = Button(aba2,image=delete_image,command=delete,bd=0)
deletar.place(x=160, y=by, width=80, height=70)

'''"O problema não estava nas threads, mas sim no while da função auto_barra. Para corrigir isso, criei uma variável de controle chamada parado e a utilizei dentro do while. 
Se parado for True, o loop da auto_barra começa e só para quando a estrutura de condiçao: if pos_musica > total_musica: é executada com parado recebendo False, assim reinicia o loop com ajuda da tag global parada recebendo True novamente. 
Além disso, adicionei um outro if para evitar que a barra ficasse travada no meio da música quando a função proximo é executada, pois de alguma forma o while se tornava False e o processo parava de funcionar."'''

#preciso otimizar o codigo e deixar mais dinamico, vou separar melhor as funções e remover o uso do global e troca para self, deixando o codigo mais limpo e dinamico
#preciso adicionar o botao de volume
#melhorar a aparencia do player
#adicionar funçao de personalizar os botoes e banners
#desculpe os erros de ortografia, queimei meu cerebro fazendo os codigos :/
janela.mainloop()