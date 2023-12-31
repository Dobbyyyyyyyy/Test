# -*- coding: utf-8 -*-
"""기말프로젝트_폭탄게임_완성본.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xO3zg5U9NL8NTO3x1vfu8xl8_xNz1qXP
"""

import random as rd
import time as tm
import os

#Cl = 'cls' # Window
Cl = 'clear' # Mac

# ---------- 클래스 정의 ----------
class Bomb_game:
    '''2-4인용 폭탄게임을 하기 위한 여러가지 기능(메소드)을 제공하는 클래스이다.'''
    Exis_card = ['폭탄', '제거', '셔플', '투시', '강탈',
                 '스킵', '밑장빼기', '프라이팬x1', '프라이팬x3'] # 카드이름

    Card_num_2 = [1, 2, 3, 3, 3, 2, 3, 3, 2] # 2인용 카드개수
    Card_num_3 = [1, 3, 3, 4, 4, 3, 4, 4, 2] # 3인용 카드개수
    Card_num_4 = [1, 3, 3, 4, 4, 3, 4, 4, 3] # 4인용 카드개수
    Card_num_tot = Card_num_2 + Card_num_3 + Card_num_4

    How_to_play = '''
    먼저 선을 정하고, 선부터 시계방향으로 돌아가면서 턴을 진행한다.
    자기 턴에는 카드덱에서 카드를 뽑거나, 자신이 들고 있는 카드를 사용할 수 있다.
    카드덱에서 카드를 뽑으면 1턴이 소모되고, 카드를 사용하는 것은 턴을 소모하지 않는다.(특정 카드 제외)''' # 게임방법

    def __init__(self, name):
        self.name = name          # 이름
        self.hav_card = []        # 가지고 있는 카드
        self.turn = False         # 자기 턴인지
        self.num = 1              # 턴의 수
        self.frynum = 0           # 프라이팬 턴의 수
        self.alive = True         # 살아있는지

    def __str__(self):
        return self.name

    @staticmethod
    def setting_deck(pn): # pn은 플래이어 수; 2 3 4
        '''
        시작할 때 덱을 섞는 메소드
        단, 다음의 조건을 만족해야한다.
        1. 폭탄은 처음 4장에서 나올 수 없다.
        2. 폭탄보다 위에 최소 1개의 제거 카드가 있어야한다.
        3. 모든 카드는 3장 이상 연속으로 나올 수 없다.

        섞은 결과는 클래스 속성 Deck 에 들어간다.
        '''
        Bomb_game.Deck = []
        for c, cn in zip(Bomb_game.Exis_card, Bomb_game.Card_num_tot[0+9*(pn-2) : 9+9*(pn-2)]) :
            for _ in range(cn) :
                Bomb_game.Deck.append(c)

        cond1 = True
        cond2 = True
        cond3 = True

        while cond1 or cond2 or cond3 :
            rd.shuffle(Bomb_game.Deck)
            if Bomb_game.Deck.index('폭탄') < 4 : # 조건1 충족 안 되는 경우
                cond1 = True
            else :
                cond1 = False

            if Bomb_game.Deck.index('폭탄') < Bomb_game.Deck.index('제거') : # 조건2 충족 안 되는 경우
                cond2 = True
            else :
                cond2 = False

            for i in range(len(Bomb_game.Deck) - 2) :
                if (Bomb_game.Deck[i] == Bomb_game.Deck[i+1]) and (Bomb_game.Deck[i+1] == Bomb_game.Deck[i+2]) : # 조건3 충족 안 되는 경우
                    cond3 = True
                    break
                else :
                    cond3 = False

    @staticmethod
    def choose_first(instns):
        '''
        선을 정하는 메소드
        모든 인스턴스를 받아서 랜덤으로 선을 정하고, 선으로 정해진 인스턴스를 리턴한다.
        선으로 정해진 인스턴스의 self.turn 을 True 로 바꾼다.
        '''
        first = rd.choice(instns)
        first.turn = True
        return first

    @staticmethod
    def help_word():
        '''
        도움말을 출력하는 메소드
        '''
        print(f'카드 종류\n\
        제거 : {Bomb_game.remove.__doc__}\n\
        셔플 : {Bomb_game.shuffle.__doc__}\n\
        투시 : {Bomb_game.xray.__doc__}\n\
        강탈 : {Bomb_game.steal.__doc__}\n\
        스킵 : {Bomb_game.skip.__doc__}\n\
        밑장빼기 : {Bomb_game.underdraw.__doc__}\n\
        프라이팬 : {Bomb_game.frypan.__doc__}')
        print(f'게임 방법\n{Bomb_game.How_to_play}\n')

    def show_card(self):
        '''
        현재 들고 있는 카드 목록을 출력하는 메소드
        '''
        print('현재 들고 있는 카드 목록은')
        print(self.hav_card, '입니다')

    def draw_card(self):
        '''
        카드를 뽑는 메소드
        setting_deck() 메소드로 만든 Deck 속성에서 왼쪽에서부터 한 장을 뽑고, 그걸 리턴한다.
        뽑힌 카드는 Deck 에서 제거하고, self.hav_card 에 추가한다. 턴을 1 소모한다.
        '''
        card = Bomb_game.Deck.pop(0)
        self.hav_card.append(card)
        self.num -= 1
        if self.frynum > 0 :
            self.frynum -= 1
        return card

    # 카드를 사용할 때 호출되는 메소드들이다.
    # 메소드가 호출될 때 self.hav_card 에서 사용한 카드를 제거한다.
    def remove(self):
        '''
        폭탄을 뽑았을 때 이 카드를 소모해서 한번 살고, 카드덱의 랜덤한 위치에 폭탄이 들어간다. (남은 턴 개수와 상관없이 턴이 넘어간다.)
        '''
        self.hav_card.remove('제거')
        self.hav_card.remove('폭탄')
        Bomb_game.Deck.insert(rd.randrange(len(Bomb_game.Deck) + 1), '폭탄')
        print('제거 카드를 사용하여 살아남았습니다..!')

    def shuffle(self):
        '''
        카드덱을 랜덤으로 섞는다.
        '''
        self.hav_card.remove('셔플')
        rd.shuffle(Bomb_game.Deck)

    def xray(self):
        '''
        카드덱의 가장 위에 있는 3장을 본다.
        '''
        self.hav_card.remove('투시')
        try:
            print(f'윗장부터 {Bomb_game.Deck[0]}, {Bomb_game.Deck[1]}, {Bomb_game.Deck[2]} 입니다 (5초 후 사라집니다)')
        except IndexError:
            if len(Bomb_game.Deck) == 2 :
                print(f'윗장부터 {Bomb_game.Deck[0]}, {Bomb_game.Deck[1]} 입니다 (5초 후 사라집니다)')
            elif len(Bomb_game.Deck) == 1 :
                print(f'윗장부터 {Bomb_game.Deck[0]} 입니다 (5초 후 사라집니다)')
        tm.sleep(5)
        os.system(Cl)

    def steal(self, oppo):
        '''
        상대의 카드 하나를 뺏어온다. (뺏어올 카드는 상대가 정한다.)
        '''
        self.hav_card.remove('강탈')
        print(f'상대의 카드 목록은 {oppo.hav_card} 입니다')
        print(f'어떤 카드를 줄 지 {oppo} 님이 선택해주세요')
        give_card = input()
        os.system(Cl)

        while give_card not in oppo.hav_card :
            print('가지고 있는 카드 중에서 선택해주세요')
            print(f'카드 목록은 {oppo.hav_card} 입니다')
            give_card = input()
            os.system(Cl)

        oppo.hav_card.remove(give_card)
        self.hav_card.append(give_card)
        print(f'{oppo} 님에게서 {give_card} 카드를 빼앗았습니다!')

    def skip(self):
        '''
        턴을 하나 넘긴다.
        '''
        self.hav_card.remove('스킵')
        self.num -= 1
        if self.frynum > 0 :
            self.frynum -= 1

    def underdraw(self):
        '''
        카드덱 가장 아래의 있는 카드를 뽑는다. (턴을 소모하지 않는다.)
        '''
        self.hav_card.remove('밑장빼기')
        card = Bomb_game.Deck.pop(-1)
        self.hav_card.append(card)
        return card

    def frypan(self, oppo, n): # pl은 플래이어 리스트, n은 프라이팬 배수; 1 3
        '''
        x1과 x3 두 종류가 있다.상대 또는 자신에게 사용할 수 있으며, 지목받은 자에게 1 또는 3턴을 부여한다.
        자신이 프라이팬 턴을 가지고 있는 상황에서 사용하면 턴이 추가된다.
        '''
        if n == 1 :
            self.hav_card.remove('프라이팬x1')
        elif n == 3 :
            self.hav_card.remove('프라이팬x3')

        if (not self.frynum) and (oppo.name == self.name) : # 프라이팬 턴이 0일 때 & 나에게 사용
            self.frynum = n
            self.num = self.frynum

        elif self.frynum and (oppo.name == self.name) : # 프라이팬 턴이 0이 아닐 때 & 나에게 사용
            self.frynum += n
            self.num = self.frynum

        elif (not self.frynum) and (oppo.name != self.name) : # 프라이팬 턴이 0일 때 & 상대에게 사용
            oppo.frynum = n
            oppo.num = oppo.frynum
            self.num = 0
            self.frynum = 0

        elif self.frynum and (oppo.name != self.name) : # 프라이팬 턴이 0이 아닐 때 & 상대에게 사용
            oppo.frynum = self.frynum + n
            oppo.num = oppo.frynum
            self.num = 0
            self.frynum = 0


    # 폭탄 카드를 뽑고, 제거 카드가 있을 때 실행되는 메소드
    def bomb(self):
        '''
        폭탄 카드를 뽑고, 제거카드로 제거하지 못할 시 폭탄이 터지고 게임에서 패배한다.
        '''
        print('폭탄이 터집니다!!')
        for i in range(3, 0, -1) :
            print(i)
            tm.sleep(1)
        print('BOOM!!')
        self.alive = False

