import random as rd
import copy

class PlayerDoll:
    def __init__(self, _name, _hp, _mp, _atk, _dfs, _crt, _crd, _avd, _cool): #스탯 초기화
        self.name = _name #인형의 이름
        self.maxhp = _hp #인형의 최대 체력
        self.hp = _hp #인형의 현재 체력
        self.mp = _mp #인형의 연산력
        self.atk = _atk #공격력
        self.dfs = _dfs #방어력
        self.crt = _crt #치명률
        self.defaultcrt = _crt #원래 치명률 값
        self.crd = _crd #치명피해
        self.avd = _avd #회피율
        self.cool = _cool #스킬 쿨타임
        self.defaultcool = _cool #초기 쿨타임 값
        self.buffcheck = False #버프 상태 체크
        self.buffduration = 0 #버프 지속 시간

    def attack(self, other, color): #일반 공격 메소드(본인, 공격대상, 플레이어 컬러)
        #일반 공격 관련 난수 결정
        crtnan = rd.random() * 100 #치명률
        avdnan = rd.random() * 100 #회피율
        damage = int(self.atk * (0.9 + rd.random() * 0.2)) #공격력의 90%~110% 사이의 랜덤 데미지
        print("\033[32m" + "-" * 15 + " 일반 공격 결과 " + "-" * 15 + "\033[0m")
        if avdnan < other.avd: #회피 판정
            print(f"{color}{self.name}의 공격은 빗나갔다...\033[0m")
            print("\033[32m" + "-" * 15 + " 현재 인형 스탯 " + "-" * 15 + "\033[0m")
            return
        if crtnan < self.crt: #치명타 판정
            damage = int(damage * (1 + self.crd/100)) #치명타 피해 계산(치명타는 방어력을 관통)
            if damage < 0: #최소 데미지 보정
                damage = 1
            other.hp -= damage #데미지만큼 공격대상 체력 차감
            print(f"{color}크리티컬 히트! {self.name}은 {other.name}에게 {damage}데미지를 입혔다!\033[0m") #데미지 출력
        else : #평타 판정
            damage -= other.dfs #피해 계산
            if damage < 0: #최소 데미지 보정
                damage = 1
            other.hp -= damage #데미지만큼 공격대상 체력 차감
            print(f"{color}{self.name}은 {other.name}에게 {damage}데미지를 입혔다.\033[0m") #데미지 출력
        if self.isalive() and other.isalive(): #생존여부 체크
            print("\033[32m" + "-" * 15 + " 현재 인형 스탯 " + "-" * 15 + "\033[0m")
            return
        
    def passiveSkill(self):
        if self.name == "솔":
            self.hp += 10  # 예: 매 턴 체력 회복
            print(f"{self.name}의 패시브 스킬 발동! 체력이 10 회복되었다.")
        elif self.name == "크로크":
            self.dfs += 2  # 예: 방어력 증가
            print(f"{self.name}의 패시브 스킬 발동! 방어력이 2 증가했다.")
        elif self.name == "보름":
            self.crd += 2  # 예: 방어력 증가
            print(f"{self.name}의 패시브 스킬 발동! 치명 데미지가 2 증가했다.")
        # 다른 캐릭터에 대한 패시브 스킬 구현
        pass
    def activeSkill(self, other, color):
        print("\033[32m" + "-" * 15 + " 스킬 사용 결과 " + "-" * 15 + "\033[0m")
        if self.cool == 0:
            if self.name == "솔":
                damage = self.atk * 2  # 예: 공격력의 2배 데미지
                other.hp -= damage
                print(f"{color}{self.name}의 사!자!열!화!참! {other.name}에게 {damage} 데미지를 입혔다.\033[0m")
            elif self.name == "크로크":
                self.hp += 200  # 예: 체력 회복
                print(f"{color}{self.name}의 이지스의 방패 발동. 보호막을 200 획득했다.\033[0m")
            elif self.name == "보름":
                print(f"{color}{self.name}이 추적의 룬을 사용. 다음 2턴간 치명타가 상승한다.\033[0m")
                self.crt += 50  # 치명률 30 증가
                self.buffcheck = True  # 버프 활성화
                self.buffduration = 3   # 버프 지속 시간 3턴
            self.cool = self.defaultcool  # 스킬 사용 후 쿨타임 초기화
            # 이하 다른 캐릭터에 대한 액티브 스킬 구현
        else:
            print("스킬을 사용할 수 없습니다. 쿨타임이 남아 있습니다.")
        if self.isalive() and other.isalive(): #생존여부 체크
            print("\033[32m" + "-" * 15 + " 현재 인형 스탯 " + "-" * 15 + "\033[0m")
            return

    def turnEnd(self):
        if self.buffcheck:
            self.buffduration -= 1  # 버프 지속 시간 감소
            if self.buffduration <= 0:  # 버프 지속 시간이 끝나면
                self.crt = self.defaultcrt  # 치명률 원래대로 복구
                self.buffcheck = False
                print(f"\033[0m{self.name}의 치명률 버프가 해제되었습니다.\033[0m")
        # 쿨타임 감소 처리
        if self.cool > 0:
            self.cool -= 1

    def isalive(self): #생존여부 체크 메소드
        return self.hp > 0
    def __str__(self): #캐릭터 스탯 반환
        return (f"{self.name} HP:{self.hp} 스킬 쿨타임: {self.cool}\n"
                f"공격력 {self.atk}, 방어력 {self.dfs}, 치명률 {self.crt}%, 회피율 {self.avd}%")
    def statdisplay(self): #스탯 출력
        print("\033[32m" + "-" * 15 + " 현재 인형 스탯 " + "-" * 15 + "\033[0m")
    def reset(self):#캐릭터의 체력을 초기 상태로 복원
        self.hp = self.maxhp
    def clone(self): #캐릭터 선택시 복제
        return copy.deepcopy(self)

