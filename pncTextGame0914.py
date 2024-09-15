import pygame
import sys
import random as rd
import copy
########################################파이 게임 및 텍스트#########################################
# region 파이게임 관련 변수 및 텍스트
# 파이게임 초기화
pygame.init()
# 화면 설정
WIN_WIDTH = 1200 # 가로
WIN_HEIGHT = 800 # 세로
WIN_SCREEN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("뉴럴 클라우드 텍스트 게임")
# 색상 정의 (RGB 값)
COL_WHITE = (255, 255, 255)
COL_BLACK = (0, 0, 0)
COL_RED = (255, 120, 120)
COL_GREEN = (100, 255, 100)
COL_BLUE = (120, 120, 255)
COL_YELLOW = (230, 230, 10)
# HP바 색상 정의
COL_HP70 = (100, 255, 70)
COL_HP50 = (255, 230, 10)
COL_HP30 = (250, 150, 10)
COL_HP00 = (180, 20, 10)
# MP바 색상 정의
COL_MP00 = (80, 150, 255)
# 폰트 설정
FONT_50 = pygame.font.SysFont("malgungothic", 50)
FONT_40 = pygame.font.SysFont("malgungothic", 40)
FONT_30 = pygame.font.SysFont("malgungothic", 30)
FONT_24 = pygame.font.SysFont("malgungothic", 24)
FONT_22 = pygame.font.SysFont("malgungothic", 22)
FONT_20 = pygame.font.SysFont("malgungothic", 20)
FONT_18 = pygame.font.SysFont("malgungothic", 18)
# 텍스트
TXT_TEST = FONT_50.render("test text", True, COL_WHITE) # 테스트용 텍스트
TXT_MENU_TITLE = FONT_50.render("뉴럴 클라우드 텍스트 게임", True, COL_WHITE) # 게임 타이틀
TXT_MENU_START = FONT_40.render("게임 시작", True, COL_WHITE) # 시작 메뉴
TXT_MENU_MANUEL = FONT_40.render("게임 설명(미구현)", True, COL_WHITE) # 설명 메뉴
TXT_MENU_QUIT = FONT_40.render("게임 종료", True, COL_WHITE) # 종료 메뉴
TXT_MENU_SELECT = FONT_40.render("▶", True, COL_WHITE) # 커서
TXT_MENU_INFO = FONT_20.render("조작 : 방향키, 선택 : Z, 취소 : X(버전 정보:0.240914 베타버전)", True, COL_WHITE) # 버전 및 사용설명
TXT_SELECT_DOLL = FONT_40.render("전투에 참가할 인형을 선택하세요.", True, COL_WHITE) # 인형 선택문
TXT_SELECT_CURSOR = FONT_40.render("◀                ▶", True, COL_WHITE) # 캐릭터 선택 커서
TXT_SELECT_PLAYER01 = FONT_40.render("Player1", True, COL_RED) # 플레이어1
TXT_SELECT_PLAYER02 = FONT_40.render("Player2", True, COL_BLUE) # 플레이어2
TXT_SELECT_FINISH = FONT_40.render("전투 시작", True, COL_WHITE) # 전투 시작 메뉴
TXT_BATTLE_ACT01 = FONT_30.render("일반 공격", True, COL_WHITE) # 기본 평타
TXT_BATTLE_ACT02 = FONT_30.render("연산량 충전", True, COL_WHITE) # 방어 및 충전
TXT_BATTLE_ACT03 = FONT_30.render("고유 스킬", True, COL_WHITE) # 캐릭터 고유 스킬(500)
TXT_BATTLE_ACT04 = FONT_30.render("궁극 스킬", True, COL_WHITE) # 궁극 스킬(1000)
TXT_BATTLE_ACT05 = FONT_30.render("턴 종료", True, COL_WHITE) # 그냥 턴 종료
# endregion
####################################################################################################

############################################글로벌 변수#############################################
# region 전역 변수
SYS_STAGE_ID = 0 # 현재 진행중인 플로우차트 ID
SYS_TURN_COUNT = 0 # 해당 게임의 현재 턴 정보
SYS_TURN_PLAYER = 0 # 해당 턴에서의 플레이어 ID
SYS_STATUS = [] # 플레이어 스탯 출력
SYS_BATTLE_LOG = [] # 전투 로그 기록
SYS_DAMAGE = 0 # 데미지
SYS_HASH = 0 # 연산량
# endregion
####################################################################################################