# ---------- 예외 함수 ----------
def tw_fo_name(names):
    if (len(names) < 2) or (len(names) > 4) :
        raise ValueError('2-4 명의 이름을 입력해주세요')

def dif_name(names):
    for i in range(len(names)-1) :
        if names[i].replace(' ', '') == names[i+1].replace(' ', '') :
            raise ValueError('이름을 다르게 적어주세요')

def no_empty_name(names):
    for name in names :
        if (name.replace(' ', '') == '') :
            raise ValueError('한 글자 이상의 이름을 입력해주세요')

while True :
    # ---------- 시작 세팅 ----------
    os.system(Cl)
    print('폭탄게임에 오신 걸 환영합니다!')
    while True :
        try:
            print("폭탄게임을 하려고 하는 분들의 이름을 ','(쉼표)로 구분하여 적어주세요")
            print('최소 2명에서 최대 4명까지 가능합니다!')
            name_list = input().split(',')
            os.system(Cl)

            tw_fo_name(name_list)
            dif_name(name_list)
            no_empty_name(name_list)

        except Exception as e:
            print('Error :', e)
            continue

        print(f'{len(name_list)}분의 이름이 {name_list} 가 맞으신가요?')
        print("맞으시다면 'yes', 아니라면 'no'를 입력해주세요")
        check_name = input()
        os.system(Cl)

        while (check_name != 'yes') and (check_name != 'no') :
            print('yes 또는 no 를 입력해주세요')
            check_name = input()
            os.system(Cl)

        if check_name == 'yes' :
            break
        elif check_name == 'no' :
            continue

    if len(name_list) == 2 :
        plyer1, plyer2 = Bomb_game(name_list[0]), Bomb_game(name_list[1])
        plyer_list = [plyer1, plyer2]
    elif len(name_list) == 3 :
        plyer1, plyer2, plyer3 = Bomb_game(name_list[0]), Bomb_game(name_list[1]), Bomb_game(name_list[2])
        plyer_list = [plyer1, plyer2, plyer3]
    elif len(name_list) == 4 :
        plyer1, plyer2, plyer3, plyer4 = Bomb_game(name_list[0]), Bomb_game(name_list[1]), Bomb_game(name_list[2]), Bomb_game(name_list[3])
        plyer_list = [plyer1, plyer2, plyer3, plyer4]

    print('좋습니다')
    print('그럼 게임을 시작하겠습니다')
    tm.sleep(2)
    os.system(Cl)

    print('먼저 선을 정하겠습니다')
    for _ in range(3) :
        tm.sleep(1)
        print('.')

    first = Bomb_game.choose_first(plyer_list)
    tm.sleep(2)
    print(f'선은 {first} 님 입니다!')
    plyer_list = plyer_list[plyer_list.index(first):] + plyer_list[:plyer_list.index(first)]
    tm.sleep(3)
    os.system(Cl)


    # ---------- 게임 시작 ----------
    Bomb_game.setting_deck(len(plyer_list))
    print('게임을 시작합니다')
    while list(filter(lambda x : x.alive, plyer_list)) == plyer_list :
        os.system(Cl)
        now_turn = plyer_list[0]
        print(f'{now_turn} 님의 턴!')
        tm.sleep(1.5)

        while now_turn.num > 0 :
            draw_use = None
            getout = True # 탈출 커맨드
            while draw_use != '0' and getout :
                print(f'\n현재 남은 턴 수는 {now_turn.num} 입니다.  {len(Bomb_game.Deck)} 장 남았습니다')
                print("카드를 뽑을거면 '0', 카드를 사용할거면 '1' 을 입력하세요")
                print("(자신이 들고있는 카드를 보고싶으면 'show', 도움이 필요하다면 'help' 를 입력하세요)")
                draw_use = input()
                os.system(Cl)

                if draw_use == 'show' :
                    now_turn.show_card()

                elif draw_use == 'help' :
                    Bomb_game.help_word()

                elif draw_use == '1' :
                    use_card = '제거'
                    while use_card == '제거' :
                        now_turn.show_card()
                        print("어떤 카드를 사용할 지 선택하세요 (뒤로 가려면 'back'을 입력하세요)")
                        use_card = input()
                        os.system(Cl)

                        while (use_card != 'back') and (use_card not in now_turn.hav_card) :
                            now_turn.show_card()
                            print(f"{use_card} 을(를) 찾을 수 없습니다. 다시 입력해주세요 (뒤로 가려면 'back'을 입력하세요)")
                            use_card = input()
                            os.system(Cl)

                        if use_card == 'back' :
                            break
                        elif use_card == '제거' :
                            print('제거 카드는 직접 사용할 수 없습니다. 다른 카드를 선택하세요')
                            continue
                        else :
                            print(f'{use_card} 카드를 사용합니다')
                            if use_card == '셔플' :
                                now_turn.shuffle()

                            elif use_card == '투시' :
                                now_turn.xray()

                            elif use_card == '강탈' :
                                if list(filter(lambda x : x.hav_card, plyer_list[1:]))[0].hav_card == [] :
                                    print('카드를 가지고 있는 상대가 아무도 없습니다..')
                                else :
                                    while True :
                                        print(f'{list(map(lambda x : x.name, plyer_list[1:]))} 중에서')
                                        print('누구의 카드를 빼앗을 지 선택하세요')
                                        stolen = input()
                                        os.system(Cl)

                                        while stolen not in list(map(lambda x : x.name, plyer_list[1:])) :
                                            print(f'{list(map(lambda x : x.name, plyer_list[1:]))} 중에서 골라주세요')
                                            stolen = input()
                                            os.system(Cl)

                                        if list(filter(lambda x : x.name == stolen, plyer_list[1:]))[0].hav_card == [] :
                                            print(f'{stolen} 님은 가지고 있는 카드가 없습니다')
                                            print('다른 분을 선택해주세요')
                                            continue
                                        else :
                                            break

                                    now_turn.steal(*list(filter(lambda x : x.name == stolen, plyer_list[1:])))

                            elif use_card == '스킵' :
                                now_turn.skip()
                                getout = False

                            elif use_card == '밑장빼기' :
                                card = now_turn.underdraw()
                                print(f'{card} 카드를 뽑으셨습니다!')
                                tm.sleep(3)

                            elif use_card == '프라이팬x1' :
                                print(f'{list(map(lambda x : x.name, plyer_list))} 중에서')
                                print('누구에게 사용할 지 선택하세요')
                                gang = input()
                                os.system(Cl)

                                while gang not in list(map(lambda x : x.name, plyer_list)) :
                                    print(f'{list(map(lambda x : x.name, plyer_list))} 중에서 골라주세요')
                                    gang = input()
                                    os.system(Cl)

                                now_turn.frypan(*list(filter(lambda x : x.name == gang, plyer_list)), 1)
                                getout = False

                            elif use_card == '프라이팬x3' :
                                print(f'{list(map(lambda x : x.name, plyer_list))} 중에서')
                                print('누구에게 사용할 지 선택하세요')
                                gang = input()
                                os.system(Cl)

                                while gang not in list(map(lambda x : x.name, plyer_list)) :
                                    print(f'{list(map(lambda x : x.name, plyer_list))} 중에서 골라주세요')
                                    gang = input()
                                    os.system(Cl)

                                now_turn.frypan(*list(filter(lambda x : x.name == gang, plyer_list)), 3)
                                getout = False

            if draw_use == '0' :
                card = now_turn.draw_card()
                print(f'{card} 카드를 뽑으셨습니다!')
                tm.sleep(3)

                if card == '폭탄' :
                    now_turn.num = 0
                    now_turn.frynum = 0
                    if '제거' in now_turn.hav_card :
                        now_turn.remove()
                        tm.sleep(2)
                        os.system(Cl)

                    else :
                        now_turn.bomb()
                        tm.sleep(2)
                        break

            if now_turn.num == 0 : # 턴을 다 소모했을 경우
                now_turn.turn = False
                if list(filter(lambda x : x.frynum != 0, plyer_list)) :
                    get_fried = list(filter(lambda x : x.frynum != 0, plyer_list))[0]
                    get_fried.turn = True
                    plyer_list = plyer_list[plyer_list.index(get_fried):] + plyer_list[:plyer_list.index(get_fried)]
                else :
                    plyer_list[1].turn = True
                    plyer_list[1].num = 1
                    plyer_list.append(plyer_list.pop(0))

    print()
    print('='*50)
    print(f'축하합니다! {list(map(lambda x : x.name, filter(lambda x : x.alive, plyer_list)))} 님은 살아남으셨습니다!!')
    print('='*50)
    print()

    print("다시 하시려면 'yes', 그만하시려면 'no' 를 입력해주세요")
    restart = input()
    os.system(Cl)

    while (restart != 'yes') and (restart != 'no') :
        print("다시 하시려면 'yes', 그만하시려면 'no' 를 입력해주세요")
        restart = input()

    if restart == 'yes' :
        continue
    elif restart == 'no' :
        break

