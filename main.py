# all of our imports are listed here
import math
import random
import pygame
from pygame.locals import *
import sys


class Card:

    # esta classe contém todos os atributos de uma carta de baralho
    def __init__(self, suit, color, label, value):
        self.suit = suit
        self.color = color
        self.label = label
        self.value = value


class Deck:

    # esta classe contém uma matriz que atua como nosso baralho de 52 cartas
    def __init__(self):
        self.cards = []

    # este método simplesmente cria um baralho usando a classe Card acima
    def createDeck(self):
        suits = ["Clover", "Spade", "Heart", "Diamond"]
        for symbol in suits:
            number = 2
            while number < 15:
                if symbol == "Clover" or symbol == "Spade":
                    suitColor = "Black"
                else:
                    suitColor = "Red"
                value = number
                if number > 10:
                    value = 10
                if number == 14:
                    value = 1
                letter = number
                if number == 11:
                    letter = "J"
                elif number == 12:
                    letter = "Q"
                elif number == 13:
                    letter = "K"
                elif number == 14:
                    letter = "A"
                newCard = Card(symbol, suitColor, letter, value)
                self.cards.append(newCard)
                number += 1

    
    # este método nos permite embaralhar nosso baralho de forma que ele fique organizado aleatoriamente
    def shuffleDeck(self):
        return random.shuffle(self.cards)

    # este método basicamente pega a carta do topo do baralho e a retorna
    def getCard(self):
        topCard = self.cards[0]
        self.cards.pop(0)
        return topCard


class Dealer:

    # esta classe contém tudo o que está sob o controle do revendedor
    def __init__(self):
        self.deck = Deck()
        self.deck.createDeck()
        self.deck.shuffleDeck()
        self.hand = []
        self.count = 0
        self.x = halfWidth
        self.y = 100

    
    # este método cria a mão de duas cartas com a qual o crupiê começa
    def createDealerHand(self):
        for i in range(1, 3):
            self.addCard()

    
    # este método usa getCard() para distribuir uma carta a um jogador
    def dealCard(self):
        return self.deck.getCard()

    
    # este método permite que o crupiê distribua uma carta para si mesmo e também contabilize a contagem do crupiê
    def addCard(self):
        dealerCard = self.dealCard()
        self.hand.append(dealerCard)
        self.count += dealerCard.value
        self.countAce()

    # este método imprime a mão do crupiê
    def printDealerHand(self):
        print("")
        print("Mão do Crupiê:")
        for dealerCard in self.hand:
            print("Suit: " + dealerCard.suit + "\nLabel: " + str(dealerCard.label))

    # este método imprime a contagem do crupiê
    def printDealerCount(self):
        print("")
        print("Contagem do Crupiê: " + str(self.count))

    # este método considera todos os ases na mão do crupiê para dar a eles a contagem mais próxima de 21
    def countAce(self):
        if self.count <= 21:
            for card in self.hand:
                if card.label == "A":
                    self.count += 10
                    if self.count > 21:
                        self.count -= 10
                        break

    # este método irá comprar todas as cartas de uma mão (proporção de dimensão de carta 13:20)
    def drawHand(self, surface):
        cardWidth, cardHeight = 78, 120
        cardGap = 20
        playerBoxLength, playerBoxHeight = cardWidth + (cardGap * (len(self.hand) - 1)), cardHeight
        playerTopLeftX = self.x - (0.5 * playerBoxLength)
        playerTopLeftY = self.y - (0.5 * playerBoxHeight)
        for card in self.hand:
            if card == self.hand[1]:
                drawCard = pygame.image.load("Resources/Cards/Back/red_back.png")
            else:
                drawCard = pygame.image.load("Resources/Cards/" + str(card.suit) + "/" + str(card.label) + ".png")
            resizedCard = pygame.transform.scale(drawCard, (cardWidth, cardHeight))
            surface.blit(resizedCard, (playerTopLeftX, playerTopLeftY))
            pygame.display.update()
            playerTopLeftX += cardGap
        nameX = self.x
        nameY = self.y + (0.75 * cardHeight)
        add_text("CRUPIÊ", text_Normal, surface, nameX, nameY, white)
        deckX = 400 - (0.5 * cardWidth)
        deckY = 100 - (0.5 * cardHeight)
        for card in range(1, 7):
            deckCard = pygame.image.load("Resources/Cards/Back/red_back.png")
            backCard = pygame.transform.scale(deckCard, (cardWidth, cardHeight))
            surface.blit(backCard, (deckX, deckY))
            deckX += cardGap


