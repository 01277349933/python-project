#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
آلة حاسبة بسيطة باستخدام Tkinter
Calculator App using Tkinter GUI
"""

import tkinter as tk
from tkinter import messagebox
import math

class Calculator:
    """فئة الآلة الحاسبة الرئيسية"""
    
    def __init__(self, root):
        """تهيئة الآلة الحاسبة"""
        self.root = root
        self.root.title("الآلة الحاسبة - Calculator")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # متغيرات الحالة
        self.current_input = ""
        self.total = 0
        self.operation = None
        self.new_number = True
        
        # إعداد الواجهة الرسومية
        self.setup_ui()
        
    def setup_ui(self):
        """إعداد واجهة المستخدم الرسومية"""
        # إعداد الألوان والخطوط
        bg_color = "#2C3E50"
        button_color = "#34495E"
        number_color = "#3498DB"
        operator_color = "#E74C3C"
        equals_color = "#27AE60"
        text_color = "white"
        
        self.root.configure(bg=bg_color)
        
        # شاشة العرض
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        display_frame = tk.Frame(self.root, bg=bg_color)
        display_frame.pack(pady=20, padx=20, fill=tk.X)
        
        self.display = tk.Entry(
            display_frame,
            textvariable=self.display_var,
            font=("Arial", 24, "bold"),
            justify="right",
            state="readonly",
            bg="white",
            fg="black",
            bd=0,
            relief=tk.FLAT
        )
        self.display.pack(fill=tk.X, ipady=10)
        
        # إطار الأزرار
        buttons_frame = tk.Frame(self.root, bg=bg_color)
        buttons_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # تعريف الأزرار
        buttons = [
            ['C', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]
        
        # إنشاء الأزرار
        for i, row in enumerate(buttons):
            for j, button_text in enumerate(row):
                if button_text == '0':
                    # زر الصفر يأخذ مساحة أكبر
                    btn = tk.Button(
                        buttons_frame,
                        text=button_text,
                        font=("Arial", 18, "bold"),
                        bg=number_color,
                        fg=text_color,
                        bd=0,
                        relief=tk.FLAT,
                        command=lambda x=button_text: self.button_click(x)
                    )
                    btn.grid(row=i, column=j, columnspan=2, sticky="nsew", padx=2, pady=2)
                elif button_text == '=':
                    # زر المساواة
                    btn = tk.Button(
                        buttons_frame,
                        text=button_text,
                        font=("Arial", 18, "bold"),
                        bg=equals_color,
                        fg=text_color,
                        bd=0,
                        relief=tk.FLAT,
                        command=lambda x=button_text: self.button_click(x)
                    )
                    btn.grid(row=i, column=j+1, sticky="nsew", padx=2, pady=2)
                else:
                    # باقي الأزرار
                    if button_text in ['÷', '×', '-', '+', '%', '±', 'C']:
                        color = operator_color if button_text in ['÷', '×', '-', '+'] else button_color
                    else:
                        color = number_color
                    
                    btn = tk.Button(
                        buttons_frame,
                        text=button_text,
                        font=("Arial", 18, "bold"),
                        bg=color,
                        fg=text_color,
                        bd=0,
                        relief=tk.FLAT,
                        command=lambda x=button_text: self.button_click(x)
                    )
                    btn.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)
        
        # تكوين الشبكة للتمدد
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            buttons_frame.grid_columnconfigure(j, weight=1)
    
    def button_click(self, char):
        """معالجة النقر على الأزرار"""
        try:
            if char.isdigit():
                self.number_click(char)
            elif char == '.':
                self.decimal_click()
            elif char in ['÷', '×', '-', '+']:
                self.operator_click(char)
            elif char == '=':
                self.equals_click()
            elif char == 'C':
                self.clear_click()
            elif char == '±':
                self.plus_minus_click()
            elif char == '%':
                self.percent_click()
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}")
            self.clear_all()
    
    def number_click(self, number):
        """معالجة النقر على الأرقام"""
        if self.new_number:
            self.current_input = number
            self.new_number = False
        else:
            if len(self.current_input) < 15:  # حد أقصى للأرقام
                self.current_input += number
        
        self.display_var.set(self.current_input)
    
    def decimal_click(self):
        """معالجة النقر على العلامة العشرية"""
        if self.new_number:
            self.current_input = "0."
            self.new_number = False
        elif '.' not in self.current_input:
            self.current_input += '.'
        
        self.display_var.set(self.current_input)
    
    def operator_click(self, operator):
        """معالجة النقر على العمليات"""
        if not self.new_number:
            if self.operation:
                self.equals_click()
            else:
                self.total = float(self.current_input)
        
        self.operation = operator
        self.new_number = True
    
    def equals_click(self):
        """معالجة النقر على زر المساواة"""
        if self.operation and not self.new_number:
            try:
                current_number = float(self.current_input)
                
                if self.operation == '+':
                    result = self.total + current_number
                elif self.operation == '-':
                    result = self.total - current_number
                elif self.operation == '×':
                    result = self.total * current_number
                elif self.operation == '÷':
                    if current_number == 0:
                        messagebox.showerror("خطأ", "لا يمكن القسمة على صفر!")
                        return
                    result = self.total / current_number
                
                # تنسيق النتيجة
                if result == int(result):
                    result = int(result)
                else:
                    result = round(result, 10)
                
                self.display_var.set(str(result))
                self.current_input = str(result)
                self.total = 0
                self.operation = None
                self.new_number = True
                
            except ValueError:
                messagebox.showerror("خطأ", "إدخال غير صالح!")
                self.clear_all()
    
    def clear_click(self):
        """معالجة النقر على زر المسح"""
        self.clear_all()
    
    def clear_all(self):
        """مسح جميع البيانات"""
        self.current_input = ""
        self.total = 0
        self.operation = None
        self.new_number = True
        self.display_var.set("0")
    
    def plus_minus_click(self):
        """معالجة تغيير الإشارة"""
        if self.current_input and self.current_input != "0":
            if self.current_input.startswith('-'):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.display_var.set(self.current_input)
    
    def percent_click(self):
        """معالجة النسبة المئوية"""
        if self.current_input:
            try:
                result = float(self.current_input) / 100
                if result == int(result):
                    result = int(result)
                self.current_input = str(result)
                self.display_var.set(self.current_input)
            except ValueError:
                messagebox.showerror("خطأ", "إدخال غير صالح!")

def main():
    """الدالة الرئيسية لتشغيل التطبيق"""
    root = tk.Tk()
    app = Calculator(root)
    
    # ربط اختصارات لوحة المفاتيح
    root.bind('<Key>', lambda event: app.keyboard_input(event))
    root.focus_set()
    
    # تشغيل التطبيق
    root.mainloop()

# إضافة دعم لوحة المفاتيح
def keyboard_input(self, event):
    """معالجة إدخال لوحة المفاتيح"""
    key = event.char
    if key.isdigit():
        self.button_click(key)
    elif key == '.':
        self.button_click('.')
    elif key == '+':
        self.button_click('+')
    elif key == '-':
        self.button_click('-')
    elif key == '*':
        self.button_click('×')
    elif key == '/':
        self.button_click('÷')
    elif key == '=' or event.keysym == 'Return':
        self.button_click('=')
    elif event.keysym == 'Escape':
        self.button_click('C')

# ربط دالة لوحة المفاتيح بالفئة
Calculator.keyboard_input = keyboard_input

if __name__ == "__main__":
    main()