########################################게임 시스템 관련############################################
# region 클래스, 시스템 함수
# 플레이어돌 캐릭터 클래스
class PlayableDoll:
    # 플레이어 인형 객체 생성(이름, 체력, 연산량, 공격력, 연산력, 방어력, 회피율, 치명률, 치명피해, 주피증, 받피감, 스킬연산량, 궁극기연산량)
    def __init__(self, _name, _hp, _mp, _atk, _hsh, _dfs, _avd, _crt, _crd, _dmg, _prt, _scost, _ucost):
        self.name = _name # 인형의 이름
        self.maxhp = _hp # 인형의 최대 체력
        self.hp = _hp # 인형의 현재 체력
        self.maxmp = _mp # 인형의 최대 체력
        self.mp = 0 # 인형의 연산력
        self.atk = _atk # 공격력
        self.defaultatk = _atk # 원본 공격력
        self.hsh = _hsh # 공격력
        self.defaulthsh = _hsh # 원본 공격력
        self.dfs = _dfs # 방어력
        self.defaultdfs = _dfs # 원본 방어력
        self.avd = _avd # 회피율
        self.defaultavd = _avd # 원본 회피율
        self.crt = _crt # 치명률
        self.defaultcrt = _crt # 원본 치명률
        self.crd = _crd # 치명피해
        self.dmg = _dmg # 주피증
        self.defaultdmg = _dmg # 원본 주피증
        self.prt = _prt # 받피감
        self.defaultprt = _prt # 원본 받피감
        self.scost = _scost # 스킬 코스트
        self.defaultscost = _scost # 원본 코스트
        self.ucost = _ucost # 궁극기 코스트
        self.defaultucost = _ucost # 원본 코스트
        self.value = 0 # 다용도 변수
        self.check = False # 다용도 TF
        self.buffcheck = False # 버프 상태 체크
        self.buffduration = 0 # 버프 지속 시간
        self.nuffcheck = False # 디버프 상태 체크
        self.nuffduration = 0 # 디버프 지속 시간
        self.total_damage = 0 # 총합뎀
        self.total_atk = 0 # 평타뎀
        self.total_psk = 0 # 총 패시브 스킬뎀
        self.total_ask = 0 # 총 액티브 스킬뎀
        self.total_ult = 0 # 궁극기뎀
    # 행동 선택 공격 함수
    def act_normalAttack(self, other, cursor, color, turn):
        global SYS_DAMAGE # 글로벌 데미지 호출
        global SYS_BATTLE_LOG # 글로벌 로그 호출
        nan_crt = rd.random() * 100 # 치명 난수 체크
        nan_avd = rd.random() * 100 # 치명 난수 체크
        SYS_DAMAGE = int((self.atk * (0.9 + rd.random() * 0.2))) # 공격력의 90%~110% 사이의 랜덤 데미지
        min_dam = int(SYS_DAMAGE * 0.05) # 최소 데미지 보정(데미지의 5%)
        if nan_avd < other.avd: # 적 회피 판정
            print(f"{self.name}의 공격은 빗나갔다...")
            SYS_BATTLE_LOG.append(FONT_24.render(f"{self.name}의 공격은 빗나갔다...", True, color))
            return # 빗나갈 경우 공격 함수 탈출
        if nan_crt < self.crt: # 치명타 판정
            SYS_DAMAGE = int(SYS_DAMAGE * (1 + self.crd / 100.0) * (1 + self.dmg / 100.0) * (1 + other.prt / 100.0)) # 치명타는 방어력 관통, 주피증 받피감 계산
            if SYS_DAMAGE < min_dam:
                SYS_DAMAGE = min_dam
            other.hp -= SYS_DAMAGE # 적 체력 감소
            print(f"크리티컬 히트! {self.name}은 {other.name}에게 {SYS_DAMAGE}데미지를 입혔다!")
            SYS_BATTLE_LOG.append(FONT_24.render(f"크리티컬 히트! {self.name}의 공격은 {other.name}에게 {SYS_DAMAGE}의 데미지를 입혔다!", True, color))
        else : # 기본 공격 판정
            SYS_DAMAGE = int((SYS_DAMAGE - other.dfs) * (1 + self.dmg / 100.0) * (1 + other.prt / 100.0)) # 방어력 주피증 받피감 포함 피해 계산
            if SYS_DAMAGE < min_dam:
                SYS_DAMAGE = min_dam
            other.hp -= SYS_DAMAGE # 적 체력 감소
            print(f"{self.name}은 {other.name}에게 {SYS_DAMAGE}데미지를 입혔다.") #데미지 출력
            SYS_BATTLE_LOG.append(FONT_24.render(f"{self.name}의 공격은 {other.name}에게 {SYS_DAMAGE}데미지를 입혔다.", True, color))
        # 평타 연산량 회복은 평타 함수 밖에
        if self.sys_aliveCheck() and other.sys_aliveCheck(): # 콘솔 스탯 출력
            print(self)
            print(other)
            return
    # 행동 선택 충전 함수
    def act_hashCharge(self, color, type):
        global SYS_HASH # 글로벌 연산량 호출
        SYS_HASH = int((self.hsh * (0.7 + rd.random() * 0.6))) # 연산력의 70%~130% 사이의 랜덤 충전량
        if type == "atk": # 공격시 기초 연산 회복
            if(self.mp < self.maxmp):
                SYS_HASH = int(SYS_HASH * 0.5) # 기본 회복량의 50% 회복
        if type == "chg": # 충전시 연산 회복
            if(self.mp < self.maxmp):
                SYS_HASH = int(SYS_HASH + (self.maxmp * 0.1)) # 연산통 비례 회복 + 기본 회복량 100%
                SYS_BATTLE_LOG.append(FONT_24.render(f"충전을 통해 {self.name}의 연산량을 {SYS_HASH}만큼 확보했다.", True, color))
        #기타 옵션 추가...예정
        self.mp += SYS_HASH # 회복
        if (self.mp > self.maxmp): # 최대 연산량 오버플로우 방지
            self.mp = self.maxmp
    # 행동 선택 패시브 스킬 함수(자동 발동)
    def act_passiveSkill(self, other, cursor, color, turn): # 패시브 스킬 구현부
        # 글로벌 변수 호출
        global SYS_BATTLE_LOG # 전투 로그
        global SYS_TURN_PLAYER #현재 턴 소유주 호출
        global SYS_DAMAGE # 글로벌 데미지 호출
        SYS_DAMAGE = int((self.atk * (0.9 + rd.random() * 0.2))) # 공격력의 90%~110% 사이의 랜덤 데미지
        # 패시브 스킬은 매번 턴 개시마다 발동
        if self.name == None:
            pass
        elif self.name == "페르시카-집도":
            if self.value == 0: # 다용도 변수가 0이 될 때 마다
                dam_psk = int(SYS_DAMAGE * 0.3) # 스킬 배수
                dam_psk = int((dam_psk - other.dfs) * (1 + self.dmg / 100) * (1- other.prt / 100)) # 방어 계산
                if dam_psk < 0:
                    dam_psk = 1
                other.hp -= dam_psk # 피해 적용
                SYS_BATTLE_LOG.append(FONT_24.render(f"{self.name}의 '축적·들뜸 중첩' 발동. 폭축으로 적에게 {dam_psk}의 데미지를 주었다.", True, color))
            self.value += 1 # 매 턴마다 변수 값 증가
            if self.value == 4: # 5턴마다 쿨타임 초기화
                self.value = 0
        elif self.name == "안토니나":
            if (rd.random() * 100) < 10 and cursor != 3: # 랜덤 난수 생성
                SYS_BATTLE_LOG.append(FONT_24.render(f"{self.name}의 '데이터 침식' 발동. 적의 턴을 침식시켰다.", True, color))
                if SYS_TURN_PLAYER == 1: # 턴 변경 방지
                    SYS_TURN_PLAYER = 2
                elif SYS_TURN_PLAYER ==2:
                    SYS_TURN_PLAYER = 1
                return
            if self.check == True:
                if (rd.random() * 100) < 25: # 랜덤 난수 생성
                    self.check = False
                    SYS_BATTLE_LOG.append(FONT_24.render(f"{self.name}의 '데이터 침식' 발동! 적의 턴을 침식시켰다!", True, color))
                    if SYS_TURN_PLAYER == 1: # 턴 변경 방지
                        SYS_TURN_PLAYER = 2
                    elif SYS_TURN_PLAYER ==2:
                        SYS_TURN_PLAYER = 1
                    return
            if self.value > 0 and cursor != 3: # 궁극기로 발동하는 추가 패시브 강화
                self.value -= 1 # 횟수 감소
                if (rd.random() * 100) < 40: # 랜덤 난수 생성
                    SYS_BATTLE_LOG.append(FONT_24.render(f"{self.name}의 '데이터 침식' 발동!! 적의 턴을 침식시켰다!!", True, color))
                    if SYS_TURN_PLAYER == 1: # 턴 변경 방지
                        SYS_TURN_PLAYER = 2
                    elif SYS_TURN_PLAYER ==2:
                        SYS_TURN_PLAYER = 1
                    return
        elif self.name == "클루카이":
            if cursor == 0 and (rd.random() * 100) < 25: # 랜덤 난수 생성
                dam_psk = [int(((self.atk * (0.8 + rd.random() * 0.4)) * 0.15) * (1 + self.dmg / 100) * (1 - other.prt / 100)) for i in range(3)]
                other.hp -= sum(dam_psk) # 피해 적용
                SYS_BATTLE_LOG.append(FONT_24.render(f"{self.name}의 '피어나는 죽음' 발동. 삼점사로 적에게 {sum(dam_psk)}={dam_psk}의 데미지를 주었다.", True, color))
        elif self.name == "메메코":
            if turn == 150: # 150턴 째가 되면 자살
                self.hp = 0
        pass
    # 행동 선택 액티브 스킬 함수(선택 발동)
    def act_activeSkill(self, other, cursor, color, turn): # 액티브 스킬 구현부
        # 글로벌 변수 호출
        global SYS_BATTLE_LOG # 전투 로그
        global SYS_TURN_PLAYER #현재 턴 소유주 호출
        global SYS_DAMAGE # 데미지
        SYS_DAMAGE = int((self.atk * (0.9 + rd.random() * 0.2))) # 공격력의 90%~110% 사이의 랜덤 데미지
        # 액티브 스킬은 scost를 사용
        if self.name == None:
            pass
        elif self.name == "페르시카-집도":
            dam_ask = [int(((self.atk * (0.9 + rd.random() * 0.2)) * 0.6 - other.dfs) * (1 + self.dmg / 100) * (1 - other.prt / 100)) for i in range(5)]
            dam_ask = sys_negativeDamage(dam_ask, int(SYS_DAMAGE * 0.05)) # 방어력 때문에 음수 발생하는 것 방지
            other.hp -= sum(dam_ask)
            SYS_BATTLE_LOG.append(FONT_24.render(f"{self.name}의 '천공·벡터 발산' 발동! 폭축으로 적에게 {sum(dam_ask)}={dam_ask}의 데미지를 주었다!", True, color))
        elif self.name == "안토니나":
            self.check = True # 패시브 강화
            dam_ask = int(((SYS_DAMAGE * 2.2)- other.dfs) * (1 + self.dmg / 100) * (1- other.prt / 100))
            other.hp -= dam_ask # 피해 적용
            SYS_BATTLE_LOG.append(FONT_24.render(f"{self.name}의 '연쇄감염' 발동! 트로이 공격으로 적에게 {dam_ask}의 데미지를 주었다!", True, color))
            if (rd.random() * 100) < 35: # 랜덤 난수 생성
                SYS_BATTLE_LOG.append(FONT_24.render(f"이어서 '데이터 침식' 발동! 적의 턴을 침식시켰다!", True, color))
                if SYS_TURN_PLAYER == 1: # 턴 변경 방지
                    SYS_TURN_PLAYER = 2
                elif SYS_TURN_PLAYER ==2:
                    SYS_TURN_PLAYER = 1
        elif self.name == "클루카이":
            dam_ask = int(((SYS_DAMAGE * 2.7)) * (1 + self.dmg / 100) * (1- other.prt / 100)) # 데미지 계산
            other.hp -= dam_ask # 피해 적용
            SYS_BATTLE_LOG.append(FONT_24.render(f"{self.name}의 '밤하늘의 천둥' 발동! 은멸 유탄으로 적에게 {dam_ask}의 데미지를 주었다!", True, color))
        elif self.name == "메메코":
            other.hp -= other.maxhp // 10 # 적 체력 절대치 감소
            SYS_BATTLE_LOG.append(FONT_24.render(f"？？？의 '￥％, ￥＃＊＆!' 발동! ￥＊＆＃으로 적에게 {other.maxhp // 10}의 데미％￥＃＆￥＆...!", True, color))
        pass
    # 행동 선택 궁극기 함수(선택 발동)
    def act_ultimateSkill(self, other, cursor, color, turn): # 궁극기 구현부
        # 글로벌 변수 호출
        global SYS_BATTLE_LOG # 전투 로그
        global SYS_TURN_PLAYER #현재 턴 소유주 호출
        global SYS_DAMAGE # 데미지
        SYS_DAMAGE = int((self.atk * (0.8 + rd.random() * 0.4))) # 데미지 계산(궁극기는 좀더 변동폭 크게)
        # 궁극 스킬은 ucost를 사용
        if self.name == None:
            pass
        elif self.name == "페르시카-집도":
            dam_usk = int((SYS_DAMAGE * 4) * (1 + self.dmg / 100) * (1 - other.prt / 100))
            other.hp -= dam_usk
            SYS_BATTLE_LOG.append(FONT_24.render(f"{self.name}의 폭연·선형 분열 발동!! 적에게 {dam_usk}의 데미지를 주었다!!", True, color))
        elif self.name == "안토니나":
            if True: # 랜덤 난수 생성
                self.value = 3 # 패시브 기회 3회 추가
                SYS_BATTLE_LOG.append(FONT_24.render(f"{self.name}의 '글로벌 해킹' 발동!! 적의 턴을 침식시켰다!!", True, color))
                if SYS_TURN_PLAYER == 1: # 턴 변경 방지
                    SYS_TURN_PLAYER = 2
                elif SYS_TURN_PLAYER ==2:
                    SYS_TURN_PLAYER = 1
                return
        elif self.name == "클루카이":
            dam_usk = [int(((self.atk * (0.8 + rd.random() * 0.4)) * 1.2 - other.dfs) * (1 + self.dmg / 100) * (1 - other.prt / 100)) for i in range(5)]
            dam_usk = sys_negativeDamage(dam_usk, int(SYS_DAMAGE * 0.05)) # 방어력 때문에 음수 발생하는 것 방지
            other.hp -= sum(dam_usk) # 피해 적용
            SYS_BATTLE_LOG.append(FONT_24.render(f"{self.name}의 '데이브레이커' 발동!! 공습 지원으로 적에게 {sum(dam_usk)}={dam_usk}의 데미지를 주었다!!", True, color))
        elif self.name == "메메코":
            other.hp -= other.maxhp // 3 # 적 체력 절대치 감소
            other.maxhp -= other.maxhp // 3 # 적 최대체력 절대치 감소
            SYS_BATTLE_LOG.append(FONT_24.render(f"？？？의 '￥＃＆％＊＆￥!' 발＃!! ￥＊＆＃으로 적￥ {other.maxhp // 5 // 10}％ ￥＃＆지＊＃다...!!", True, color))
        pass
    # 지속형 버프/디버프 체크 및 스탯 초기화
    def sys_durationCheck(self):
        if self.buffcheck:
            self.buffduration -= 1
            if self.buffduration <= 0:
                #여기에 스탯 초기화
                self.buffcheck = False
        if self.nuffcheck:
            self.nuffduration -= 1
            if self.nuffduration <= 0:
                #여기에 스탯 초기화
                self.nuffcheck = False
    # 생존 여부 체크
    def sys_aliveCheck(self):
        return self.hp > 0 # 생존 여부 반환(생존 True, 사망 False)
    # 캐릭터 복사 메소드
    def clone(self):
        return copy.deepcopy(self)
    # 캐릭터 스탯 반환
    def __str__(self):
        return (f"{self.name}\n"
                f"HP : {self.hp}, MP : {self.mp}\n"
                f"ATK : {self.atk}, HSH : {self.hsh}\n"
                f"DFS : {self.dfs}, AVD : {self.avd}\n"
                f"CRT : {self.crt}, CRD : {self.crd}\n"
                f"DMG : {self.dmg}, PRT : {self.prt}\n"
                f"BUF : {self.buffcheck}, NUF : {self.nuffcheck}")