class Player:

    # esta classe contém tudo o que está sob o controle do jogador
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.count = 0
        self.blackjack = False
        self.bust = False
        self.bank = 100
        self.bet = 0
        self.roundsWon = 0
        self.x = 0
        self.y = 0
        self.currentTurn = False

    # este método pergunta ao jogador qual a sua escolha de ação quando for a sua vez
    def askChoice(self):
        inp = 0
        answered = False
        while answered is False:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and event.key == K_h:
                    inp = 1
                    answered = True
                if event.type == KEYDOWN and event.key == K_p:
                    inp = 2
                    answered = True
        return inp

    # este método adiciona uma carta fornecida pelo dealer à mão do jogador
    def addCard(self, card):
        self.hand.append(card)
        self.countCards()
        print(str(self.name) + "'s Count: " + str(self.count))

    # este método imprime a mão do jogador
    def printHand(self):
        print("")
        print(str(self.name) + "'s Hand: ")
        for playerCard in self.hand:
            print("Suit - " + playerCard.suit + "\nLabel - " + str(playerCard.label))

    # este método imprime a contagem do jogador
    def printCount(self):
        print("")
        print(str(self.name) + "'s Count: " + str(self.count))


    # este método aplicará o resultado da aposta ao banco
    # nenhum parâmetro negativo precisará ser passado, pois já subtraímos a aposta do banco
    def applyBet(self, factor):
        self.bank += self.bet * factor

    # este método que irá zerar as apostas
    def resetBet(self):
        self.bet = 0

    # este método imprime o banco do jogador
    def printBank(self):
        print("")
        print(str(self.name) + "'s Bank: " + str(self.bank))

    # este método reinicia a mão do jogador
    def resetHandAndCount(self):
        self.hand = []
        self.count = 0

    # este método considera todos os ases na mão de um jogador para dar a ele a contagem mais próxima abaixo de 21
    def countCards(self):
        self.count = 0
        for card in self.hand:
            self.count += card.value
        for card in self.hand:
            if card.label == "A":
                self.count += 10
                if self.count > 21:
                    self.count -= 10
                    break

    
    # este método irá comprar todas as cartas de uma mão (proporção de dimensão de carta 13:20)
    def drawHand(self, surface):
        cardWidth, cardHeight = 78, 120
        cardGap = 20
        playerBoxLength, playerBoxHeight = cardWidth + (cardGap * (len(self.hand) - 1)), cardHeight
        playerTopLeftX = self.x - (0.5 * playerBoxLength)
        playerTopLeftY = self.y - (0.5 * playerBoxHeight)
        for card in self.hand:
            drawCard = pygame.image.load("Resources/Cards/" + str(card.suit) + "/" + str(card.label) + ".png")
            resizedCard = pygame.transform.scale(drawCard, (cardWidth, cardHeight))
            surface.blit(resizedCard, (playerTopLeftX, playerTopLeftY))
            pygame.display.update()
            playerTopLeftX += cardGap
        nameX = self.x
        nameY = self.y + (0.75 * cardHeight)
        nameColor = white
        if self.currentTurn:
            nameColor = blue
            add_text("Hit(H) or Pass(P)", text_Normal, surface, self.x, self.y - (0.75 * cardHeight), nameColor)
        if self.bust:
            bust = pygame.image.load("Resources/Icons/bust.png")
            bustWidth = bust.get_width()
            bustHeight = bust.get_height()
            surface.blit(bust, (self.x - (0.5 * bustWidth), self.y - (0.5 * bustHeight)))
        if self.blackjack:
            blackjack = pygame.image.load("Resources/Icons/blackjack.png")
            bjWidth = blackjack.get_width()
            bjHeight = blackjack.get_height()
            surface.blit(blackjack, (self.x - (0.5 * bjWidth), self.y - (0.5 * bjHeight)))
        add_text(str(self.name) + "   $" + str(self.bank), text_Normal, surface, nameX, nameY, nameColor)

    # função para redefinir tudo para a próxima rodada
    def resetState(self):
        self.bust = False
        self.blackjack = False
        self.resetBet()
        self.resetHandAndCount()


