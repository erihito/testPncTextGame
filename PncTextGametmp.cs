using System;

public class PlayerDoll
{
    public string Name { get; private set; }
    public int MaxHP { get; private set; }
    public int HP { get; set; }
    public int MP { get; private set; }
    public int ATK { get; private set; }
    public int DFS { get; private set; }
    public int CRT { get; private set; }
    public int CRD { get; private set; }
    public int AVD { get; private set; }
    public int Cool { get; set; }
    public int DefaultCool { get; private set; }
    public bool BuffCheck { get; set; }
    public int BuffDuration { get; set; }
    private Random rand = new Random();
    
    public PlayerDoll(string name, int hp, int mp, int atk, int dfs, int crt, int crd, int avd, int cool)
    {
        Name = name;
        MaxHP = hp;
        HP = hp;
        MP = mp;
        ATK = atk;
        DFS = dfs;
        CRT = crt;
        CRD = crd;
        AVD = avd;
        Cool = cool;
        DefaultCool = cool;
        BuffCheck = false;
        BuffDuration = 0;
    }

    public void Attack(PlayerDoll other)
    {
        double crtnan = rand.NextDouble() * 100;
        double avdnan = rand.NextDouble() * 100;
        int damage = (int)(ATK * (0.9 + rand.NextDouble() * 0.2));

        Console.WriteLine("--------------- 일반 공격 결과 ---------------");
        if (avdnan < other.AVD)
        {
            Console.WriteLine($"{Name}의 공격이 빗나갔습니다...");
            return;
        }

        if (crtnan < CRT)
        {
            damage = (int)(damage * (1 + CRD / 100.0));
            if (damage < 0) damage = 1;
            other.HP -= damage;
            Console.WriteLine($"크리티컬 히트! {Name}이 {other.Name}에게 {damage} 데미지를 입혔습니다!");
        }
        else
        {
            damage -= other.DFS;
            if (damage < 0) damage = 1;
            other.HP -= damage;
            Console.WriteLine($"{Name}이 {other.Name}에게 {damage} 데미지를 입혔습니다.");
        }

        if (!IsAlive())
        {
            Console.WriteLine($"{Name}이 쓰러졌습니다.");
        }
        if (!other.IsAlive())
        {
            Console.WriteLine($"{other.Name}이 쓰러졌습니다.");
        }
    }

    public void ActiveSkill(PlayerDoll other)
    {
        Console.WriteLine("--------------- 스킬 사용 결과 ---------------");
        if (Cool == 0)
        {
            switch (Name)
            {
                case "솔":
                    int damage = ATK * 2;
                    other.HP -= damage;
                    Console.WriteLine($"{Name}의 스킬! {other.Name}에게 {damage} 데미지를 입혔습니다!");
                    break;
                case "크로크":
                    HP += 200;
                    Console.WriteLine($"{Name}의 스킬! 체력이 200 회복되었습니다.");
                    break;
                case "보름":
                    CRT += 50;
                    BuffCheck = true;
                    BuffDuration = 3;
                    Console.WriteLine($"{Name}의 스킬! 치명률이 50% 증가했습니다.");
                    break;
            }
            Cool = DefaultCool;
        }
        else
        {
            Console.WriteLine("스킬을 사용할 수 없습니다. 쿨타임이 남아 있습니다.");
        }
    }

    public void TurnEnd()
    {
        if (BuffCheck)
        {
            BuffDuration--;
            if (BuffDuration <= 0)
            {
                CRT -= 50;
                BuffCheck = false;
                Console.WriteLine($"{Name}의 치명률 버프가 종료되었습니다.");
            }
        }

        if (Cool > 0)
        {
            Cool--;
        }
    }

    public bool IsAlive()
    {
        return HP > 0;
    }

    public void DisplayStats()
    {
        Console.WriteLine($"{Name}의 상태 - HP: {HP}/{MaxHP}, 쿨타임: {Cool}");
    }
}
public class Program
{
    static void PlayerTurn(PlayerDoll player, PlayerDoll opponent)
    {
        player.DisplayStats();
        opponent.DisplayStats();
        
        while (true)
        {
            Console.WriteLine($"{player.Name}의 턴입니다. 행동을 선택하세요:");
            Console.WriteLine("1. 일반 공격");
            Console.WriteLine("2. 스킬 사용");

            string choice = Console.ReadLine();
            switch (choice)
            {
                case "1":
                    player.Attack(opponent);
                    return;
                case "2":
                    player.ActiveSkill(opponent);
                    return;
                default:
                    Console.WriteLine("잘못된 선택입니다. 다시 선택하세요.");
                    break;
            }
        }
    }

    static void Main()
    {
        PlayerDoll player1 = new PlayerDoll("솔", 800, 300, 100, 20, 20, 50, 5, 7);
        PlayerDoll player2 = new PlayerDoll("크로크", 1000, 300, 70, 40, 15, 50, 10, 6);

        Console.WriteLine("게임 시작!");

        while (player1.IsAlive() && player2.IsAlive())
        {
            PlayerTurn(player1, player2);
            if (!player2.IsAlive()) break;

            PlayerTurn(player2, player1);
        }

        if (player1.IsAlive())
        {
            Console.WriteLine($"{player1.Name} 승리!");
        }
        else
        {
            Console.WriteLine($"{player2.Name} 승리!");
        }
    }
}