# 플레이어 턴 시스템 함수
def sys_playerTurn(player, opponent, cursor, color, turn): # 플레이어 턴의 행동 처리
    # 글로벌 턴 관련 변수 호출
    global SYS_TURN_COUNT # 현재 턴 값
    global SYS_TURN_PLAYER # 현재 턴 소유자
    global SYS_BATTLE_LOG # 전투 로그
    player.act_passiveSkill(opponent, cursor, color, turn) # 턴 개시 시 패시브 발동
    if cursor == 0: # 일반 공격
        player.act_normalAttack(opponent, cursor, color, turn) # 행동 선택 공격
        player.act_hashCharge(color, "atk") # 행동 선택 충전(타입:공격)
    elif cursor == 1: # 연산량 충전
        player.act_hashCharge(color, "chg") # 행동 선택 충전
    elif cursor == 2: # 고유 스킬
        player.mp -= player.scost
        player.act_activeSkill(opponent, cursor, color, turn) # 행동 선택 액티브 스킬
    elif cursor == 3: # 궁극 스킬
        player.mp -= player.ucost
        player.act_ultimateSkill(opponent, cursor, color, turn) # 행동 선택 궁극기
    elif cursor == 4:
        print(f"{player.name}의 턴을 바로 종료 합니다.")
        SYS_BATTLE_LOG.append(FONT_24.render(f"{player.name}의 턴을 바로 종료 합니다.", True, color))
    ### 턴 종료 수치 증가 ###
    SYS_TURN_COUNT += 1 # 턴 종료시 턴 수치 증가
    #########################
    # 턴 소유주 변경
    if SYS_TURN_PLAYER == 1:
        SYS_TURN_PLAYER = 2
    elif SYS_TURN_PLAYER ==2:
        SYS_TURN_PLAYER = 1
    return
