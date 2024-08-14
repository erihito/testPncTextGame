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
        self.crd = _crd #치명피해
        self.avd = _avd #회피율
        self.cool = _cool #스킬 쿨타임
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
    def skill(self):
        #여기 if와 self.name으로 캐릭터별 스킬 구현
        print("test")
    def isalive(self): #생존여부 체크 메소드
        return self.hp > 0
    def __str__(self): #캐릭터 스탯 반환
        return (f"{self.name} HP:{self.hp}\n"
                f"공격력 {self.atk}, 방어력 {self.dfs}, 치명률 {self.crt}%, 회피율 {self.avd}%")
    def statdisplay(self): #스탯 출력
        print("\033[32m" + "-" * 15 + " 현재 인형 스탯 " + "-" * 15 + "\033[0m")
    def reset(self):#캐릭터의 체력을 초기 상태로 복원
        self.hp = self.maxhp
    def clone(self): #캐릭터 선택시 복제
        return copy.deepcopy(self)

def playerTurn(player, opponent, color): #플레이어 턴의 행동 처리
    while True:
        print(f"{color}{player.name}의 턴입니다. 행동을 선택하세요. : \033[0m")
        print("1. 일반 공격")
        #print("2. 스킬")
        #print("3. 아이템")
        choice = input("행동 선택 : ")
        if choice == "1": #일반 공격 선택
            player.attack(opponent, color) #일반 공격 실행
            break
        #스킬 실행
        #아이템 사용
        else:
            print("잘못된 입력입니다.") #잘못된 입력 예외 처리

def battleStart(player01, player02): #전투 시작
    print("\033[32m" + "=" * 50 + "\033[0m")
    print("\033[33m전투 시작!\033[0m")
    print("\033[32m" + "-" * 50 + "\033[0m")
    print("\033[31m", end="") #플레이어01 = 빨간색
    print(player01) #플레이어 스탯 출력
    print("\033[0m", end="")
    print("\033[34m", end="") #플레이어02 = 파란색
    print(player02) #플레이어 스탯 출력
    print("\033[0m", end="")
    print("\033[32m" + "-" * 50 + "\033[0m")
    #플레이어 사망 전까지 전투 루프 진행
    while player01.isalive() and player02.isalive():
        playerTurn(player01, player02, "\033[31m") #플레이어01의 턴
        if not player02.isalive():
            print("\033[32m" + "-" * 50 + "\033[0m")
            print(f"\033[31m{player01.name}의 승리!\033[0m")
            print("\033[32m" + "=" * 50 + "\033[0m")
            break
        print("\033[31m", end="")
        print(player01) #플레이어 스탯 출력
        print("\033[0m", end="")
        print("\033[34m", end="")
        print(player02) #플레이어 스탯 출력
        print("\033[0m", end="")
        print("\033[32m" + "-" * 50 + "\033[0m")
        playerTurn(player02, player01, "\033[34m") #플레이어02의 턴
        if not player01.isalive():
            print("\033[32m" + "-" * 50 + "\033[0m")
            print(f"\033[34m{player02.name}의 승리!\033[0m")
            print("\033[32m" + "=" * 50 + "\033[0m")
            break
        print("\033[31m", end="")
        print(player01) #플레이어 스탯 출력
        print("\033[0m", end="")
        print("\033[34m", end="")
        print(player02) #플레이어 스탯 출력
        print("\033[0m", end="")
        print("\033[32m" + "-" * 50 + "\033[0m")

def selectDoll(): #인형 선택 함수
    dollList = [
        wr01_Sol,
        gd01_Croque,
        sn01_Clukay,
        sp01_Luna,
        md01_Persica
    ]
    print("인형을 선택하세요 : ")
    for i, doll in enumerate(dollList, 1): #인형 리스트 출력
        print(f"{i}. {doll.name}")
    while True:
        choice = input("인형 선택 : ")
        if choice.isdigit() and 1 <= int(choice) <= len(dollList):
            return dollList[int(choice) - 1].clone() #선택한 인형 반환
        else:
            print("잘못된 입력입니다.") #잘못된 입력 예외 처리

def main(): #메인 메뉴 함수
    while True:
        print("\033[32m" + "=" * 50 + "\033[0m")
        print("\033[33m 뉴럴 클라우드 정실 대전 \033[0m")
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
            print("\033[31m", end="") #플레이어01 = 빨간색
            print("플레이어 1의 인형 선택:")
            print("\033[0m", end="")
            player1 = selectDoll() #플레이어01 캐릭터 선택
            print("\033[31m", end="")
            print(f"플레이어 1이 {player1.name}을(를) 선택했습니다.")
            print("\033[0m", end="")
            print("\033[34m", end="") #플레이어02 = 파란색
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
wr01_Sol     = PlayerDoll("솔"      , _hp=800 , _mp=300, _atk=110, _dfs=20, _crt=20, _crd=50 , _avd=5 , _cool=3)
gd01_Croque  = PlayerDoll("크로크"  , _hp=1000, _mp=300, _atk=85 , _dfs=55, _crt=15, _crd=50 , _avd=10, _cool=3)
sn01_Clukay  = PlayerDoll("클루카이", _hp=750 , _mp=400, _atk=100, _dfs=10, _crt=30, _crd=100, _avd=5 , _cool=3)
sp01_Luna    = PlayerDoll("보름"    , _hp=700 , _mp=500, _atk=90 , _dfs=15, _crt=50, _crd=80 , _avd=25, _cool=3)
md01_Persica = PlayerDoll("페르시카", _hp=600 , _mp=700, _atk=70 , _dfs=10, _crt=10, _crd=100, _avd=10, _cool=3)

#게임 시작
main()
