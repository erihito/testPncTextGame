import pygame
import sys
import random as rd
import copy
########################################파이 게임 및 텍스트#########################################
####################################################################################################
# 파이게임 초기화
pygame.init()
# 색상 정의 (RGB 값)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
BLUE = (100, 100, 255)
# 폰트 설정
font50 = pygame.font.SysFont("malgungothic", 50)
font40 = pygame.font.SysFont("malgungothic", 40)
font30 = pygame.font.SysFont("malgungothic", 30)
font24 = pygame.font.SysFont("malgungothic", 24)
font20 = pygame.font.SysFont("malgungothic", 20)
# 텍스트 
txt_menu_title = font50.render("뉴럴 클라우드 정실 결정전", True, WHITE)
txt_menu_start = font40.render("게임 시작", True, WHITE)
txt_menu_quit = font40.render("게임 종료", True, WHITE)
txt_menu_select = font40.render("▶", True, WHITE)
txt_menu_ctrl = font20.render("조작 : 방향키, 선택 : Z, 취소 : X(버전 정보:0.10817 베타버전)", True, WHITE)
txt_test = font50.render("test text", True, WHITE)
txt_select_doll = font40.render("정실 결정전에 참가할 인형을 선택하세요.", True, WHITE)
txt_select_cursor = font40.render("◀                ▶", True, WHITE)
txt_select_player01 = font40.render("Player1", True, RED)
txt_select_player02 = font40.render("Player2", True, BLUE)
txt_select_finish = font40.render("전투 시작", True, WHITE)
txt_battle_act01 = font30.render("일반 공격", True, WHITE)
txt_battle_act02 = font30.render("고유 스킬", True, WHITE)
txt_battle_act03 = font30.render("궁극 스킬", True, WHITE)
txt_battle_act04 = font30.render("턴 종료", True, WHITE)
statusList = []
def statDisplay(player, pnum, color):
    pygame.draw.rect(screen, color, [window_width - (window_width / pnum ) + (window_width/5), 50, 80, 140])
    txt_tmp = font20.render("*캐릭터 이미지 삽입", True, WHITE)
    rect_tmp = txt_tmp.get_rect(left=(window_width - (window_width / pnum ) + (window_width/5)), bottom=50)
    screen.blit(txt_tmp, rect_tmp)

    statusList.append(font24.render(f"    P{pnum} - {player.name}", True, color))
    statusList.append(font24.render(f"            현재 체력 : [ {player.hp} / {player.maxhp} ]", True, WHITE))
    now = int(player.hp / player.maxhp * 20)
    if now > 14:
        statusList.append(font24.render(f"[" + ("■" * now) + ("□" * (20 - now)) + "]", True, (100, 255, 70)))
    elif now > 9:
        statusList.append(font24.render(f"[" + ("■" * now) + ("□" * (20 - now)) + "]", True, (255, 230, 10)))
    elif now > 3:
        statusList.append(font24.render(f"[" + ("■" * now) + ("□" * (20 - now)) + "]", True, (250, 150, 10)))
    else:
        statusList.append(font24.render(f"[" + ("■" * now) + ("□" * (20 - now)) + "]", True, (180, 20, 10)))
    statusList.append(font24.render(f"    공격력 : {player.atk} / 방어력 : {player.dfs} / 회피율 : {player.avd}%", True, WHITE))
    statusList.append(font24.render(f"    치명률 : {player.crt}% / 치명피해 : {player.crd}%", True, WHITE))
    statusList.append(font24.render(f"    주는 피해 증가 : {player.dmg}% / 받는 피해 감소 : {player.prt}%", True, WHITE))
    statusList.append(font24.render(f"    현재 스킬 쿨타임 : {player.cool}턴", True, WHITE))
    linegap = 250
    for stat in statusList:
        rect_stat = stat.get_rect(left=(window_width - (window_width / pnum) + 40), bottom=linegap)
        screen.blit(stat, rect_stat)
        linegap += 35
    statusList.clear()
    pass
battleLog = []
player_turn = 0
# 화면 설정
window_width = 1150
window_height = 720
screen = pygame.display.set_mode((window_width+50, window_height))
pygame.display.set_caption("뉴럴 클라우드 정실 결정전")
####################################################################################################
########################################파이 게임 및 텍스트#########################################

