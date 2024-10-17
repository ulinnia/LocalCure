import tkinter as tk
from tkinter import messagebox, simpledialog

class Participant:
    def __init__(self, name):
        self.name = name
        self.paired = False
        self.paired_with = None  # 記錄配對對象
        self.attempted = set()  # 記錄已經嘗試配對的對象

class PairingGameGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("彩色心連心")
        self.master.geometry("800x600")
        
        # 設定較大的字體
        self.large_font = ("標楷體", 20)
        
        # 初始化遊戲數據
        self.participants = {}
        self.last_paired = []
        
        # 建立GUI組件
        self.create_widgets()
        
    def create_widgets(self):
        # 框架：添加參與者
        add_frame = tk.Frame(self.master)
        add_frame.pack(pady=10)
        
        add_button = tk.Button(add_frame, text="添加參與者", command=self.add_participant, font=self.large_font)
        add_button.pack(side=tk.LEFT, padx=5)
        
        delete_button = tk.Button(add_frame, text="刪除參與者", command=self.delete_participant, font=self.large_font)
        delete_button.pack(side=tk.LEFT, padx=5)
        
        # 框架：顯示參與者列表
        list_frame = tk.Frame(self.master)
        list_frame.pack(pady=10)
        
        tk.Label(list_frame, text="參與者列表:", font=self.large_font).pack()
        self.participants_listbox = tk.Listbox(list_frame, height=7, width=50, font=self.large_font)
        self.participants_listbox.pack()
        
        # 框架：開始遊戲
        start_frame = tk.Frame(self.master)
        start_frame.pack(pady=10)
        
        start_button = tk.Button(start_frame, text="開始遊戲", command=self.start_game, font=self.large_font)
        start_button.pack()
        
        # 框架：配對區域
        pairing_frame = tk.Frame(self.master)
        pairing_frame.pack(pady=10)
        
        tk.Label(pairing_frame, text="選擇配對者:", font=self.large_font).grid(row=0, column=0, padx=5, pady=5)
        self.selector_var = tk.StringVar()
        self.selector_menu = tk.OptionMenu(pairing_frame, self.selector_var, ())
        self.selector_menu.config(width=20, font=self.large_font)
        self.selector_menu.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(pairing_frame, text="被配對者:", font=self.large_font).grid(row=1, column=0, padx=5, pady=5)
        self.selected_var = tk.StringVar()
        self.selected_menu = tk.OptionMenu(pairing_frame, self.selected_var, ())
        self.selected_menu.config(width=20, font=self.large_font)
        self.selected_menu.grid(row=1, column=1, padx=5, pady=5)
        
        pair_success_button = tk.Button(pairing_frame, text="配對成功", command=lambda: self.pair(True), font=self.large_font)
        pair_success_button.grid(row=0, column=2, padx=10, pady=5)
        
        pair_fail_button = tk.Button(pairing_frame, text="配對失敗", command=lambda: self.pair(False), font=self.large_font)
        pair_fail_button.grid(row=1, column=2, padx=10, pady=5)
        
        # 框架：遊戲狀態
        status_frame = tk.Frame(self.master)
        status_frame.pack(pady=10)
        
        tk.Label(status_frame, text="遊戲狀態:", font=self.large_font).pack()
        self.status_text = tk.Text(status_frame, height=15, width=80, state='disabled', font=self.large_font)
        self.status_text.pack()
        
    def add_participant(self):
        # 使用 simpledialog 來獲取參與者姓名
        name = simpledialog.askstring("添加參與者", "請輸入參與者的姓名:", parent=self.master)
        if name:
            name = name.strip()
            if not name:
                messagebox.showwarning("警告", "姓名不能為空。")
                return
            if name in self.participants:
                messagebox.showwarning("警告", "該姓名已存在。")
                return
            self.participants[name] = Participant(name)
            self.participants_listbox.insert(tk.END, name)
            self.update_selector_menu()
            self.update_selected_menu()
            self.log_status(f"添加參與者: {name}")
        else:
            messagebox.showinfo("取消", "未添加任何參與者。")
        
    def delete_participant(self):
        # 獲取選中的參與者
        selected_indices = self.participants_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("警告", "請選擇要刪除的參與者。")
            return
        selected_index = selected_indices[0]
        selected_name = self.participants_listbox.get(selected_index)
        
        # 確認刪除
        confirm = messagebox.askyesno("確認刪除", f"確定要刪除參與者 '{selected_name}' 嗎？")
        if not confirm:
            return
        
        # 刪除參與者
        del self.participants[selected_name]
        self.participants_listbox.delete(selected_index)
        self.log_status(f"刪除參與者: {selected_name}")
        
        # 更新其他參與者的 attempted 集合
        for participant in self.participants.values():
            if selected_name in participant.attempted:
                participant.attempted.remove(selected_name)
        
        # 更新配對選單
        self.update_selector_menu()
        self.update_selected_menu()
        
    def start_game(self):
        if len(self.participants) < 2:
            messagebox.showwarning("警告", "參與者人數不足，無法開始遊戲。")
            return
        messagebox.showinfo("開始遊戲", "遊戲開始！")
        self.log_status("遊戲已開始。")
        self.update_selector_menu()
        self.update_selected_menu()
        
    def update_selector_menu(self):
        menu = self.selector_menu['menu']
        menu.delete(0, 'end')
        available = [p.name for p in self.participants.values() if not p.paired]
        for name in available:
            menu.add_command(label=name, command=lambda value=name: self.selector_var.set(value))
        if available:
            self.selector_var.set(available[0])
        else:
            self.selector_var.set('')
            
    def update_selected_menu(self):
        menu = self.selected_menu['menu']
        menu.delete(0, 'end')
        available = [p.name for p in self.participants.values() if not p.paired]
        for name in available:
            menu.add_command(label=name, command=lambda value=name: self.selected_var.set(value))
        if available:
            self.selected_var.set(available[0])
        else:
            self.selected_var.set('')
    
    def pair(self, success):
        selector = self.selector_var.get()
        selected = self.selected_var.get()
        
        if not selector or not selected:
            messagebox.showwarning("警告", "請選擇配對者和被配對者。")
            return
        if selector == selected:
            messagebox.showwarning("警告", "不能選擇自己進行配對。")
            return
        
        selector_obj = self.participants[selector]
        selected_obj = self.participants[selected]
        
        # 檢查是否已經嘗試過
        if selected in selector_obj.attempted:
            messagebox.showwarning("警告", f"{selector} 已經嘗試過與 {selected} 配對。")
            return
        
        if success:
            # 成功配對
            selector_obj.paired = True
            selected_obj.paired = True
            selector_obj.paired_with = selected
            selected_obj.paired_with = selector
            self.last_paired = [selector, selected]
            self.log_status(f"{selector} 和 {selected} 配對成功！")
            self.log_status(f"為對方留下印跡或祝福。\n")
            messagebox.showinfo("配對成功", f"{selector} 和 {selected} 配對成功，獲得獎勵！")
            # 更新所有人的可選配對對象
            for p in self.participants.values():
                p.attempted.discard(selector)
                p.attempted.discard(selected)
            # 清除配對者和被配對者的嘗試記錄
            selector_obj.attempted.clear()
            selected_obj.attempted.clear()
        else:
            # 失敗配對
            self.log_status(f"{selector} 和 {selected} 配對失敗。\n")
            messagebox.showinfo("配對失敗", f"{selector} 和 {selected} 配對失敗。")
            # 將這對參與者加入彼此的嘗試記錄
            selector_obj.attempted.add(selected)
            selected_obj.attempted.add(selector)
        
        self.update_selector_menu()
        self.update_selected_menu()
        self.display_remaining_options()
        
        # 檢查遊戲是否結束
        if self.check_game_end():
            self.end_game()
        
    def display_remaining_options(self):
        self.log_status("目前每位參與者的剩餘可選配對對象：")
        for participant in self.participants.values():
            if not participant.paired:
                options = [name for name in self.participants if name != participant.name and not self.participants[name].paired and name not in participant.attempted]
                options_text = ', '.join(options) if options else '無'
                self.log_status(f"{participant.name}: {options_text}")
        self.log_status("\n")
        
    def log_status(self, message):
        self.status_text.config(state='normal')
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.config(state='disabled')
        self.status_text.see(tk.END)
        
    def check_game_end(self):
        available = [p for p in self.participants.values() if not p.paired]
        if not available:
            return True
        # 檢查是否還有可行的配對
        for p in available:
            possible = [name for name in self.participants if name != p.name and not self.participants[name].paired and name not in p.attempted]
            if possible:
                return False
        return True
    
    def end_game(self):
        # 檢查是否有未配對者
        unpaired = [p.name for p in self.participants.values() if not p.paired]
        if unpaired:
            unpaired_text = "、".join(unpaired)
            self.log_status(f"最後剩下未匹配的是: {unpaired_text}。他/她將獲得翻倍獎勵！\n遊戲結束!!!\n")
        else:
            last = " 和 ".join(self.last_paired)
            self.log_status(f"最後匹配成功的是: {last}。他/她們將獲得翻倍獎勵！\n")
            self.log_status("遊戲結束!!所有參與者都已成功配對。\n")

        # 印出所有成功配對的參與者配對
        self.log_status("所有成功配對的參與者配對關係：")
        for p in self.participants.values():
            if p.paired and p.paired_with:
                self.log_status(f"{p.name} 和 {p.paired_with}")
        
        # 禁用配對區域
        self.selector_menu.config(state='disabled')
        self.selected_menu.config(state='disabled')
        # 禁用刪除按鈕
        for widget in self.master.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Button) and child['text'] == "刪除參與者":
                        child.config(state='disabled')
                        
if __name__ == "__main__":
    root = tk.Tk()
    app = PairingGameGUI(root)
    root.mainloop()