# oficialmente o fim de todas as nossas inicializações de classe e métodos

# abaixo consiste o código relacionado ao py-game/graphics

pygame.init()
pygame.font.init()
screenWidth, screenHeight = 1250, 750
halfWidth, halfHeight = screenWidth / 2, screenHeight / 2
pokerBackgroundOriginal = pygame.image.load("Resources/Icons/pokerBackground3.jpg")
pokerGreen = pygame.transform.scale(pokerBackgroundOriginal, (screenWidth, screenHeight))
black, blue, white, orange, red = (0, 0, 0), (51, 235, 255), (255, 255, 255), (255, 165, 0), (255, 0, 0)
fontType = 'Comic Sans MS'
text_Title = pygame.font.SysFont(fontType, 80)
text_Heading = pygame.font.SysFont(fontType, 60)
text_SubHeading = pygame.font.SysFont(fontType, 45)
text_Bold = pygame.font.SysFont(fontType, 30)
text_Normal = pygame.font.SysFont(fontType, 20)
text_Small = pygame.font.SysFont(fontType, 10)

# variáveis ​​globais listadas abaixo
players = []
numPlayers = 0
dealer = Dealer()
startY = 50


# função para adicionar texto ao jogo quando necessário
def add_text(text, font, surface, x, y, text_color):
    textObject = font.render(text, False, text_color)
    textWidth = textObject.get_rect().width
    textHeight = textObject.get_rect().height
    surface.blit(textObject, (x - (textWidth / 2), y - (textHeight / 2)))

# função para criar a tela inicial do jogo
def startGame():
    pygame.init()
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Welcome")
    screen.blit(pokerGreen, (0, 0))
    titleLogo = pygame.image.load("Resources/Icons/titleBlitzEdition.png")
    logoX = titleLogo.get_width()
    logoY = titleLogo.get_height()
    screen.blit(titleLogo, (halfWidth - (0.5 * logoX), halfHeight - (0.5 * logoY) - 25))
    add_text("PRESSIONE ESPAÇO PARA CONTINUAR", text_SubHeading, screen, halfWidth, halfHeight + 100, white)
    pygame.display.update()
    beginning = True
    while beginning:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                beginning = False

# função para mostrar ao leitor todas as instruções e regras do nosso jogo
def showInstructions():
    pygame.init()
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("How to Play")
    screen.blit(pokerGreen, (0, 0))
    add_text("Objetivo do Jogo:", text_SubHeading, screen, halfWidth, 50, orange)
    add_text("--> Ficar o mais próximo possível de 21 sem ultrapassar, para você ganhar dinheiro.", text_Normal, screen, halfWidth, 100, white)
    add_text("Regras Básicas:", text_SubHeading, screen, halfWidth, 150, orange)
    add_text("--> Cartas 2 - 10 = valor nominal        Valete, Dama, Rei = 10        Ás = 1 ou 11", text_Normal, screen, halfWidth, 200, white)
    add_text("--> Pressione H para Pedir (Pega uma carta)        Pressione P para Passar (Finaliza a vez)", text_Normal, screen, halfWidth, 250, white)
    add_text("--> Você pode pedir quantas cartas quiser, porém, ao ultrapassar 21, você estoura e sua vez termina.", text_Normal, screen, halfWidth, 300, white)
    add_text("--> Se você atingir 21 com suas duas primeiras cartas, você faz um Blackjack, e fica de fora dessa rodada.", text_Normal, screen, halfWidth, 350, white)
    add_text("Apostas:", text_SubHeading, screen, halfWidth, 400, orange)
    add_text("--> Todos começam com $100 para jogar.", text_Normal, screen, halfWidth, 450, white)
    add_text("--> Cuidado, pois você pode falir, porém o jogo sempre fornecerá pelo menos um dólar para você jogar.", text_Normal, screen, halfWidth, 500, white)
    add_text("--> Estourar = O crupiê pega sua aposta        Blackjack = Ganhe 1 e meio da sua aposta", text_Normal, screen, halfWidth, 550, white)
    add_text("--> Mais próximo de 21 = Ganhe 2 vezes sua aposta, caso contrário, o crupiê pega sua aposta", text_Normal, screen, halfWidth, 600, white)
    add_text("--> Se a sua contagem for igual à do crupiê e for a maior contagem abaixo de 21, você recebe sua aposta de volta", text_Normal, screen, halfWidth, 650, white)
    add_text("--> crupiê estourar = Todos os jogadores restantes ganham 2 vezes suas apostas.", text_Normal, screen, halfWidth, 700, white)

    pygame.display.update()
    instructions = True
    while instructions:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                instructions = False