def playerTurn(player, opponent, color): #플레이어 턴의 행동 처리
    player.passiveSkill()
    while True:
        print(f"{color}{player.name}의 턴입니다. 행동을 선택하세요. : \033[0m")
        print("1. 일반 공격")
        print("2. 스킬")
        #print("3. 아이템")
        choice = input("행동 선택 : ")
        if choice == "1": #일반 공격 선택
            player.attack(opponent, color) #일반 공격 실행
            break
        #스킬 실행
        elif choice == "2":  # 스킬 선택
            if player.cool == 0:  # 쿨타임이 0이면 스킬 발동 가능
                player.activeSkill(opponent, color)
                break
            else:
                print("스킬을 사용할 수 없습니다. 쿨타임이 남아 있습니다.")
                # 쿨타임이 남아있으면 메뉴를 다시 출력
        #아이템 사용
        else:
            print("잘못된 입력입니다.") #잘못된 입력 예외 처리
    player.turnEnd()

def displayStats(player01, player02):
    print("\033[31m", end="")
    print(player01)  # 플레이어 1의 스탯 출력
    print("\033[0m", end="")
    print("\033[34m", end="")
    print(player02)  # 플레이어 2의 스탯 출력
    print("\033[0m", end="")
    print("\033[32m" + "-" * 50 + "\033[0m")

def battleStart(player01, player02):
    print("\033[32m" + "=" * 50 + "\033[0m")
    print("\033[33m전투 시작!\033[0m")
    print("\033[32m" + "-" * 50 + "\033[0m")
    
    # 초기 스탯 출력
    displayStats(player01, player02)
    
    # 전투 루프
    while player01.isalive() and player02.isalive():
        playerTurn(player01, player02, "\033[31m")  # 플레이어 1의 턴
        
        if not player02.isalive():
            print("\033[32m" + "-" * 50 + "\033[0m")
            print(f"\033[31m{player01.name}의 승리!\033[0m")
            break
        
        displayStats(player01, player02)  # 턴 후 스탯 출력
        
        playerTurn(player02, player01, "\033[34m")  # 플레이어 2의 턴
        
        if not player01.isalive():
            print("\033[32m" + "-" * 50 + "\033[0m")
            print(f"\033[34m{player02.name}의 승리!\033[0m")
            break
        
        displayStats(player01, player02)  # 턴 후 스탯 출력

