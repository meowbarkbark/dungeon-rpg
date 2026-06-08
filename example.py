# -*- coding: utf-8 -*-
import random
import time

def slow_print(text, delay=0.03):
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)
    print()

def show_status(hp, max_hp, atk, gold, floor):
    bar = '█' * (hp * 10 // max_hp) + '░' * (10 - hp * 10 // max_hp)
    print(f"\n  HP [{bar}] {hp}/{max_hp}  공격력: {atk}  골드: {gold}G  층수: B{floor}F")

MONSTERS = [
    {"name": "슬라임",      "hp": 10, "atk": 3,  "gold": 5,  "exp": "약함"},
    {"name": "고블린",      "hp": 18, "atk": 6,  "gold": 12, "exp": "보통"},
    {"name": "해골 전사",   "hp": 25, "atk": 9,  "gold": 20, "exp": "강함"},
    {"name": "독거미",      "hp": 20, "atk": 12, "gold": 18, "exp": "강함"},
    {"name": "어둠의 마법사","hp": 30, "atk": 15, "gold": 35, "exp": "매우 강함"},
]
BOSS = {"name": "💀 던전 보스 '심연의 군주'", "hp": 80, "atk": 20, "gold": 100}

ITEMS = [
    {"name": "회복 포션",   "type": "heal",   "value": 20, "price": 15},
    {"name": "강화 포션",   "type": "attack", "value": 5,  "price": 25},
    {"name": "녹슨 검",     "type": "weapon", "value": 8,  "price": 20},
    {"name": "강철 검",     "type": "weapon", "value": 15, "price": 40},
]

def battle(player, monster):
    slow_print(f"\n  ⚔️  {monster['name']} 등장!")
    m_hp = monster["hp"]

    while True:
        print(f"\n  [{monster['name']}] HP: {m_hp}")
        print("  [1] 공격  [2] 강공격(50% 확률, 2배 데미지)  [3] 도망")
        choice = input("  선택 >> ").strip()

        if choice == "1":
            dmg = player["atk"] + random.randint(-2, 2)
            m_hp -= dmg
            slow_print(f"  → {dmg} 데미지!")
        elif choice == "2":
            if random.random() < 0.5:
                dmg = player["atk"] * 2
                m_hp -= dmg
                slow_print(f"  → 크리티컬! {dmg} 데미지!")
            else:
                slow_print("  → 빗나갔다...")
        elif choice == "3":
            if random.random() < 0.4:
                slow_print("  → 도망쳤다!")
                return "escape"
            else:
                slow_print("  → 도망 실패!")
        else:
            continue

        if m_hp <= 0:
            slow_print(f"  ✅ {monster['name']} 처치! +{monster['gold']}G 획득!")
            player["gold"] += monster["gold"]
            return "win"

        # 몬스터 반격
        m_dmg = monster["atk"] + random.randint(-2, 2)
        # 10% 확률로 공격 빗나감
        if random.random() < 0.1:
            slow_print(f"  ← {monster['name']}의 공격이 빗나갔다!")
        else:
            player["hp"] -= m_dmg
            slow_print(f"  ← {monster['name']}의 반격! -{m_dmg} HP")

        if player["hp"] <= 0:
            return "dead"

def shop(player):
    slow_print("\n  🏪 상인: 어서오세요~ 뭘 드릴까요?")
    while True:
        print(f"\n  보유 골드: {player['gold']}G")
        for i, item in enumerate(ITEMS, 1):
            print(f"  [{i}] {item['name']} - {item['price']}G")
        print("  [0] 나가기")
        choice = input("  선택 >> ").strip()
        if choice == "0":
            break
        if not choice.isdigit() or not (1 <= int(choice) <= len(ITEMS)):
            continue
        item = ITEMS[int(choice) - 1]
        if player["gold"] < item["price"]:
            slow_print("  골드가 부족합니다!")
            continue
        player["gold"] -= item["price"]
        if item["type"] == "heal":
            player["hp"] = min(player["max_hp"], player["hp"] + item["value"])
            slow_print(f"  💊 HP +{item['value']} 회복! (현재 {player['hp']})")
        elif item["type"] == "attack":
            player["atk"] += item["value"]
            slow_print(f"  ⚡ 공격력 +{item['value']}! (현재 {player['atk']})")
        elif item["type"] == "weapon":
            player["atk"] += item["value"]
            slow_print(f"  🗡️  {item['name']} 장착! 공격력 +{item['value']}!")

def dungeon():
    print("\n" + "=" * 45)
    slow_print("   ⚔️   던전 탈출 RPG   ⚔️")
    print("=" * 45)
    slow_print("  어둠의 던전에 갇혔다. 보스를 쓰러트리고")
    slow_print("  5층을 탈출하라!\n")

    name = input("  캐릭터 이름: ").strip() or "용사"
    player = {"name": name, "hp": 50, "max_hp": 50, "atk": 10, "gold": 10, "floor": 1}
    slow_print(f"\n  {name}의 모험이 시작된다...\n")

    while player["floor"] <= 5:
        show_status(player["hp"], player["max_hp"], player["atk"], player["gold"], player["floor"])

        # 5층은 보스
        if player["floor"] == 5:
            slow_print("\n  으르렁... 보스 방에 도달했다!")
            input("  [Enter] 보스와 대결!")
            result = battle(player, BOSS.copy())
            if result == "win":
                slow_print(f"\n  🎉 {player['name']}은 던전을 탈출했다!")
                slow_print(f"  최종 공격력: {player['atk']}  남은 HP: {player['hp']}/{player['max_hp']}  골드: {player['gold']}G")
                print("=" * 45)
            else:
                slow_print(f"\n  💀 {player['name']}은 쓰러졌다... GAME OVER")
                print("=" * 45)
            return

        # 일반 층
        print(f"\n  B{player['floor']}F — 무엇을 할까?")
        print("  [1] 앞으로 이동 (몬스터 조우)")
        print("  [2] 상점 방문  [3] HP 회복 (20G)")
        choice = input("  선택 >> ").strip()

        if choice == "1":
            monster = random.choice(MONSTERS[:player["floor"] + 1]).copy()
            result = battle(player, monster)
            if result == "dead":
                slow_print(f"\n  💀 {player['name']}은 쓰러졌다... GAME OVER")
                print("=" * 45)
                return
            elif result == "win":
                player["floor"] += 1
                slow_print(f"  계단을 발견했다. B{player['floor']}F로 이동한다.")

        elif choice == "2":
            shop(player)

        elif choice == "3":
            if player["gold"] >= 20:
                player["gold"] -= 20
                heal = 15
                player["hp"] = min(player["max_hp"], player["hp"] + heal)
                slow_print(f"  🛌 잠시 휴식... HP +{heal} (현재 {player['hp']})")
            else:
                slow_print("  골드가 부족합니다!")

        if player["hp"] <= 0:
            slow_print(f"\n  💀 {player['name']}은 쓰러졌다... GAME OVER")
            print("=" * 45)
            return

if __name__ == "__main__":
    while True:
        dungeon()
        again = input("\n  다시 플레이할까요? (y/n) >> ").strip().lower()
        if again != 'y':
            slow_print("  게임을 종료합니다. 또 만나요! 👋")
            break