# função para receber o número de jogadores
def getNumberOfPlayers():
    global numPlayers
    pygame.init()
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Entrar Jogadores")
    validNumbers = "23456"
    userString = ""
    answered = False
    while answered is False:
        screen.blit(pokerGreen, (0, 0))
        add_text("Insira o número de jogadores abaixo (o jogo foi projetado para 2 a 6 jogadores):", text_Bold, screen, halfWidth, halfHeight - 50, orange)
        add_text(userString, text_SubHeading, screen, halfWidth, halfHeight, white)
        add_text("PRESSIONE ESPAÇO PARA CONTINUAR", text_Bold, screen, halfWidth, halfHeight + 50, orange)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (pygame.key.name(event.key) in validNumbers) and len(userString) < 1:
                userString += str(pygame.key.name(event.key))
            if event.type == KEYDOWN and event.key == K_BACKSPACE:
                userString = ""
            if event.type == KEYDOWN and event.key == K_SPACE and len(userString) == 1:
                numPlayers = int(userString)
                answered = True

# função para receber os nomes de todos os jogadores
def getPlayerNames():
    global players, numPlayers
    pygame.init()
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Insira os nomes")
    validCharacters = "abcdefghijklmnopqrstuvwxyz1234567890"
    allNames = False
    while allNames is False:
        for player in range(1, numPlayers + 1):
            userString = ""
            singleName = False
            while singleName is False:
                screen.blit(pokerGreen, (0, 0))
                add_text("Digite o nome do jogador " + str(player) + ":", text_Bold, screen, halfWidth, halfHeight - 50, orange)
                add_text(userString, text_SubHeading, screen, halfWidth, halfHeight, white)
                if player < numPlayers:
                    add_text("PRESSIONE ESPAÇO PARA ADICIONAR NOME", text_Bold, screen, halfWidth, halfHeight + 50, orange)
                elif player == numPlayers:
                    add_text("PRESSIONE ESPAÇO PARA CONTINUAR", text_Bold, screen, halfWidth, halfHeight + 50, orange)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN and (pygame.key.name(event.key) in validCharacters) and len(userString) < 9:
                        userString += str(pygame.key.name(event.key))
                    if event.type == KEYDOWN and event.key == K_BACKSPACE:
                        userString = ""
                    if event.type == KEYDOWN and event.key == K_SPACE:
                        players.append(Player(userString))
                        singleName = True
                        if player == numPlayers:
                            allNames = True

# função que define as coordenadas x e y de cada jogador mais o crupiê
def fixCoordinates():
    global players, dealer, numPlayers
    if numPlayers == 1:
        players[0].x = halfWidth
        players[0].y = 650
    elif numPlayers == 2:
        players[0].x = 850
        players[0].y = halfHeight + 150
        players[1].x = 400
        players[1].y = halfHeight + 150
    elif numPlayers == 3:
        players[0].x = 1000
        players[0].y = halfHeight
        players[1].x = halfWidth
        players[1].y = 625
        players[2].x = 250
        players[2].y = halfHeight
    elif numPlayers == 4:
        players[0].x = 1050
        players[0].y = halfHeight
        players[1].x = halfWidth + 200
        players[1].y = 625
        players[2].x = halfWidth - 200
        players[2].y = 625
        players[3].x = 200
        players[3].y = halfHeight
    elif numPlayers == 5:
        players[0].x = 1100
        players[0].y = halfHeight - 50
        players[1].x = halfWidth + 300
        players[1].y = 525
        players[2].x = halfWidth
        players[2].y = 625
        players[3].x = halfWidth - 300
        players[3].y = 525
        players[4].x = 150
        players[4].y = halfHeight - 50
    elif numPlayers == 6:
        players[0].x = 1100
        players[0].y = halfHeight - 170
        players[1].x = halfWidth + 350
        players[1].y = 415
        players[2].x = halfWidth + 175
        players[2].y = 625
        players[3].x = halfWidth - 175
        players[3].y = 625
        players[4].x = halfWidth - 350
        players[4].y = 415
        players[5].x = 150
        players[5].y = halfHeight - 170