def selectDoll(): #인형 선택 함수
    dollList = [
        wr01_Sol,
        gd01_Croque,
        sn01_Clukay,
        sp01_Luna,
        md01_Persica,
        etc01_memeko
    ]
    #dollList.sort()
    print("인형을 선택하세요 : ")
    for i, doll in enumerate(dollList, 1): #인형 리스트 출력
        print(f"{i}. {doll.name}")
    while True:
        choice = input("인형 선택 : ")
        if choice.isdigit() and 1 <= int(choice) <= len(dollList):
            return dollList[int(choice) - 1].clone() #선택한 인형 반환
        else:
            print("잘못된 입력입니다.") #잘못된 입력 예외 처리


def print_with_color(message, color_code):#색상 출력 관련 함수
    print(f"{color_code}{message}\033[0m")

def main(): #메인 메뉴 함수
    while True:
        print("\033[32m" + "=" * 50 + "\033[0m")
        print("\033[33m 뉴럴 클라우드 정실 대전 240816beta \033[0m")
        print("")
        print("")
        print("1. 정실 대전 시작")
        print("")
        print("2. 게임 종료")
        print("")
        print("")
        print("\033[32m" + "=" * 50 + "\033[0m")
        
        choice = input("메뉴 선택: ")
        if choice == "1":
            print("\033[32m" + "=" * 50 + "\033[0m")
            print("\033[31m", end="") #플레이어01 = 빨간색
            print("플레이어 1의 인형 선택:")
            print("\033[0m", end="")
            player1 = selectDoll() #플레이어01 캐릭터 선택
            print("\033[31m", end="")
            print(f"플레이어 1이 {player1.name}을(를) 선택했습니다.")
            print("\033[0m", end="")
            print("\033[34m", end="") #플레이어02 = 파란색
            print("\033[32m" + "=" * 50 + "\033[0m")
            print("플레이어 2의 캐릭터 선택:")
            print("\033[0m", end="")
            player2 = selectDoll() #플레이어02 캐릭터 선택
            print("\033[34m", end="") #플레이어02 = 파란색
            print(f"플레이어 2가 {player2.name}을(를) 선택했습니다.")
            print("\033[0m", end="")
            
            battleStart(player1, player2) #정실 대전 시작
        elif choice == "2": #게임 종료
            print("게임을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다.") #잘못된 입력 예외 처리

#인형 리스트             (인형 이름, 체력     , 연산력 , 공격력  , 방어력 , 치명률 , 치명피해, 회피율, 스킬 쿨타임)
wr01_Sol     = PlayerDoll("솔"      , _hp=800 , _mp=300 , _atk=100, _dfs=20, _crt=20, _crd=50 , _avd=5 , _cool=7)
gd01_Croque  = PlayerDoll("크로크"  , _hp=1000, _mp=300 , _atk=70 , _dfs=40, _crt=15, _crd=50 , _avd=10, _cool=6)
sn01_Clukay  = PlayerDoll("클루카이", _hp=750 , _mp=400 , _atk=90 , _dfs=10, _crt=30, _crd=100, _avd=5 , _cool=5)
sp01_Luna    = PlayerDoll("보름"    , _hp=700 , _mp=500 , _atk=80 , _dfs=15, _crt=50, _crd=80 , _avd=25, _cool=5)
sp02_Sakuya  = PlayerDoll("사쿠야"  , _hp=700 , _mp=500 , _atk=90 , _dfs=20, _crt=30, _crd=50 , _avd=20, _cool=5)
md01_Persica = PlayerDoll("페르시카", _hp=600 , _mp=700 , _atk=70 , _dfs=10, _crt=10, _crd=100, _avd=10, _cool=5)
etc01_memeko = PlayerDoll("메메코"  , _hp=3000, _mp=1000, _atk=10 , _dfs=70, _crt=1 , _crd=999, _avd=1 , _cool=999)

#게임 시작
main()