# 플레이어 스테이터스 출력 시스템 함수
def sys_statDisplay(player, pnum, color): # 플레이어 클래스, 플레이어 ID(SYS_TURN_PLAYER)
    # 글로벌 스테이터스 호출
    global SYS_STATUS
    # 이미지 출력 위치 선정
    pos_x = WIN_WIDTH - (WIN_WIDTH / pnum) + 240 # x 좌표
    pos_y = 20 # y 좌표
    # 여기 포지션 계산
    sys_eraserDisplay(player.name, pos_x, pos_y) # 플레이어 캐릭터 이미지 출력
    # 캐릭터 스탯 출력부
    SYS_STATUS.append(FONT_24.render(f"            P{pnum} - {player.name}", True, color))
    SYS_STATUS.append(FONT_22.render(f"      현재 생명력 : [ {player.hp} / {player.maxhp} ]", True, COL_WHITE))
    now = int(player.hp / player.maxhp * 20)
    if now > 14:
        SYS_STATUS.append(FONT_18.render(f"[" + ("■" * now) + ("□" * (20 - now)) + "]", True, COL_HP70))
    elif now > 9:
        SYS_STATUS.append(FONT_18.render(f"[" + ("■" * now) + ("□" * (20 - now)) + "]", True, COL_HP50))
    elif now > 3:
        SYS_STATUS.append(FONT_18.render(f"[" + ("■" * now) + ("□" * (20 - now)) + "]", True, COL_HP30))
    else:
        SYS_STATUS.append(FONT_18.render(f"[" + ("■" * now) + ("□" * (20 - now)) + "]", True, COL_HP00))
    SYS_STATUS.append(FONT_22.render(f"      현재 연산량 : [ {player.mp} / {player.maxmp} ]", True, COL_WHITE))
    now = int(player.mp / player.maxmp * 20)
    if now > 14:
        SYS_STATUS.append(FONT_18.render(f"[" + ("■" * now) + ("□" * (20 - now)) + "]", True, COL_MP00))
    elif now > 9:
        SYS_STATUS.append(FONT_18.render(f"[" + ("■" * now) + ("□" * (20 - now)) + "]", True, COL_MP00))
    elif now > 3:
        SYS_STATUS.append(FONT_18.render(f"[" + ("■" * now) + ("□" * (20 - now)) + "]", True, COL_MP00))
    else:
        SYS_STATUS.append(FONT_18.render(f"[" + ("■" * now) + ("□" * (20 - now)) + "]", True, COL_MP00))
    SYS_STATUS.append(FONT_24.render(f"공격력 : {player.atk} / 연산력 : {player.hsh}", True, COL_WHITE))
    SYS_STATUS.append(FONT_24.render(f"방어력 : {player.dfs} / 회피율 : {player.avd}%", True, COL_WHITE))
    SYS_STATUS.append(FONT_24.render(f"치명률 : {player.crt}% / 치명피해 : {player.crd}%", True, COL_WHITE))
    SYS_STATUS.append(FONT_24.render(f"고유 스킬 : {player.scost} hr / 궁극 스킬 : {player.ucost} hr", True, COL_WHITE))
    #SYS_STATUS.append(FONT_22.render(f"주는 피해 증가 : {player.dmg}% / 받는 피해 감소 : {player.prt}%", True, COL_WHITE))
    # 출력 행 초기 위치
    line_space = 250
    for stat in SYS_STATUS:
        rect_stat = stat.get_rect(left=(WIN_WIDTH - (WIN_WIDTH / pnum) + 75), bottom=line_space)
        WIN_SCREEN.blit(stat, rect_stat)
        #sys_textDisplay(stat, WIN_WIDTH - (WIN_WIDTH / pnum) + 300, line_space)
        line_space += 30 # 행간 간격
    SYS_STATUS.clear()
    pass