########################################게임 시스템 관련############################################
####################################################################################################
damage = 0
class PlayerDoll:
    def __init__(self, _name, _hp, _mp, _atk, _dfs, _crt, _crd, _avd, _dmg, _prt, _cool): #스탯 초기화
        self.name = _name #인형의 이름
        self.maxhp = _hp #인형의 최대 체력
        self.hp = _hp #인형의 현재 체력
        self.maxmp = _mp #인형의 최대 체력
        self.mp = _mp #인형의 연산력
        self.atk = _atk #공격력
        self.defaultatk = _atk # 원본 공격력
        self.dfs = _dfs #방어력
        self.defaultdfs = _dfs # 원본 방어력
        self.crt = _crt #치명률
        self.defaultcrt = _crt # 원본 치명률
        self.crd = _crd #치명피해
        self.defaultcrd = _crd # 원본 치명피해
        self.avd = _avd #회피율
        self.defaultavd = _avd # 원본 회피율
        self.dmg = _dmg #주피증
        self.defaultdmg = _dmg # 원본 주피증
        self.prt = _prt #받피감
        self.defaultprt = _prt # 원본 받피감
        self.cool = _cool #스킬 쿨타임
        self.defaultcool = _cool #초기 쿨타임 값
        self.buffcheck = False #버프 상태 체크
        self.buffduration = 0 #버프 지속 시간
        self.nuffcheck = False #디버프 상태 체크
        self.nuffduration = 0 #디버프 지속 시간
    def attack(self, other, color, turn):
        global damage
        crtnan = rd.random() * 100 #치명률
        avdnan = rd.random() * 100 #회피율
        damage = int((self.atk * (0.9 + rd.random() * 0.2))) #공격력의 90%~110% 사이의 랜덤 데미지
        print("-" * 15 + " 일반 공격 결과 " + "-" * 15)
        if avdnan < other.avd: #회피 판정
            print(f"{self.name}의 공격은 빗나갔다...")
            battleLog.append(font24.render(f"{self.name}의 공격은 빗나갔다...", True, color))
            print("-" * 15 + " 현재 인형 스탯 " + "-" * 15)
            return
        if crtnan < self.crt: #치명타 판정
            damage = int((damage * (1 + self.crd / 100)) * (1 + self.dmg / 100) * (1- other.prt / 100))#치명타 피해 계산(치명타는 방어력을 관통)
            mindam = damage * 0.05
            if damage < mindam: #최소 데미지 보정
                damage = mindam
            other.hp -= damage #데미지만큼 공격대상 체력 차감
            print(f"크리티컬 히트! {self.name}은 {other.name}에게 {damage}데미지를 입혔다!") #데미지 출력
            battleLog.append(font24.render(f"크리티컬 히트! {self.name}의 공격은 {other.name}에게 {damage}의 데미지를 입혔다!", True, color))
        else : #평타 판정
            damage = int((damage - other.dfs) * (1 + self.dmg / 100) * (1- other.prt / 100)) #피해 계산
            mindam = damage * 0.05
            if damage < mindam: #최소 데미지 보정
                damage = mindam
            other.hp -= damage #데미지만큼 공격대상 체력 차감
            print(f"{self.name}은 {other.name}에게 {damage}데미지를 입혔다.") #데미지 출력
            battleLog.append(font24.render(f"{self.name}의 공격은 {other.name}에게 {damage}데미지를 입혔다.", True, color))
        if self.isalive() and other.isalive(): #생존여부 체크
            print("-" * 15 + " 현재 인형 스탯 " + "-" * 15)
            print(self)
            print(other)
            print("-" * 50)
            return
    def passiveSkill(self, other, color, turn):
        # if self.name == "솔":
        #     self.hp += 10  # 예: 매 턴 체력 회복
        #     print(f"{self.name}의 패시브 스킬 발동! 체력이 10 회복되었다.")
        # elif self.name == "크로크":
        #     self.dfs += 2  # 예: 방어력 증가
        #     print(f"{self.name}의 패시브 스킬 발동! 방어력이 2 증가했다.")
        # elif self.name == "보름":
        #     self.crd += 2  # 예: 방어력 증가
        #     print(f"{self.name}의 패시브 스킬 발동! 치명 데미지가 2 증가했다.")
        # 다른 캐릭터에 대한 패시브 스킬 구현
        global player_turn
        if self.name == "페르시카-집도":
            if int(turn/2) % 4 == 0:
                damage = int((self.atk * (0.9 + rd.random() * 0.2)) * 0.3)
                other.hp -= damage
                print(f"{self.name}의 축적·들뜸 중첩 발동! 폭축으로 적에게 {damage}의 데미지를 주었다.")
                battleLog.append(font24.render(f"{self.name}의 축적·들뜸 중첩 발동! 폭축으로 적에게 {damage}의 데미지를 주었다.", True, color))
        if self.name == "안토니나":
            if (rd.random() * 100) < 10:
                player_turn += 1
                print(f"{self.name}의 데이터 침식 발동! 적의 턴을 침식시켰다. {self.name}의 턴!")
                battleLog.append(font24.render(f"{self.name}의 데이터 침식 발동! 적의 턴을 침식시켰다. {self.name}의 턴!", True, color))
        pass
    def activeSkill(self, other, color, turn):
        # print("-" * 15 + " 스킬 사용 결과 " + "-")
        # if self.cool == 0:
        #     # if self.name == "솔":
        #     #     damage = self.atk * 2  # 예: 공격력의 2배 데미지
        #     #     other.hp -= damage
        #     #     print(f"{color}{self.name}의 사!자!열!화!참! {other.name}에게 {damage} 데미지를 입혔다.\033[0m")
        #     # elif self.name == "크로크":
        #     #     self.hp += 200  # 예: 체력 회복
        #     #     print(f"{color}{self.name}의 이지스의 방패 발동. 보호막을 200 획득했다.\033[0m")
        #     # elif self.name == "보름":
        #     #     print(f"{color}{self.name}이 추적의 룬을 사용. 다음 2턴간 치명타가 상승한다.\033[0m")
        #     #     self.crt += 50  # 치명률 30 증가
        #     #     self.buffcheck = True  # 버프 활성화
        #     #     self.buffduration = 3   # 버프 지속 시간 3턴
        #     # self.cool = self.defaultcool  # 스킬 사용 후 쿨타임 초기화
        #     #이하 다른 캐릭터에 대한 액티브 스킬 구현
        #     if self.name == "":
        # else:
        #     print("스킬을 사용할 수 없습니다. 쿨타임이 남아 있습니다.")
        # if self.isalive() and other.isalive(): #생존여부 체크
        #     print("-" * 15 + " 현재 인형 스탯 " + "-" * 15)
        #     return
        if self.cool == 0:
            global player_turn
            if self.name == "페르시카-집도":
                sk_damage = int((self.atk * (0.9 + rd.random() * 0.2)))
                sk_damage = int(sk_damage * 0.3)
                sk_damage = int((sk_damage - other.dfs) * (1 + self.dmg / 100) * (1- other.prt / 100))
                mindam = sk_damage * 0.05
                if sk_damage < mindam: #최소 데미지 보정
                    sk_damage = mindam
                other.hp -= sk_damage
                other.hp -= sk_damage
                other.hp -= sk_damage
                other.hp -= sk_damage
                other.hp -= sk_damage
                print(f"{self.name}의 천공·벡터 발산 발동! 폭축으로 적에게 {sk_damage * 5}의 데미지를 주었다.")
                battleLog.append(font24.render(f"{self.name}의 천공·벡터 발산 발동! 폭축으로 적에게 {sk_damage * 5}의 데미지를 주었다.", True, color))
            if self.name == "안토니나":
                sk_damage = int((self.atk * (0.9 + rd.random() * 0.2)))
                sk_damage = int(sk_damage * 2)
                mindam = sk_damage * 0.05
                if sk_damage < mindam: #최소 데미지 보정
                    sk_damage = mindam
                other.hp -= sk_damage
                print(f"{self.name}의 연쇄감염 발동! 트로이 공격으로 적에게 {sk_damage}의 데미지를 주었다.")
                battleLog.append(font24.render(f"{self.name}의 연쇄감염 발동! 트로이 공격으로 적에게 {sk_damage}의 데미지를 주었다.", True, color))
                if (rd.random() * 100) < 25:
                    player_turn += 1
                    print(f"{self.name}의 데이터 침식 발동! 적의 턴을 침식시켰다. {self.name}의 턴!")
                    battleLog.append(font24.render(f"{self.name}의 데이터 침식 발동! 적의 턴을 침식시켰다. {self.name}의 턴!", True, color))
        pass
    def turnEnd(self):
        if self.buffcheck:
            self.buffduration -= 1  # 버프 지속 시간 감소
            if self.buffduration <= 0:  # 버프 지속 시간이 끝나면
                #self.crt = self.defaultcrt  # 치명률 원래대로 복구
                self.buffcheck = False
        if self.nuffcheck:
            self.nuffduration -= 1  # 버프 지속 시간 감소
            if self.nuffduration <= 0:  # 버프 지속 시간이 끝나면
                #self.crt = self.defaultcrt  # 치명률 원래대로 복구
                self.buffcheck = False
        # 쿨타임 감소 처리
        if self.cool > 0:
            self.cool -= 1
    def isalive(self): #생존여부 체크 메소드
        return self.hp > 0
    def clone(self): #캐릭터 선택시 복제
        return copy.deepcopy(self)
    def __str__(self): #캐릭터 스탯 반환
        return (f"{self.name}\n"
                f"HP : {self.hp}, ATK : {self.atk}, DFS : {self.dfs}\n"
                f"CRT : {self.crt}, CRD : {self.crd}, AVD : {self.avd}\n"
                f"DMG : {self.dmg}, PRT : {self.prt}, CSC : {self.cool}\n"
                f"BUF : {self.buffcheck}, NUF : {self.nuffcheck}")# CSC : current skill cool
    