# função para coletar as apostas de todos os jogadores a cada rodada
def getPlayerBets():
    # for player in players:
    #     player.createBet()
    # for player in players:
    #     player.bet = 5
    #     player.applyBet(-1)
    global players, numPlayers
    pygame.init()
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Enter Bets")
    validNumbers = "1234567890"
    allBets = False
    while allBets is False:
        for player in players:
            if player.bank == 0:
                player.bank += 1
            validBet = True
            userString = ""
            singleBet = False
            while singleBet is False:
                screen.blit(pokerGreen, (0, 0))
                add_text("Insira o valor de aposta do jogador " + str(player.name).upper().upper() + " (" + str(player.name).upper().upper() + " tem o saldo de = $" + str(player.bank) + "):", text_Bold, screen, halfWidth, halfHeight - 50,
                         orange)
                add_text(userString, text_SubHeading, screen, halfWidth, halfHeight, white)
                if player is not players[len(players) - 1]:
                    add_text("PRESSIONE ESPAÇO PARA CONTINUAR", text_Bold, screen, halfWidth, halfHeight + 50, orange)
                else:
                    add_text("PRESSIONE ESPAÇO PARA CONTINUAR", text_Bold, screen, halfWidth, halfHeight + 50, orange)
                if validBet is False:
                    add_text("ENTRE COM UMA APOSTA VÁLIDA", text_Bold, screen, halfWidth, halfHeight + 100, red)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN and (pygame.key.name(event.key) in validNumbers) and len(
                            userString) < 4:
                        userString += str(pygame.key.name(event.key))
                    if event.type == KEYDOWN and event.key == K_BACKSPACE:
                        userString = ""
                    if event.type == KEYDOWN and event.key == K_SPACE:
                        if userString == "":
                            userString = "0"
                        if 0 <= int(userString) <= player.bank:
                            singleBet = True
                            player.bet = int(userString)
                            player.applyBet(-1)
                        if int(userString) > player.bank:
                            validBet = False
                        if singleBet is True and player == players[len(players) - 1]:
                            allBets = True

# função para restaurar todas as cartas do baralho para uma nova rodada
def newDeck():
    global dealer
    dealer = Dealer()

# função para criar as mãos do crupiê e de todos os jogadores
def createHands():
    global dealer
    dealer.createDealerHand()
    for i in range(1, 3):
        for player in players:
            card = dealer.dealCard()
            player.addCard(card)

# função para verificar blackjacks (basicamente quando as duas primeiras cartas iniciais distribuídas a um jogador somam 21)
# se houver um, você ganha automaticamente uma vez e meia sua aposta e fica de fora da rodada
def checkBlackJack():
    for player in players:
        if player.count == 21:
            print("")
            print(player.name + ", você fez um BLACKJACK e ganhou uma vez e meia a sua aposta.")
            player.applyBet(3/2)
            player.resetBet()
            player.blackjack = True