# 플레이어 캐릭터 이미지 출력 시스템 함수
def sys_eraserDisplay(name, x, y):
    erasers = {
    "페르시카-집도": pygame.image.load("./data/ers_persica.png"),
    "안토니나": pygame.image.load("./data/ers_antonina.png"),
    "클루카이": pygame.image.load("./data/ers_clukay.png"),
    # "드 레이시": pygame.image.load("./data/delacey.png"),
    # "하츠치리": pygame.image.load("./data/hatsuchiri.png"),
    # "센타우레이시": pygame.image.load("./data/centaureissi.png"),
    # "에오스": pygame.image.load("./data/eos.png"),
    # "강우": pygame.image.load("./data/jiangyu.png"),
    # "쿠로": pygame.image.load("./data/kuro.png"),
    # "린드": pygame.image.load("./data/lind.png"),
    # "보름": pygame.image.load("./data/luna.png"),
    # "사쿠야": pygame.image.load("./data/sakuya.png")
    "메메코": pygame.image.load("./data/ers_memeko.png"),
    } # 실행파일과 같은 경로에 있는 data 폴더로부터 이미지 호출하여 저장
    eraser = erasers[name] # 딕셔너리에서 이름에 따른 이미지 호출
    eraser = pygame.transform.scale(eraser, (80, 150)) # 이미지 리스케일
    WIN_SCREEN.blit(eraser, (x, y)) # x, y 좌표에 이미지 출력
    pass
# 지정된 텍스트 변수를 입력받아 x, y에 출력하는 함수
def sys_textDisplay(text, x, y):
    text_rect = text.get_rect() # 텍스트 rect 선언
    text_rect.center = (x, y) # rect 위치 지정
    WIN_SCREEN.blit(text, text_rect) # 스크린 출력
#
def sys_negativeDamage(dam, m): # 다단히트 공격에서 음수 발생 방지
    for i in range(len(dam)):
        if dam[i] < 0:
            dam[i] = m  # 0보다 낮은 데미지를 최소 데미지로 변환
    return dam  # 대체된 리스트 반환
# endregion
####################################################################################################

########################################인형 스탯 설정########################################
# region 게임 씬 관련 함수
# 플레이어블 캐릭터 (self, _name, _hp, _mp, _atk, _hsh, _dfs, _avd, _crt, _crd, _dmg, _prt):
wr01_PersicaSE = PlayableDoll("페르시카-집도", _hp=1600, _mp=1350, _atk=110, _hsh=110, _dfs=20, _avd=10, _crt=15, _crd=70, _dmg=0, _prt=0, _scost=450, _ucost=1000)
sp01_Antonina  = PlayableDoll("안토니나", _hp=1450, _mp=1700, _atk=90, _hsh=120, _dfs=10, _avd=15, _crt=20, _crd=50, _dmg=0, _prt=0, _scost=500, _ucost=900)
sn01_Clukay = PlayableDoll("클루카이", _hp=1500, _mp=1500, _atk=100, _hsh=100, _dfs=15, _avd=5, _crt=25, _crd=70, _dmg=0, _prt=0, _scost=550, _ucost=1200)
# 테스트용 및 초기화용 캐릭터
pc1_Doll = PlayableDoll("지능체01", _hp=1000, _mp=1000, _atk=100, _hsh=100, _dfs=10, _avd=5, _crt=15, _crd=50, _dmg=0, _prt=0, _scost=500, _ucost=1000)
pc2_Doll = PlayableDoll("지능체02", _hp=1000, _mp=1000, _atk=100, _hsh=100, _dfs=10, _avd=5, _crt=15, _crd=50, _dmg=0, _prt=0, _scost=500, _ucost=1000)
ex01_Memeko = PlayableDoll("메메코", _hp=8000, _mp=8000, _atk=1, _hsh=100, _dfs=80, _avd=1, _crt=1, _crd=80000, _dmg=0, _prt=0, _scost=3000, _ucost=5000)
# 플레이어블 캐릭터 리스트
doll_list = [wr01_PersicaSE, sp01_Antonina, sn01_Clukay, ex01_Memeko]
# endregion
####################################################################################################


