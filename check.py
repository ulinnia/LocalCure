# 色彩心連心配對追蹤程式

def initialize_participants():
    """
    初始化參與者列表和每位參與者的可選配對對象列表。
    """
    participants = []
    print("請輸入所有參與者的姓名，輸入完成後輸入 'done':")
    while True:
        name = input("參與者姓名: ").strip()
        if name.lower() == 'done':
            break
        if not name:
            print("姓名不能為空，請重新輸入。")
            continue
        if name in participants:
            print("該姓名已存在，請輸入另一個姓名。")
        else:
            participants.append(name)
    num_of_participants = len(participants)
    if num_of_participants < 2:
        print("參與者人數不足，遊戲無法開始。")
        exit()
    
    # 為每位參與者生成可選配對對象列表
    pairings = {participant: set(participants) - {participant} for participant in participants}
    
    return participants, pairings, num_of_participants

def display_remaining_pairings(pairings):
    """
    顯示每位參與者剩餘的可選配對對象。
    """
    print("\n目前每位參與者的可選配對對象如下：")
    for participant, options in pairings.items():
        print(f"{participant}: {', '.join(options) if options else '無'}")
    print("\n")

def add_participant(participants, pairings):
    """
    手動添加一位參與者。
    """
    name = input("請輸入要添加的參與者姓名: ").strip()
    if not name:
        print("姓名不能為空。")
        return
    if name in participants:
        print("該姓名已存在。")
        return
    participants.append(name)
    # 更新 pairings
    for p in pairings:
        pairings[p].add(name)
    pairings[name] = set(participants) - {name}
    print(f"已成功添加參與者: {name}")

def delete_participant(participants, pairings):
    """
    手動刪除一位參與者。
    """
    name = input("請輸入要刪除的參與者姓名: ").strip()
    if name not in participants:
        print("該參與者不在名單中。")
        return
    participants.remove(name)
    pairings.pop(name)
    for p in pairings:
        pairings[p].discard(name)
    print(f"已成功刪除參與者: {name}")
    # 檢查並移除已配對的參與者
    to_remove = [p for p in participants if not pairings[p]]
    if to_remove:
        print(f"以下參與者已無可選配對對象並將被移除：{', '.join(to_remove)}")
        for p in to_remove:
            participants.remove(p)
            pairings.pop(p)
            for other in pairings:
                pairings[other].discard(p)
            # 新增提示訊息
            print(f"{p} 可能配對皆已試完。")

def display_menu():
    """
    顯示操作選單。
    """
    print("請選擇操作:")
    print("1. 添加參與者")
    print("2. 刪除參與者")
    print("3. 進行配對")
    print("4. 顯示剩餘配對")
    print("5. 退出遊戲")

def main():
    participants, pairings, num_of_participants = initialize_participants()
    
    while True:
        display_menu()
        choice = input("輸入選項號碼: ").strip()
        
        if choice == '1':
            add_participant(participants, pairings)
        elif choice == '2':
            delete_participant(participants, pairings)
        elif choice == '3':
            if len(participants) < 2:
                print("參與者人數不足，無法進行配對。")
                continue
            display_remaining_pairings(pairings)
            
            # 輸入選擇者和被選擇者
            selector = input("輪到選擇配對的參與者姓名 (輸入 'cancel' 返回選單): ").strip()
            if selector.lower() == 'cancel':
                continue
            if selector not in participants:
                print("選擇者不在參與者列表中，請重新輸入。")
                continue
            
            # 確認選擇者是否有可選配對對象
            if not pairings[selector]:
                print(f"{selector} 已無可選配對對象，請選擇其他參與者。")
                continue
            
            selected = input(f"請輸入 {selector} 想要配對的對象姓名 (輸入 'cancel' 返回選單): ").strip()
            if selected.lower() == 'cancel':
                continue
            if selected not in participants:
                print("被選擇者不在參與者列表中，請重新輸入。")
                continue
            if selected not in pairings[selector]:
                print(f"{selected} 不是 {selector} 的可選配對對象，請重新選擇。")
                continue
            
            # 輸入配對結果
            result = input("配對是否成功? (Y/N): ").strip().upper()
            if result not in ['Y', 'N']:
                print("無效的輸入，請輸入 'Y' 或 'N'。")
                continue
            
            if result == 'Y':
                print(f"{selector} 和 {selected} 配對成功！")
                # 將兩位參與者從總參與者列表中移除
                participants.remove(selector)
                participants.remove(selected)
                # 從pairings中移除這兩位
                pairings.pop(selector)
                pairings.pop(selected)
                for p in pairings:
                    pairings[p].discard(selector)
                    pairings[p].discard(selected)
            else:
                print(f"{selector} 和 {selected} 配對失敗。")
                # 將被選擇者從選擇者的可選配對列表中移除
                pairings[selector].remove(selected)
                # 將選擇者從被選擇者的可選配對列表中移除
                pairings[selected].remove(selector)
            
            # 檢查是否有參與者無可選配對對象
            to_remove = [p for p in participants if not pairings[p]]
            if to_remove:
                for p in to_remove:
                    print(f"{p} 可能配對皆已試完。")
                    participants.remove(p)
                    pairings.pop(p)
                    for other in pairings:
                        pairings[other].discard(p)
        
        elif choice == '4':
            display_remaining_pairings(pairings)
        elif choice == '5':
            print("\n遊戲結束！")
            if len(participants) == 1:
                print(f"最後一位未配對的參與者是：{participants[0]}")
            elif len(participants) > 1:
                print("遊戲結束，以下參與者未能配對：")
                print(", ".join(participants))
            else:
                print("所有參與者已完成配對。")
            break
        else:
            print("無效的選項，請重新選擇。")
    
    print("謝謝遊玩！")

if __name__ == "__main__":
    main()