# função para executar os turnos de todos os jogadores, basicamente permitindo bater e passar normalmente
# esta função também contém o código para alterar o valor de um ás quando necessário
def playTurns():
    pygame.init()
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Rodada de Jogo")
    turn = 0
    while turn < len(players):
        currentPlayer = players[turn]
        if currentPlayer.blackjack:
            turn += 1
            if turn >= len(players):
                break
            currentPlayer = players[turn]
        for player in players:
            player.currentTurn = False
            if player == currentPlayer:
                player.currentTurn = True
        currentPlayer.printHand()
        drawTurn(screen)
        choice = currentPlayer.askChoice()
        if choice == 1:
            keepHitting = True
            while keepHitting is True:
                hitCard = dealer.dealCard()
                currentPlayer.addCard(hitCard)
                drawTurn(screen)
                currentPlayer.printHand()
                if currentPlayer.count > 21:
                    print("")
                    print(str(currentPlayer.name) + ", você estourou. O Crupiê fica com sua aposta.")
                    currentPlayer.bust = True
                    currentPlayer.resetBet()
                    break
                choice = currentPlayer.askChoice()
                if choice != 1:
                    keepHitting = False
        turn += 1

# função para desenhar a tela toda vez que uma ação é realizada no jogo
def drawTurn(surface):
    global players, dealer
    surface.blit(pokerGreen, (0, 0))
    dealer.drawHand(surface)
    for player in players:
        player.drawHand(surface)
    tigerEye = pygame.image.load("Resources/Icons/tigerEye.png")
    tigerX = round(tigerEye.get_width() * 0.5)
    tigerY = round(tigerEye.get_height() * 0.5)
    tigerEye = pygame.transform.scale(tigerEye, (tigerX, tigerY))
    tigerEye.set_alpha(10)
    surface.blit(tigerEye, (halfWidth - (0.5 * tigerX), halfHeight - (0.5 * tigerY)))
    pygame.display.update()

# função para revelar a carta virada para baixo do crupiê, e se o crupiê tiver que forçar o hit, ele o fará
def revealDealerHand(surface):
    global dealer, startY
    dealerBust = False
    while dealer.count <= 16:
        dealer.addCard()
    if dealer.count > 21:
        print("")
        print("O Crupiê estourou. Vocês todos ganharam o dobro de suas apostas.")
        startY += 50
        add_text("O Crupiê estourou. Vocês todos ganharam o dobro de suas apostas.", text_Normal, surface, halfWidth, startY, white)
        for player in players:
            if player.bet > 0:
                player.applyBet(2)
        dealerBust = True
    dealer.printDealerHand()
    dealer.printDealerCount()
    return dealerBust

# função para ver como as apostas são recuperadas com base nas contagens
def compareCounts(surface):
    global players, dealer, startY
    noCounts = True
    highestCount = 0
    for player in players:
        if 21 >= player.count > highestCount:
            highestCount = player.count
            noCounts = False
    if noCounts is False:
        for player in players:
            if player.count == highestCount and highestCount > dealer.count and player.blackjack is False:
                print("")
                print(str(player.name).upper() + ", você ganhou o dobro da sua aposta")
                startY += 50
                add_text(str(player.name).upper() + ", você ganhou o dobro da sua aposta.", text_Normal, surface, halfWidth, startY, white)
                player.applyBet(2)
                player.resetBet()
            elif player.count == dealer.count and player.blackjack is False:
                print("")
                print(str(player.name).upper() + ", você recebeu sua aposta de volta.")
                startY += 50
                add_text(str(player.name).upper() + ", você recebeu sua aposta de volta.", text_Normal, surface, halfWidth, startY, white)
                player.applyBet(1)
                player.resetBet()
            elif player.count < dealer.count and player.blackjack is False:
                print("")
                print(str(player.name).upper() + ", o crupiê aceitou sua aposta.")
                startY += 50
                add_text(str(player.name).upper() + ", o crupiê aceitou sua aposta.", text_Normal, surface, halfWidth, startY, white)
                player.resetBet()
            elif player.bust:
                startY += 50
                add_text(str(player.name).upper() + " pego.", text_Normal, surface, halfWidth, startY, white)
            elif player.blackjack:
                startY += 50
                add_text(str(player.name).upper() + " consegui um blackjack.", text_Normal, surface, halfWidth, startY, white)
    else:
        startY += 50
        add_text("Vocês todos foram pegos.", text_Normal, surface, halfWidth, startY, white)