########################################화면 출력 및 게임 씬########################################
# region 게임 씬 관련 함수
def scn_titleMenu(): # 타이틀 씬 스테이지 ID 0
    # 커서 변수 선언
    sys_cursor_v = 0
    # 타이틀메뉴 루프 변수
    loop_st0 = True
    sys_story = True # 스토리 보기
    # 타이틀 화면 루프 시작
    while loop_st0 :
        WIN_SCREEN.fill(COL_BLACK) # 배경 화면 검정색으로 지정
        # 텍스트 출력
        sys_textDisplay(TXT_MENU_TITLE, WIN_WIDTH // 2, WIN_HEIGHT // 4) # 메인 타이틀
        sys_textDisplay(TXT_MENU_START, WIN_WIDTH // 2, WIN_HEIGHT // 2) # 게임 시작
        sys_textDisplay(TXT_MENU_MANUEL, WIN_WIDTH // 2, WIN_HEIGHT // 2 + 70) # 게임 설명
        sys_textDisplay(TXT_MENU_QUIT, WIN_WIDTH // 2, WIN_HEIGHT // 2 + 140) # 게임 종료
        sys_textDisplay(TXT_MENU_INFO, WIN_WIDTH // 4 , WIN_HEIGHT * 0.97) # 게임 정보
        # 커서 이동
        if sys_cursor_v == 0:
            sys_textDisplay(TXT_SELECT_CURSOR, WIN_WIDTH // 2, WIN_HEIGHT // 2 )
        elif sys_cursor_v == 1:
            sys_textDisplay(TXT_SELECT_CURSOR, WIN_WIDTH // 2, WIN_HEIGHT // 2 + 70)
        elif sys_cursor_v == 2:
            sys_textDisplay(TXT_SELECT_CURSOR, WIN_WIDTH // 2, WIN_HEIGHT // 2 + 140)
        # 사용자 입력 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop_st0 = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN: # 커서 상하 이동
                    sys_cursor_v = (sys_cursor_v + 1) % 3
                if event.key == pygame.K_UP: # 커서 상하 이동
                    sys_cursor_v = (sys_cursor_v - 1) % 3
                if event.key == pygame.K_z: # z키 입력으로 선택
                    if sys_cursor_v == 0: # 게임 시작 선택
                        if sys_story:
                            scn_storyShow() # 스토리 설명 씬 출력
                            sys_story = False # 스토리는 게임 실행해서 한 번만
                        scn_dollSelect() # 인형 선택 씬으로 이동
                        pass
                    elif sys_cursor_v == 1: # 게임 설명 선택
                        # 게임 설명 이동
                        loop_st0 = False # 임시(구현시 삭제)
                    elif sys_cursor_v == 2: # 게임 종료 선택
                        loop_st0 = False
                if event.key == pygame.K_x: # X 키로 게임 종료
                    if sys_cursor_v != 2: # 커서가 종료에 있지 않으면
                        sys_cursor_v = 2 # 종료로 이동
                    elif sys_cursor_v == 2: #게임 종료
                        loop_st0 = False
        # 화면 업데이트
        pygame.display.flip()

def scn_storyShow(): # 스토리 설명 씬 임시 스테이지 ID 0
    # 루프 변수
    loop_st0 = True
    # 스토리 출력용 임시변수
    sys_story = []
    sys_story.append(FONT_40.render("마즈와,", True, COL_WHITE))
    sys_story.append(FONT_30.render("마그라세아에서 교수의 정실을 결정하는 회의가 열렸다.", True, COL_WHITE))
    sys_story.append(FONT_30.render("수 많은 인형들이 정실부인을 자처하며 나섰지만,", True, COL_WHITE))
    sys_story.append(FONT_30.render("정실 자리는 화투 쳐서 따는게 아닌 법...", True, COL_WHITE))
    sys_story.append(FONT_30.render("난세의 마그라세아에서는 강한 자만이 살아남을 수 있다.", True, COL_WHITE))
    sys_story.append(FONT_30.render("강함이란 무엇인가...", True, COL_WHITE))
    sys_story.append(FONT_30.render("강함이란 억지를 관철하는 힘! 의지를 관철하는 힘!", True, COL_WHITE))
    sys_story.append(FONT_30.render("주먹에 염원을 담아서... 원하는 것을 얻어라!", True, COL_WHITE))
    sys_story.append(FONT_30.render("이것은 명령이다, 압도적인 힘으로 내리는...", True, COL_WHITE))
    sys_story.append(FONT_30.render("", True, COL_WHITE))
    sys_story.append(FONT_40.render("머뭇거릴 틈이 없다!", True, COL_WHITE))
    sys_story.append(FONT_30.render("", True, COL_WHITE))
    sys_story.append(FONT_40.render("정실 결정 최대 토너먼트 개마아아아악!!", True, COL_WHITE))
    # 스토리 출력 루프 시작
    while loop_st0:
        WIN_SCREEN.fill(COL_BLACK) # 배경 화면 검정색으로 지정
        # 스토리 출력
        line_space = 120
        for story in sys_story:
            rect_story = story.get_rect(left=(WIN_WIDTH/6), bottom=line_space)
            WIN_SCREEN.blit(story, rect_story)
            line_space += 40 # 행간 간격
        #sys_textDisplay(TXT_TEST, WIN_WIDTH // 2, WIN_HEIGHT // 2) # 테스트
        # 사용자 입력 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN: # 키를 무엇이든 누르면 넘어감
                if event.key == pygame.K_z:
                    loop_st0 = False
                if event.key == pygame.K_x:
                    loop_st0 = False
        pygame.display.flip()

def scn_dollSelect(): # 플레이어블 인형 선택 씬 스테이지 ID 1
    # 글로벌 변수 선언
    global pc1_Doll
    global pc2_Doll
    # 커서 변수 선언
    sys_cursor_v = 0
    sys_cursor_h1 = 0
    sys_cursor_h2 = 0
    # 루프 변수
    loop_st1 = True
    # 플레이어블 인형 선택 루프 시작
    while loop_st1:
        WIN_SCREEN.fill(COL_BLACK) # 배경 화면 검정색으로 지정
        sys_textDisplay(TXT_SELECT_DOLL, WIN_WIDTH // 2, WIN_HEIGHT // 4) # 인형 선택 메뉴 출력
        sys_textDisplay(TXT_SELECT_PLAYER01, WIN_WIDTH // 2 - 250, WIN_HEIGHT // 2) # 플레이어1 출력
        sys_textDisplay(TXT_SELECT_PLAYER02, WIN_WIDTH // 2 - 250, WIN_HEIGHT // 2 + 100) # 플레이어 2출력
        # 커서 이동
        if sys_cursor_v == 0: # 커서 세로 위치에 따라
            sys_textDisplay(TXT_SELECT_CURSOR, WIN_WIDTH // 2, WIN_HEIGHT // 2) # 플레이어1 출력
        elif sys_cursor_v == 1:
            sys_textDisplay(TXT_SELECT_CURSOR, WIN_WIDTH // 2, WIN_HEIGHT // 2 + 100) # 플레이어2 출력
        elif sys_cursor_v == 2:
            sys_textDisplay(TXT_SELECT_CURSOR, WIN_WIDTH // 2, WIN_HEIGHT // 2 + 250) # 전투 시작 출력
        txt_temp = FONT_30.render(f"{doll_list[sys_cursor_h1].name}", True, COL_WHITE)
        sys_textDisplay(txt_temp, WIN_WIDTH // 2, WIN_HEIGHT // 2) # 플레이어1 인형 선택지 출력
        txt_temp = FONT_30.render(f"{doll_list[sys_cursor_h2].name}", True, COL_WHITE)
        sys_textDisplay(txt_temp, WIN_WIDTH // 2, WIN_HEIGHT // 2 + 100) # 플레이어2 인형 선택지 출력
        sys_textDisplay(TXT_SELECT_FINISH, WIN_WIDTH // 2, WIN_HEIGHT // 2 + 250) # 선택 완료 후 전투 시작

        # 사용자 입력 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 키보드 이벤트 처리
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN: # 커서 상하 이동
                    sys_cursor_v = (sys_cursor_v + 1) % 3
                if event.key == pygame.K_UP: # 커서 상하 이동
                    sys_cursor_v = (sys_cursor_v - 1) % 3
                if event.key == pygame.K_RIGHT: # 커서 좌우 이동
                    if sys_cursor_v == 0: # 1p
                        sys_cursor_h1 = (sys_cursor_h1 + 1) % len(doll_list) # 인형 리스트 이동
                    elif sys_cursor_v ==1: # 2p
                        sys_cursor_h2 = (sys_cursor_h2 + 1) % len(doll_list) # 인형 리스트 이동
                if event.key == pygame.K_LEFT: # 커서 좌우 이동
                    if sys_cursor_v == 0: # 1p
                        sys_cursor_h1 = (sys_cursor_h1 - 1) % len(doll_list) # 인형 리스트 이동
                    elif sys_cursor_v ==1: # 2p
                        sys_cursor_h2 = (sys_cursor_h2 - 1) % len(doll_list) # 인형 리스트 이동
                if event.key == pygame.K_z: # z키 입력으로 선택
                    if sys_cursor_v != 2: # 커서 이동
                        sys_cursor_v += 1 # 커서 이동
                    elif sys_cursor_v == 2: # 게임 시작 선택
                        pc1_Doll = doll_list[sys_cursor_h1].clone() # 플레이어블 캐릭터 복제
                        print(pc1_Doll)
                        pc2_Doll = doll_list[sys_cursor_h2].clone() # 플레이어블 캐릭터 복제
                        print(pc1_Doll)
                        print("-" * 15  + "인형 선택 완료" + "-" * 15)
                        scn_battleMain() # 전투 화면 씬으로 이동
                        # 승리 화면으로 이동
                        loop_st1 = False
                if event.key == pygame.K_x:  # X 키로 취소
                    loop_st1 = False
        pygame.display.flip()

def scn_battleMain(): # 메인 전투 화면 씬 스테이지 ID 2
    # 글로벌 변수 선언 및 초기화
    global pc1_Doll # 플레이어1 캐릭터 호출
    global pc2_Doll # 플레이어2 캐릭터 호출
    global SYS_TURN_COUNT # 턴 호출
    global SYS_TURN_PLAYER # 행동 플레이어 호출
    global SYS_BATTLE_LOG # 전투 로그 호출
    SYS_TURN_COUNT = 0 # 턴 초기화
    SYS_TURN_PLAYER = 0 # 현재 행동 플레이어 초기화
    SYS_BATTLE_LOG.clear() # 전투 로그 초기화
    # 전투 화면 루프 변수
    loop_st2 = True
    # 커서 변수 선언
    sys_cursor_h = 0
    # 터미널 출력부
    print("-" * 15  + "전투 시작!" + "-" * 15)
    print(pc1_Doll)
    print(pc2_Doll)
    # 선제 턴 결정
    nan_turn = rd.random() * 100 # 랜덤 선제 턴 뽑기
    if 50 <= nan_turn:
        SYS_TURN_PLAYER = 1 # 플레이어1 선제 공격
        SYS_BATTLE_LOG.append(FONT_24.render(f"{pc1_Doll.name}의 선제 공격({int(nan_turn)})", True, COL_RED))
    else:
        SYS_TURN_PLAYER = 2 # 플레이어2 선제공격
        SYS_BATTLE_LOG.append(FONT_24.render(f"{pc2_Doll.name}의 선제 공격({int(nan_turn)})", True, COL_BLUE))
    
    ### 시작 턴 수치 증가 ###
    SYS_TURN_COUNT += 1 # 초기화 된 턴으로부터 1턴 개시
    #########################
    
    # 전투 메인 화면 루프 시작
    while loop_st2:
        WIN_SCREEN.fill(COL_BLACK) # 배경 화면 검정색으로 지정
        # 전투 시스템 메뉴 출력부
        sys_textDisplay(TXT_BATTLE_ACT01, (WIN_WIDTH // 6) * 1 - 50 , int(WIN_HEIGHT * 0.95)) # 기본 공격
        sys_textDisplay(TXT_BATTLE_ACT02, (WIN_WIDTH // 6) * 2 - 25, int(WIN_HEIGHT * 0.95)) # 충전
        sys_textDisplay(TXT_BATTLE_ACT03, (WIN_WIDTH // 6) * 3, int(WIN_HEIGHT * 0.95)) # 캐릭터 고유 스킬
        sys_textDisplay(TXT_BATTLE_ACT04, (WIN_WIDTH // 6) * 4 + 25, int(WIN_HEIGHT * 0.95)) # 궁극 스킬
        sys_textDisplay(TXT_BATTLE_ACT05, (WIN_WIDTH // 6) * 5 + 50, int(WIN_HEIGHT * 0.95)) # 그냥 턴 종료

        # 커서 이동
        if sys_cursor_h == 0:
            sys_textDisplay(TXT_MENU_SELECT, (WIN_WIDTH // 6) * 1 - 140, int(WIN_HEIGHT * 0.945)) # 기본 공격
        elif sys_cursor_h == 1:
            sys_textDisplay(TXT_MENU_SELECT, (WIN_WIDTH // 6) * 2 - 115, int(WIN_HEIGHT * 0.945)) # 충전
        elif sys_cursor_h == 2:
            sys_textDisplay(TXT_MENU_SELECT, (WIN_WIDTH // 6) * 3 - 90, int(WIN_HEIGHT * 0.945)) # 캐릭터 고유 스킬
        elif sys_cursor_h == 3:
            sys_textDisplay(TXT_MENU_SELECT, (WIN_WIDTH // 6) * 4 - 65, int(WIN_HEIGHT * 0.945)) # 궁극 스킬
        elif sys_cursor_h == 4:
            sys_textDisplay(TXT_MENU_SELECT, (WIN_WIDTH // 6) * 5 - 40, int(WIN_HEIGHT * 0.945)) # 그냥 턴 종료
        
        # 전투 로그 출력부
        line_space = -10 # 출력 행
        for log in SYS_BATTLE_LOG:
            sys_textDisplay(log, WIN_WIDTH // 2, (WIN_HEIGHT // 3) * 2 + line_space) # 로그 출력
            line_space += 35 # 출력 행간
        if len(SYS_BATTLE_LOG) > 6: # 로그 행 제한
            SYS_BATTLE_LOG.pop(0) # 팝으로 오래된 행 제거

        # 현재 턴 소유자 출력
        txt_temp = FONT_24.render(f"{SYS_TURN_COUNT}턴, 플레이어{SYS_TURN_PLAYER}의 차례", True, COL_YELLOW) # 현재 턴, 소유자 정보
        sys_textDisplay(txt_temp, WIN_WIDTH // 2, int(WIN_HEIGHT * 0.03)) # 최상단에 출력
        txt_temp = FONT_24.render(f"▼ 현재 턴 ▼", True, COL_YELLOW) # 현재 소유자 커서
        if SYS_TURN_PLAYER == 1:
            sys_textDisplay(txt_temp, WIN_WIDTH // 4 * 1, 200) # 플레이어1의 소유 커서 표시
        elif SYS_TURN_PLAYER == 2:
            sys_textDisplay(txt_temp, WIN_WIDTH // 4 * 3, 200) # 플레이어2의 소유 커서 표시

        # 스탯 디스플레이 함수 호출
        sys_statDisplay(pc1_Doll, 1, COL_RED)
        sys_statDisplay(pc2_Doll, 2, COL_BLUE)

        # 승패 결착이 날 경우 메시지 출력(승자 표기, 계속 하려면 ZX키를 누르세요 등)
        if (not pc1_Doll.sys_aliveCheck() or not pc2_Doll.sys_aliveCheck()):
            if pc1_Doll.sys_aliveCheck():
                txt_temp = FONT_40.render(f"P1 - {pc1_Doll.name} 승리!", True, COL_RED) # 플레이어1 승리
            if pc2_Doll.sys_aliveCheck():
                txt_temp = FONT_40.render(f"P2 - {pc2_Doll.name} 승리!", True, COL_BLUE) # 플레이어2 승리 
            sys_textDisplay(txt_temp, WIN_WIDTH//2, WIN_HEIGHT//5)

        # 사용자 입력 이벤트 처리
        for event in pygame.event.get():
                if event.type == pygame.QUIT: # 게임 종료
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if (pc1_Doll.sys_aliveCheck() and pc2_Doll.sys_aliveCheck()):
                        if event.key == pygame.K_RIGHT: # 행동 선택 이동
                            sys_cursor_h = (sys_cursor_h + 1) % 5
                        if event.key == pygame.K_LEFT: # 행동 선택 이동
                            sys_cursor_h = (sys_cursor_h - 1) % 5
                        if event.key == pygame.K_z: # 행동 선택 결과
                            if SYS_TURN_PLAYER == 1: #플레이어1의 차례일 경우
                                if sys_cursor_h == 0 or sys_cursor_h == 1 or sys_cursor_h == 4: # 연산량이 필요 없을 경우
                                    sys_playerTurn(pc1_Doll, pc2_Doll, sys_cursor_h, COL_RED, SYS_TURN_COUNT)
                                    sys_cursor_h = 0 # 커서 위치 초기화
                                elif sys_cursor_h == 2: # 스킬 사용시 연산량 체크
                                    if pc1_Doll.mp >= pc1_Doll.scost:
                                        sys_playerTurn(pc1_Doll, pc2_Doll, sys_cursor_h, COL_RED, SYS_TURN_COUNT)
                                        sys_cursor_h = 0 # 커서 위치 초기화
                                    else:
                                        SYS_BATTLE_LOG.append(FONT_24.render(f"{pc1_Doll.name}의 스킬을 사용할 연산력이 {pc1_Doll.scost - pc1_Doll.mp} 부족합니다.", True, COL_RED))
                                        sys_cursor_h = 0 # 커서 위치 초기화
                                elif sys_cursor_h == 3: # 스킬 사용시 연산량 체크
                                    if pc1_Doll.mp >= pc1_Doll.ucost:
                                        sys_playerTurn(pc1_Doll, pc2_Doll, sys_cursor_h, COL_RED, SYS_TURN_COUNT)
                                        sys_cursor_h = 0 # 커서 위치 초기화
                                    else:
                                        SYS_BATTLE_LOG.append(FONT_24.render(f"{pc1_Doll.name}의 궁극기를 사용할 연산력이 {pc1_Doll.ucost - pc1_Doll.mp} 부족합니다.", True, COL_RED))
                                        sys_cursor_h = 0 # 커서 위치 초기화
                            elif SYS_TURN_PLAYER == 2: #플레이어2의 차례일 경우
                                if sys_cursor_h == 0 or sys_cursor_h == 1 or sys_cursor_h == 4: # 연산량이 필요 없을 경우
                                    sys_playerTurn(pc2_Doll, pc1_Doll, sys_cursor_h, COL_BLUE, SYS_TURN_COUNT)
                                    sys_cursor_h = 0 # 커서 위치 초기화
                                elif sys_cursor_h == 2: # 스킬 사용시 연산량 체크
                                    if pc2_Doll.mp >= pc2_Doll.scost:
                                        sys_playerTurn(pc2_Doll, pc1_Doll, sys_cursor_h, COL_BLUE, SYS_TURN_COUNT)
                                        sys_cursor_h = 0 # 커서 위치 초기화
                                    else:
                                        SYS_BATTLE_LOG.append(FONT_24.render(f"{pc2_Doll.name}의 스킬을 사용할 연산력이 {pc2_Doll.scost - pc2_Doll.mp} 부족합니다.", True, COL_BLUE))
                                        sys_cursor_h = 0 # 커서 위치 초기화
                                elif sys_cursor_h == 3: # 스킬 사용시 연산량 체크
                                    if pc2_Doll.mp >= pc2_Doll.ucost:
                                        sys_playerTurn(pc2_Doll, pc1_Doll, sys_cursor_h, COL_BLUE, SYS_TURN_COUNT)
                                        sys_cursor_h = 0 # 커서 위치 초기화
                                    else:
                                        SYS_BATTLE_LOG.append(FONT_24.render(f"{pc2_Doll.name}의 궁극기를 사용할 연산력이 {pc2_Doll.ucost - pc2_Doll.mp} 부족합니다.", True, COL_BLUE))
                                        sys_cursor_h = 0 # 커서 위치 초기화
                    else: # 키 입력으로 루프 탈출
                        if event.key == pygame.K_z:
                            loop_st2 = False
                        if event.key == pygame.K_x:
                            loop_st2 = False
        pygame.display.flip()
# endregion
####################################################################################################

########################################메인 함수###################################################
def main():
    scn_titleMenu()
    # pygame 종료
    pygame.quit()
    sys.exit()
main()
####################################################################################################