def playerTurn(player, opponent, cursor, color, turn): #플레이어 턴의 행동 처리
    player.passiveSkill(opponent, color, turn)
    if cursor == 0:
        player.attack(opponent, color, turn)
    elif cursor == 1:
        player.activeSkill(opponent, color, turn)
    elif cursor == 2:
        pass
    elif cursor == 3:
        print(f"{player.name}의 턴을 바로 종료 합니다.")
        battleLog.append(font24.render(f"{player.name}의 턴을 바로 종료 합니다.", True, color))
    player.turnEnd()

#인형 리스트               (인형 이름        , 체력     , 연산량  , 공격력   , 방어력  , 치명률  , 치명피해 , 회피율  , 주피증 , 받피감 , 스킬 쿨타임)
wr01_PersicaSE = PlayerDoll("페르시카-집도"  , _hp=1200 , _mp=500 , _atk=120 , _dfs=25 , _crt=20 , _crd=70  , _avd=5  , _dmg=0 , _prt=0 ,_cool=7)
sp01_Antonina  = PlayerDoll("안토니나"       , _hp=1000 , _mp=700 , _atk=100 , _dfs=15 , _crt=30 , _crd=100 , _avd=15 , _dmg=0 , _prt=0 ,_cool=6)
player1doll    = PlayerDoll("지능체01"       , _hp=500  , _mp=300 , _atk=55 , _dfs=10 , _crt=25 , _crd=50  , _avd=5  , _dmg=0 , _prt=0 ,_cool=7)
player2doll    = PlayerDoll("지능체02"       , _hp=550  , _mp=300 , _atk=50 , _dfs=15 , _crt=20 , _crd=70  , _avd=10  , _dmg=0 , _prt=0 ,_cool=7)
doll_list = [wr01_PersicaSE, sp01_Antonina]
####################################################################################################
########################################게임 시스템 관련############################################