# função para verificar um vencedor, basicamente quando uma pessoa atinge uma certa quantia de dinheiro
def checkWinner(surface):
    global roundOver, gameOver, startY
    highestBank = 0
    winnerPresent = False
    for player in players:
        if player.bank > highestBank and player.bank >= 200:
            highestBank = player.bank
            winnerPresent = True
    if winnerPresent:
        for player in players:
            if player.bank == highestBank:
                print("")
                print(str(player.name).upper() + ", VOCÊ GANHOU O JOGO.")
                startY += 50
                add_text(str(player.name).upper() + ", VOCÊ GANHOU O JOGO.", text_Normal, surface, halfWidth, startY, blue)
            roundOver = True
        gameOver = True

# função para exibir uma mensagem sobre os resultados da rodada anterior
def showEndRoundScreen():
    global startY, gameOver, numPlayers, players
    pygame.init()
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Round Over")
    screen.blit(pokerGreen, (0, 0))
    add_text("Resultados:", text_SubHeading, screen, halfWidth, startY, orange)
    if revealDealerHand(screen) is False:
        compareCounts(screen)
    checkWinner(screen)
    startY += 50
    add_text("Contagem do Crupiê: " + str(dealer.count), text_Normal, screen, halfWidth, startY, orange)
    startY += 50
    countString1 = ""
    for i in range(0, 3):
        player = players[i]
        if (numPlayers > 3 and player == players[2]) or player == players[numPlayers - 1]:
            countString1 += str(player.name).upper() + " Contagem de: " + str(player.count)
        else:
            countString1 += str(player.name).upper() + " Contagem de: " + str(player.count) + "        "
        if i == 1 and numPlayers == 2:
            break
    add_text(countString1, text_Normal, screen, halfWidth, startY, orange)
    if numPlayers > 3:
        startY += 50
        countString2 = ""
        for i in range(3, numPlayers):
            player = players[i]
            if player == players[numPlayers - 1]:
                countString2 += str(player.name).upper() + " Contagem de: " + str(player.count)
            else:
                countString2 += str(player.name).upper() + " Contagem de: " + str(player.count) + "        "
        add_text(countString2, text_Normal, screen, halfWidth, startY, orange)
    bankString1 = ""
    for i in range(0, 3):
        player = players[i]
        if (numPlayers > 3 and player == players[2]) or player == players[numPlayers - 1]:
            bankString1 += str(player.name).upper() + " Saldo no Banco de: $" + str(player.bank)
        else:
            bankString1 += str(player.name).upper() + " Saldo no Banco de: $" + str(player.bank) + "        "
        if i == 1 and numPlayers == 2:
            break
    add_text(bankString1, text_Normal, screen, halfWidth, 600, white)
    if numPlayers > 3:
        bankString2 = ""
        for i in range(3, numPlayers):
            player = players[i]
            if player == players[numPlayers - 1]:
                bankString2 += str(player.name).upper() + " Saldo no Banco de: $" + str(player.bank)
            else:
                bankString2 += str(player.name).upper() + " Saldo no Banco de: $" + str(player.bank) + "        "
        add_text(bankString2, text_Normal, screen, halfWidth, 650, white)
    if gameOver is True:
        add_text("PRESSIONE ESPAÇO PARA SAIR", text_SubHeading, screen, halfWidth, 700, orange)
    else:
        add_text("PRESSIONE ESPAÇO PARA CONTINUAR", text_SubHeading, screen, halfWidth, 700, orange)
    pygame.display.update()
    roundEnd = True
    while roundEnd:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                roundEnd = False

# função para redefinir coisas como as apostas e as mãos dos jogadores para uma nova rodada (além disso, precisamos redefinir o Y inicial
# valor para todo o texto mostrado no final da rodada
def resetStats():
    global players, startY
    for player in players:
        player.printBank()
        player.resetState()
    startY = 100


# o loop do jogo principal começa aqui

gameOver = False
while gameOver is False:
    startGame()
    showInstructions()
    getNumberOfPlayers()
    getPlayerNames()
    fixCoordinates()
    roundOver = False
    while roundOver is False:
        getPlayerBets()
        newDeck()
        createHands()
        checkBlackJack()
        playTurns()
        showEndRoundScreen()
        resetStats()
