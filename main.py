#!/usr/bin/env python3
"""
📱 Finance Tracker Mobile App
Upload this file as: main.py
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.gridlayout import GridLayout
import requests
import json
import threading

class FinanceApp(App):
    def __init__(self):
        super().__init__()
        # 🔧 MODIFY THIS: Change to your laptop's IP address
        self.server_ip = "192.168.1.100"  # ← CHANGE THIS TO YOUR LAPTOP IP
        self.server_port = "5000"
        self.user_id = None
        self.user_name = ""
    
    def build(self):
        # Main container
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(8))
        
        # App title
        title = Label(
            text='💰 Finance Tracker',
            font_size='24sp',
            size_hint_y=None,
            height=dp(50),
            color=(0.2, 0.4, 0.8, 1)
        )
        main_layout.add_widget(title)
        
        # Server connection section
        connection_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(120))
        
        # Server IP input
        ip_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(35))
        ip_layout.add_widget(Label(text='Laptop IP:', size_hint_x=0.3, font_size='14sp'))
        self.ip_input = TextInput(
            text=self.server_ip,
            multiline=False,
            size_hint_x=0.7,
            font_size='14sp'
        )
        ip_layout.add_widget(self.ip_input)
        connection_layout.add_widget(ip_layout)
        
        # Connection status
        self.status_label = Label(
            text='Status: Not connected',
            size_hint_y=None,
            height=dp(25),
            font_size='12sp',
            color=(0.6, 0.6, 0.6, 1)
        )
        connection_layout.add_widget(self.status_label)
        
        # Test connection button
        test_btn = Button(
            text='🔧 Test Connection',
            size_hint_y=None,
            height=dp(40),
            background_color=(0.2, 0.6, 0.2, 1),
            font_size='14sp'
        )
        test_btn.bind(on_press=self.test_connection)
        connection_layout.add_widget(test_btn)
        
        main_layout.add_widget(connection_layout)
        
        # User setup section
        user_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(120))
        
        user_title = Label(
            text='👤 User Profile',
            size_hint_y=None,
            height=dp(25),
            font_size='16sp'
        )
        user_layout.add_widget(user_title)
        
        # Name and income inputs
        profile_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(35))
        self.name_input = TextInput(
            hint_text='Your Name',
            size_hint_x=0.6,
            multiline=False,
            font_size='14sp'
        )
        self.income_input = TextInput(
            hint_text='Income ₹',
            size_hint_x=0.4,
            multiline=False,
            input_filter='int',
            font_size='14sp'
        )
        profile_layout.add_widget(self.name_input)
        profile_layout.add_widget(self.income_input)
        user_layout.add_widget(profile_layout)
        
        # Create user button
        create_user_btn = Button(
            text='✅ Create User',
            size_hint_y=None,
            height=dp(40),
            background_color=(0.2, 0.4, 0.8, 1),
            font_size='14sp'
        )
        create_user_btn.bind(on_press=self.create_user)
        user_layout.add_widget(create_user_btn)
        
        main_layout.add_widget(user_layout)
        
        # Current user info
        self.user_info_label = Label(
            text='No user created yet',
            size_hint_y=None,
            height=dp(30),
            font_size='12sp',
            color=(0.5, 0.5, 0.5, 1)
        )
        main_layout.add_widget(self.user_info_label)
        
        # Health score display
        score_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60))
        
        score_left = BoxLayout(orientation='vertical')
        score_left.add_widget(Label(text='💳 Health Score', font_size='14sp'))
        self.score_label = Label(
            text='---',
            font_size='20sp',
            color=(0.8, 0.4, 0.2, 1)
        )
        score_left.add_widget(self.score_label)
        
        score_right = BoxLayout(orientation='vertical')
        self.grade_label = Label(text='No data', font_size='12sp', color=(0.6, 0.6, 0.6, 1))
        self.ratio_label = Label(text='---% spent', font_size='10sp', color=(0.6, 0.6, 0.6, 1))
        score_right.add_widget(self.grade_label)
        score_right.add_widget(self.ratio_label)
        
        score_layout.add_widget(score_left)
        score_layout.add_widget(score_right)
        main_layout.add_widget(score_layout)
        
        # Expense input section
        expense_title = Label(
            text='💸 Add Expense',
            size_hint_y=None,
            height=dp(25),
            font_size='16sp'
        )
        main_layout.add_widget(expense_title)
        
        # Expense text input
        self.expense_input = TextInput(
            hint_text='Describe your expense...\ne.g., "Bought coffee at Starbucks for ₹250 yesterday"',
            size_hint_y=None,
            height=dp(70),
            multiline=True,
            font_size='14sp'
        )
        main_layout.add_widget(self.expense_input)
        
        # Add expense button
        add_expense_btn = Button(
            text='➕ Add Expense',
            size_hint_y=None,
            height=dp(40),
            background_color=(0.8, 0.4, 0.2, 1),
            font_size='14sp'
        )
        add_expense_btn.bind(on_press=self.add_expense)
        main_layout.add_widget(add_expense_btn)
        
        # Quick examples
        examples_label = Label(
            text='💡 Quick Examples (tap to use):',
            size_hint_y=None,
            height=dp(25),
            font_size='12sp'
        )
        main_layout.add_widget(examples_label)
        
        examples = [
            "Coffee at Starbucks ₹250 yesterday",
            "Uber ride ₹500 today",
            "Amazon shopping ₹1200",
            "Restaurant dinner ₹800"
        ]
        
        examples_grid = GridLayout(cols=2, size_hint_y=None, height=dp(70), spacing=dp(5))
        for example in examples:
            example_btn = Button(
                text=example,
                font_size='10sp',
                background_color=(0.9, 0.9, 0.9, 1),
                color=(0.3, 0.3, 0.3, 1)
            )
            example_btn.bind(on_press=lambda x, text=example: self.set_example(text))
            examples_grid.add_widget(example_btn)
        
        main_layout.add_widget(examples_grid)
        
        # Recent expenses section
        expenses_title = Label(
            text='📊 Recent Expenses',
            size_hint_y=None,
            height=dp(30),
            font_size='16sp'
        )
        main_layout.add_widget(expenses_title)
        
        # Scrollable expenses list
        scroll = ScrollView(size_hint=(1, 0.25))
        self.expenses_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.expenses_layout.bind(minimum_height=self.expenses_layout.setter('height'))
        scroll.add_widget(self.expenses_layout)
        main_layout.add_widget(scroll)
        
        # Refresh button
        refresh_btn = Button(
            text='🔄 Refresh Dashboard',
            size_hint_y=None,
            height=dp(40),
            background_color=(0.4, 0.4, 0.4, 1),
            font_size='14sp'
        )
        refresh_btn.bind(on_press=self.refresh_dashboard)
        main_layout.add_widget(refresh_btn)
        
        return main_layout
    
    def test_connection(self, instance):
        """Test connection to backend server"""
        self.server_ip = self.ip_input.text.strip()
        if not self.server_ip:
            self.show_popup('Error', 'Please enter server IP address')
            return
        
        instance.text = '🔄 Testing...'
        instance.disabled = True
        self.status_label.text = 'Status: Testing connection...'
        
        threading.Thread(target=self._test_connection_thread, args=(instance,)).start()
    
    def _test_connection_thread(self, button):
        """Test connection in background thread"""
        try:
            url = f"http://{self.server_ip}:{self.server_port}/api/test"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                Clock.schedule_once(lambda dt: self._handle_test_result(True, button, result.get('message', 'Connected')), 0)
            else:
                Clock.schedule_once(lambda dt: self._handle_test_result(False, button, f'Server error: {response.status_code}'), 0)
                
        except requests.exceptions.RequestException as e:
            Clock.schedule_once(lambda dt: self._handle_test_result(False, button, str(e)), 0)
    
    def _handle_test_result(self, success, button, message):
        """Handle connection test result"""
        button.disabled = False
        button.text = '🔧 Test Connection'
        
        if success:
            self.status_label.text = f'Status: ✅ Connected to {self.server_ip}'
            self.status_label.color = (0.2, 0.6, 0.2, 1)
            self.show_popup('Success ✅', 'Connected to backend server!')
        else:
            self.status_label.text = f'Status: ❌ Connection failed'
            self.status_label.color = (0.8, 0.2, 0.2, 1)
            self.show_popup('Connection Failed ❌', f'Cannot connect to server.\n\nError: {message}\n\nMake sure:\n1. Backend server is running\n2. IP address is correct\n3. Same WiFi network')
    
    def create_user(self, instance):
        """Create user via API"""
        name = self.name_input.text.strip()
        income_text = self.income_input.text.strip()
        
        if not name or not income_text:
            self.show_popup('Error', 'Please enter name and income')
            return
        
        try:
            income = int(income_text)
        except ValueError:
            self.show_popup('Error', 'Please enter valid income amount')
            return
        
        instance.text = '⏳ Creating...'
        instance.disabled = True
        
        threading.Thread(target=self._create_user_thread, args=(name, income, instance)).start()
    
    def _create_user_thread(self, name, income, button):
        """Create user in background thread"""
        try:
            url = f"http://{self.server_ip}:{self.server_port}/api/user"
            data = {"name": name, "income": income}
            response = requests.post(url, json=data, timeout=10)
            result = response.json()
            
            Clock.schedule_once(lambda dt: self._handle_user_creation(result, button, name), 0)
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self._handle_user_creation({"success": False, "error": str(e)}, button, name), 0)
    
    def _handle_user_creation(self, result, button, name):
        """Handle user creation result"""
        button.disabled = False
        button.text = '✅ Create User'
        
        if result.get('success'):
            self.user_id = result['user_id']
            self.user_name = name
            self.user_info_label.text = f'👤 User: {name} (ID: {self.user_id})'
            self.user_info_label.color = (0.2, 0.6, 0.2, 1)
            
            self.show_popup('Success ✅', f'User created!\nName: {name}\nID: {self.user_id}')
            
            self.name_input.text = ''
            self.income_input.text = ''
            
            self.refresh_dashboard(None)
        else:
            self.show_popup('Error ❌', f"Failed to create user:\n{result.get('error', 'Unknown error')}")
    
    def add_expense(self, instance):
        """Add expense via API"""
        text = self.expense_input.text.strip()
        
        if not text:
            self.show_popup('Error', 'Please describe your expense')
            return
        
        if not self.user_id:
            self.show_popup('Error', 'Please create user first')
            return
        
        instance.text = '⏳ Adding...'
        instance.disabled = True
        
        threading.Thread(target=self._add_expense_thread, args=(text, instance)).start()
    
    def _add_expense_thread(self, text, button):
        """Add expense in background thread"""
        try:
            url = f"http://{self.server_ip}:{self.server_port}/api/expense"
            data = {"user_id": self.user_id, "text": text}
            response = requests.post(url, json=data, timeout=10)
            result = response.json()
            
            Clock.schedule_once(lambda dt: self._handle_expense_addition(result, button), 0)
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self._handle_expense_addition({"success": False, "error": str(e)}, button), 0)
    
    def _handle_expense_addition(self, result, button):
        """Handle expense addition result"""
        button.disabled = False
        button.text = '➕ Add Expense'
        
        if result.get('success'):
            self.expense_input.text = ''
            parsed = result.get('parsed', {})
            self.show_popup('Added ✅', f"Expense added successfully!\n\n₹{parsed.get('amount', 0)} - {parsed.get('category', 'Unknown')}\nMerchant: {parsed.get('merchant', 'Unknown')}")
            
            self.refresh_dashboard(None)
        else:
            self.show_popup('Error ❌', f"Failed to add expense:\n{result.get('error', 'Unknown error')}")
    
    def refresh_dashboard(self, instance):
        """Refresh dashboard data"""
        if not self.user_id:
            if instance:
                self.show_popup('Info', 'Please create user first')
            return
        
        if instance:
            instance.text = '🔄 Refreshing...'
            instance.disabled = True
        
        threading.Thread(target=self._refresh_dashboard_thread, args=(instance,)).start()
    
    def _refresh_dashboard_thread(self, button):
        """Refresh dashboard in background thread"""
        try:
            url = f"http://{self.server_ip}:{self.server_port}/api/dashboard/{self.user_id}"
            response = requests.get(url, timeout=10)
            result = response.json()
            
            Clock.schedule_once(lambda dt: self._handle_dashboard_data(result, button), 0)
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self._handle_dashboard_data({"error": str(e)}, button), 0)
    
    def _handle_dashboard_data(self, result, button):
        """Handle dashboard data"""
        if button:
            button.disabled = False
            button.text = '🔄 Refresh Dashboard'
        
        if result.get('success'):
            # Update health score
            health = result.get('health_score', {})
            score = health.get('score', 0)
            grade = health.get('grade', 'Unknown')
            spending_ratio = health.get('spending_ratio', 0)
            
            self.score_label.text = str(score)
            self.grade_label.text = grade
            self.ratio_label.text = f'{spending_ratio}% spent'
            
            # Color code score
            if score >= 700:
                self.score_label.color = (0.2, 0.8, 0.2, 1)  # Green
            elif score >= 500:
                self.score_label.color = (0.8, 0.6, 0.2, 1)  # Orange
            else:
                self.score_label.color = (0.8, 0.2, 0.2, 1)  # Red
            
            # Update expenses list
            self.expenses_layout.clear_widgets()
            
            expenses = result.get('recent_expenses', [])
            if not expenses:
                no_expenses = Label(
                    text='No expenses yet.\nAdd some above! 👆',
                    size_hint_y=None,
                    height=dp(50),
                    color=(0.5, 0.5, 0.5, 1),
                    font_size='12sp'
                )
                self.expenses_layout.add_widget(no_expenses)
            else:
                for expense in expenses[:8]:  # Show last 8 expenses
                    expense_layout = BoxLayout(
                        orientation='horizontal',
                        size_hint_y=None,
                        height=dp(35)
                    )
                    
                    details_text = f"{expense['category']}\n{expense['date']}"
                    details_label = Label(
                        text=details_text,
                        halign='left',
                        font_size='10sp',
                        text_size=(dp(150), None)
                    )
                    
                    amount_label = Label(
                        text=f"₹{expense['amount']}",
                        size_hint_x=None,
                        width=dp(70),
                        color=(0.8, 0.2, 0.2, 1),
                        font_size='12sp'
                    )
                    
                    expense_layout.add_widget(details_label)
                    expense_layout.add_widget(amount_label)
                    
                    self.expenses_layout.add_widget(expense_layout)
        else:
            self.show_popup('Error', f"Failed to load dashboard:\n{result.get('error', 'Unknown error')}")
    
    def set_example(self, text):
        """Set example text in expense input"""
        self.expense_input.text = text
    
    def show_popup(self, title, message):
        """Show popup message"""
        popup = Popup(
            title=title,
            content=Label(
                text=message,
                text_size=(dp(250), None),
                halign='center',
                font_size='13sp'
            ),
            size_hint=(0.85, 0.6)
        )
        popup.open()

if __name__ == '__main__':
    FinanceApp().run()