########################################화면 출력 및 루프 관련######################################
####################################################################################################
# 타이틀 메뉴 선택 화면
def title_screen():
    # 메인 루프
    title_roop = True
    select_cursor = 0
    while title_roop:
        screen.fill(BLACK)  # 배경을 검은색으로 채우기
        # 텍스트 위치 계산
        rect_menu_title = txt_menu_title.get_rect(center=(window_width // 2, window_height // 4))
        rect_menu_start = txt_menu_start.get_rect(center=(window_width // 2, window_height // 2))
        rect_menu_quit = txt_menu_quit.get_rect(center=(window_width // 2, window_height // 2 + 70))
        rect_menu_ctrl = txt_menu_ctrl.get_rect(left=0, bottom=window_height)
        # 커서 위치 변경
        if select_cursor == 0:
            rect_select = txt_menu_select.get_rect(center=(window_width // 2 - 120, window_height // 2))
        elif select_cursor ==1:
            rect_select = txt_menu_select.get_rect(center=(window_width // 2 - 120, window_height // 2 + 70))
        # 글자 디스플레이
        screen.blit(txt_menu_title, rect_menu_title)
        screen.blit(txt_menu_start, rect_menu_start)
        screen.blit(txt_menu_quit, rect_menu_quit)
        screen.blit(txt_menu_ctrl, rect_menu_ctrl)
        screen.blit(txt_menu_select, rect_select)
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                title_roop = False
            # 키보드 이벤트 처리
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    select_cursor = (select_cursor + 1) % 2  # 메뉴 이동 (0 -> 1 또는 1 -> 0)
                if event.key == pygame.K_UP:
                    select_cursor = (select_cursor - 1) % 2  # 메뉴 이동 (1 -> 0 또는 0 -> 1)
                if event.key == pygame.K_z:
                    if select_cursor == 0:  # 게임 시작 선택
                        dollselect_screen()
                    elif select_cursor == 1:  # 게임 종료 선택
                        title_roop = False
                if event.key == pygame.K_x:  # X 키로 게임 종료
                    if select_cursor == 0:
                        select_cursor = 1
                    elif select_cursor == 1:
                        title_roop = False
        # 화면 업데이트
        pygame.display.flip()

# 인형 선택 화면
def dollselect_screen():
    # 루프 선언
    dollselect_roop = True
    select_cursor_vtc = 0
    select_cursor_hrz01 = 0
    select_cursor_hrz02 = 0
    # 글로벌 변수 호출
    global player1doll
    global player2doll
    while dollselect_roop:
        screen.fill(BLACK)  # 배경을 검은색으로 채우기
        # 예시 텍스트 (게임 시작 화면)
        rect_select_doll = txt_select_doll.get_rect(center=(window_width // 2, window_height // 4))
        screen.blit(txt_select_doll, rect_select_doll)
        rect_player01 = txt_select_player01.get_rect(center=(window_width // 2 - 200, window_height // 2))
        screen.blit(txt_select_player01, rect_player01)
        rect_player02 = txt_select_player02.get_rect(center=(window_width // 2 - 200, window_height // 2 + 100))
        screen.blit(txt_select_player02, rect_player02)

        if select_cursor_vtc == 0:
            rect_cursor = txt_select_cursor.get_rect(center=(window_width // 2 + 50, window_height // 2))
        elif select_cursor_vtc ==1:
            rect_cursor = txt_select_cursor.get_rect(center=(window_width // 2 + 50, window_height // 2 + 100))
        elif select_cursor_vtc == 2:
            rect_cursor = txt_select_cursor.get_rect(center=(window_width // 2 + 50, window_height // 2 + 250))
        screen.blit(txt_select_cursor, rect_cursor)
        
        txt_doll01 = font30.render(f"{select_cursor_hrz01+1}. {doll_list[select_cursor_hrz01].name}", True, WHITE)
        rect_doll01 = txt_doll01.get_rect(center=(window_width // 2 + 50, window_height // 2))
        screen.blit(txt_doll01, rect_doll01)
        txt_doll02 = font30.render(f"{select_cursor_hrz02+1}. {doll_list[select_cursor_hrz02].name}", True, WHITE)
        rect_doll02 = txt_doll02.get_rect(center=(window_width // 2 + 50, window_height // 2 + 100))
        screen.blit(txt_doll02, rect_doll02)
        rect_finish = txt_select_finish.get_rect(center=(window_width // 2 + 50, window_height // 2 + 250))
        screen.blit(txt_select_finish, rect_finish)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 키보드 이벤트 처리
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    select_cursor_vtc = (select_cursor_vtc + 1) % 3  # 메뉴 이동 (0 -> 1 또는 1 -> 0)
                if event.key == pygame.K_UP:
                    select_cursor_vtc = (select_cursor_vtc - 1) % 3  # 메뉴 이동 (1 -> 0 또는 0 -> 1)
                if event.key == pygame.K_RIGHT:
                    if select_cursor_vtc == 0: 
                        select_cursor_hrz01 = (select_cursor_hrz01 + 1) % len(doll_list)  # 메뉴 이동 (0 -> 1 또는 1 -> 0)
                    elif select_cursor_vtc ==1:
                        select_cursor_hrz02 = (select_cursor_hrz02 + 1) % len(doll_list)  # 메뉴 이동 (0 -> 1 또는 1 -> 0)
                if event.key == pygame.K_LEFT:
                    if select_cursor_vtc == 0: 
                        select_cursor_hrz01 = (select_cursor_hrz01 - 1) % len(doll_list)  # 메뉴 이동 (0 -> 1 또는 1 -> 0)
                    elif select_cursor_vtc ==1:
                        select_cursor_hrz02 = (select_cursor_hrz02 - 1) % len(doll_list)  # 메뉴 이동 (0 -> 1 또는 1 -> 0)
                if event.key == pygame.K_z:
                    if select_cursor_vtc != 2:  # 게임 시작 선택
                        select_cursor_vtc += 1
                    elif select_cursor_vtc == 2:
                        player1doll = doll_list[select_cursor_hrz01].clone()
                        print(player1doll)
                        player2doll = doll_list[select_cursor_hrz02].clone()
                        print(player2doll)
                        print("-" * 15  + "인형 선택 완료" + "-" * 15)
                        battle_screen()
                        dollselect_roop = False
                if event.key == pygame.K_x:  # X 키로 게임 종료
                    dollselect_roop = False
        pygame.display.flip()

# 전투 화면
def battle_screen():
    battle_roop = True
    global player1doll
    global player2doll
    print("-" * 15  + "전투 시작!" + "-" * 15)
    print(player1doll)
    print(player2doll)
    select_cursor = 0
    global player_turn
    player_turn = 0
    global battleLog
    battleLog = []
    while battle_roop:
        screen.fill(BLACK)
        #rect_test = txt_test.get_rect(center=(window_width // 2, window_height // 2))
        #screen.blit(txt_test, rect_test)
        rect_battle01 = txt_battle_act01.get_rect(left=window_width // 5-150, bottom=window_height-5)
        rect_battle02 = txt_battle_act02.get_rect(left=window_width // 5 * 2 - 100, bottom=window_height-5)
        #rect_battle03 = txt_battle_act03.get_rect(left=window_width // 5 * 3 - 10, bottom=window_height-5)
        rect_battle04 = txt_battle_act04.get_rect(left=window_width // 5 * 4 + 50, bottom=window_height-5)

        screen.blit(txt_battle_act01, rect_battle01)
        screen.blit(txt_battle_act02, rect_battle02)
        #screen.blit(txt_battle_act03, rect_battle03)
        screen.blit(txt_battle_act04, rect_battle04)
        if select_cursor == 0:
            rect_cursor = txt_menu_select.get_rect(left=window_width // 5-190, bottom=window_height)
        elif select_cursor ==1:
            rect_cursor = txt_menu_select.get_rect(left=window_width // 5 * 2 - 135, bottom=window_height)
        elif select_cursor == 2:
            rect_cursor = txt_menu_select.get_rect(left=window_width // 5 * 3 - 45, bottom=window_height)
        elif select_cursor ==3 :
            rect_cursor = txt_menu_select.get_rect(left=window_width // 5 * 4 + 10, bottom=window_height)
        screen.blit(txt_menu_select, rect_cursor)

        linegap = 0
        for log in battleLog:
            rect_log = log.get_rect(center=(window_width // 2, window_height // 3 * 2 + linegap))
            screen.blit(log, rect_log)
            linegap += 35  
        if len(battleLog) > 5:
            battleLog.pop(0)

        txt_turn = font24.render("◀ 현재 턴", True, (230, 230, 10))
        if player_turn % 2 == 0:
            txt_turnname = font20.render(f"{player_turn+1}턴, 플레이어1의 차례", True, (230, 230, 10))
            rect_turn = txt_turn.get_rect(left=(window_width - (window_width / 1) + 300), bottom=250)
        elif player_turn % 2 == 1:
            txt_turnname = font20.render(f"{player_turn+1}턴, 플레이어2의 차례", True, (230, 230, 10))
            rect_turn = txt_turn.get_rect(left=(window_width - (window_width / 2) + 300), bottom=250)
        rect_turnname = txt_turn.get_rect(center=(window_width // 2 - 30, 20))
        screen.blit(txt_turnname, rect_turnname)
        screen.blit(txt_turn, rect_turn)

        statDisplay(player1doll, 1, RED)
        statDisplay(player2doll, 2, BLUE)

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        select_cursor = (select_cursor + 1) % 4  # 메뉴 이동
                    if event.key == pygame.K_LEFT:
                        select_cursor = (select_cursor - 1) % 4  # 메뉴 이동
                        pass
                    if event.key == pygame.K_z and select_cursor != 2:
                        if player_turn % 2 == 0:
                            print(f"{player_turn}턴의 {player1doll.name}의 선택 : {select_cursor}")
                            if select_cursor != 1 or (select_cursor == 1 and player1doll.cool == 0):
                                playerTurn(player1doll, player2doll, select_cursor, RED, player_turn)
                                player_turn += 1
                            elif select_cursor == 1 and player1doll.cool != 0:
                                print(f"현재 {player1doll.name}의 스킬은 쿨타임입니다")
                                battleLog.append(font24.render(f"현재 {player1doll.name}의 스킬은 쿨타임입니다", True, RED))
                        elif player_turn % 2 == 1:
                            print(f"{player_turn}턴의 {player2doll.name}의 선택 : {select_cursor}")
                            if select_cursor != 1 or (select_cursor == 1 and player2doll.cool == 0):
                                playerTurn(player2doll, player1doll, select_cursor, BLUE, player_turn)
                                player_turn += 1
                            elif select_cursor == 1 and player1doll.cool != 0:
                                print(f"현재 {player2doll.name}의 스킬은 쿨타임입니다")
                                battleLog.append(font24.render(f"현재 {player2doll.name}의 스킬은 쿨타임입니다", True, BLUE))
                    if event.key == pygame.K_x and (not player1doll.isalive() or not player2doll.isalive()):
                        battle_roop = False
        pygame.display.flip()
        if (not player1doll.isalive()) or (not player2doll.isalive()):
            break
    win_roop = True
    print("승리!")
    screen.fill(BLACK)
    if not player1doll.isalive():
        print(f"{player2doll.name}의 승리!")
        while win_roop:
            txt_win = font40.render(f"{player2doll.name}의 승리!", True, BLUE)
            rect_win = txt_win.get_rect(center=(window_width // 2, window_height // 2))
            screen.blit(txt_win, rect_win)
            txt_end = font20.render(f"메인 메뉴로 돌아가려면 X를 누르세요.", True, WHITE)
            rect_end = txt_end.get_rect(left=0, bottom=window_height)
            screen.blit(txt_end, rect_end)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                            win_roop = False
    elif not player2doll.isalive():
        print(f"{player1doll.name}의 승리!")
        while win_roop:
            txt_win = font40.render(f"{player1doll.name}의 승리!", True, RED)
            rect_win = txt_win.get_rect(center=(window_width // 2, window_height // 2))
            screen.blit(txt_win, rect_win)
            txt_end = font20.render(f"메인 메뉴로 돌아가려면 X를 누르세요.", True, WHITE)
            rect_end = txt_end.get_rect(left=0, bottom=window_height)
            screen.blit(txt_end, rect_end)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                            win_roop = False
####################################################################################################
########################################화면 출력 및 루프 관련######################################


########################################메인 함수###################################################
####################################################################################################
def main():
    title_screen()
    # pygame 종료
    pygame.quit()
    sys.exit()
main()
####################################################################################################
########################################메인 함수###################################################
