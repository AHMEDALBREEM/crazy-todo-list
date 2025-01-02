import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from datetime import datetime
import ttkbootstrap as tb
from ttkbootstrap.constants import *

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.style = tb.Style(theme="vapor")
        self.root.title("Crazy To-Do List")
        self.root.geometry("600x700")
        self.root.configure(bg="#1e1e2f")

        # Enhanced task list
        self.tasks = []
        self.categories = ["Work", "Personal", "Shopping", "Other"]
        self.priorities = ["High", "Medium", "Low"]

        # Create gradient background
        self.canvas = tk.Canvas(self.root, bg="#1e1e2f", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.create_gradient()

        # Create UI elements
        self.create_widgets()

        # Start animation
        self.animate_gradient()

    def create_gradient(self):
        self.gradient = self.canvas.create_rectangle(
            0, 0, self.root.winfo_width(), self.root.winfo_height(),
            fill="#1e1e2f", outline=""
        )
        self.colors = ["#ff9a9e", "#fad0c4", "#a1c4fd", "#c2e9fb"]
        self.color_index = 0

    def animate_gradient(self):
        color1 = self.colors[self.color_index]
        color2 = self.colors[(self.color_index + 1) % len(self.colors)]
        self.canvas.itemconfig(self.gradient, fill="")
        self.canvas.create_rectangle(
            0, 0, self.root.winfo_width(), self.root.winfo_height(),
            fill=color1, outline="", tags="gradient"
        )
        self.canvas.create_rectangle(
            0, 0, self.root.winfo_width(), self.root.winfo_height(),
            fill=color2, outline="", tags="gradient"
        )
        self.canvas.lower("gradient")
        self.color_index = (self.color_index + 1) % len(self.colors)
        self.root.after(3000, self.animate_gradient)

    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.canvas, bg="#1e1e2f")
        main_frame.pack(pady=40, padx=40, fill=tk.BOTH, expand=True)

        # Title label
        title = tk.Label(
            main_frame,
            text="Crazy To-Do List",
            font=("Comic Sans MS", 24, "bold"),
            fg="white",
            bg="#1e1e2f"
        )
        title.pack(pady=(0, 20))

        # Task list frame
        list_frame = tk.Frame(main_frame, bg="")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Listbox
        self.task_list = tk.Listbox(
            list_frame,
            width=40,
            height=15,
            bg="#333333",
            fg="white",
            selectbackground="#555555",
            yscrollcommand=scrollbar.set,
            font=("Arial", 12),
            relief=tk.FLAT,
            highlightthickness=0
        )
        self.task_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_list.yview)

        # Task input frame
        input_frame = tk.Frame(main_frame, bg="#1e1e2f")
        input_frame.pack(pady=10)

        # Task description
        self.task_entry = tb.Entry(
            input_frame,
            width=30,
            bootstyle="light",
            font=("Arial", 12)
        )
        self.task_entry.grid(row=0, column=0, padx=5, pady=5)

        # Category frame
        category_frame = tk.Frame(input_frame, bg="#1e1e2f")
        category_frame.grid(row=0, column=1, padx=5, pady=5)
        
        # Category dropdown
        self.category_var = tk.StringVar(value=self.categories[0])
        self.category_menu = tb.Combobox(
            category_frame,
            textvariable=self.category_var,
            values=self.categories,
            width=10,
            bootstyle="light"
        )
        self.category_menu.pack(side=tk.LEFT)
        
        # Add category button
        add_category_button = tb.Button(
            category_frame,
            text="+",
            width=2,
            bootstyle="info-outline",
            command=self.add_category
        )
        add_category_button.pack(side=tk.LEFT, padx=5)

        # Priority dropdown
        self.priority_var = tk.StringVar(value=self.priorities[1])
        priority_menu = tb.Combobox(
            input_frame,
            textvariable=self.priority_var,
            values=self.priorities,
            width=8,
            bootstyle="light"
        )
        priority_menu.grid(row=0, column=2, padx=5, pady=5)

        # Due date entry
        self.due_date_entry = tb.DateEntry(
            input_frame,
            width=12,
            bootstyle="light"
        )
        self.due_date_entry.grid(row=0, column=3, padx=5, pady=5)

        # Buttons frame
        button_frame = tk.Frame(main_frame, bg="#1e1e2f")
        button_frame.pack(pady=10)

        # Search frame
        search_frame = tk.Frame(main_frame, bg="#1e1e2f")
        search_frame.pack(pady=10)

        # Search entry
        self.search_entry = tb.Entry(
            search_frame,
            width=30,
            bootstyle="light",
            font=("Arial", 12)
        )
        self.search_entry.pack(side=tk.LEFT, padx=5)

        # Search button
        search_button = tb.Button(
            search_frame,
            text="🔍 Search",
            width=10,
            bootstyle="info-outline",
            command=self.search_tasks
        )
        search_button.pack(side=tk.LEFT, padx=5)

        # Add task button
        add_button = tb.Button(
            button_frame,
            text="➕ Add Task",
            width=12,
            bootstyle="success-outline",
            command=self.add_task
        )
        add_button.pack(side=tk.LEFT, padx=5)

        # Complete task button
        complete_button = tb.Button(
            button_frame,
            text="✔️ Complete",
            width=12,
            bootstyle="info-outline",
            command=self.toggle_complete
        )
        complete_button.pack(side=tk.LEFT, padx=5)

        # Edit task button
        edit_button = tb.Button(
            button_frame,
            text="✏️ Edit",
            width=12,
            bootstyle="warning-outline",
            command=self.edit_task
        )
        edit_button.pack(side=tk.LEFT, padx=5)

        # Remove task button
        remove_button = tb.Button(
            button_frame,
            text="❌ Remove",
            width=12,
            bootstyle="danger-outline",
            command=self.remove_task
        )
        remove_button.pack(side=tk.LEFT, padx=5)

        # Sort button
        sort_button = tb.Button(
            button_frame,
            text="🔽 Sort",
            width=12,
            bootstyle="secondary-outline",
            command=self.sort_tasks
        )
        sort_button.pack(side=tk.LEFT, padx=5)

    def add_task(self):
        task = self.task_entry.get()
        if task:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            due_date = self.due_date_entry.entry.get()
            category = self.category_var.get()
            priority = self.priority_var.get()
            
            task_data = {
                "task": task,
                "date": timestamp,
                "due_date": due_date,
                "category": category,
                "priority": priority,
                "completed": False
            }
            
            # Format task display
            priority_icon = "❗" if priority == "High" else "🔸" if priority == "Medium" else "🔹"
            task_display = f"{priority_icon} {task} ({category})"
            if due_date:
                task_display += f" 📅 {due_date}"
            
            self.tasks.append(task_data)
            self.task_list.insert(tk.END, task_display)
            self.task_list.itemconfig(tk.END, {'fg': 'white'})
            
            # Clear input fields
            self.task_entry.delete(0, tk.END)
            self.due_date_entry.entry.delete(0, tk.END)
            self.category_var.set(self.categories[0])
            self.priority_var.set(self.priorities[1])
        else:
            messagebox.showwarning("Warning", "Please enter a task!", parent=self.root)

    def toggle_complete(self):
        try:
            selected_index = self.task_list.curselection()[0]
            task_data = self.tasks[selected_index]
            task_data["completed"] = not task_data["completed"]
            
            # Update display
            task_text = self.task_list.get(selected_index)
            if task_data["completed"]:
                self.task_list.itemconfig(selected_index, {'fg': 'gray'})
                self.task_list.delete(selected_index)
                self.task_list.insert(selected_index, f"✔️ {task_text}")
            else:
                self.task_list.itemconfig(selected_index, {'fg': 'white'})
                self.task_list.delete(selected_index)
                self.task_list.insert(selected_index, task_text.replace("✔️ ", ""))
                
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task!", parent=self.root)

    def add_category(self):
        new_category = tk.simpledialog.askstring("New Category", "Enter new category name:")
        if new_category and new_category not in self.categories:
            self.categories.append(new_category)
            self.category_menu['values'] = self.categories
            self.category_var.set(new_category)

    def search_tasks(self):
        search_term = self.search_entry.get().lower()
        self.task_list.delete(0, tk.END)
        
        for task in self.tasks:
            if search_term in task["task"].lower() or search_term in task["category"].lower():
                self._insert_task(task)
        
        # Refresh the task list to maintain grouping/sorting
        if hasattr(self, 'current_group_by'):
            self.refresh_grouped_task_list(self.current_group_by)

    def sort_tasks(self):
        # Create sorting options window
        sort_window = tb.Toplevel(self.root)
        sort_window.title("Sort/Group Tasks")
        sort_window.geometry("300x200")
        sort_window.configure(bg="#1e1e2f")
        
        # Sorting options
        sort_var = tk.StringVar(value="priority")
        
        # Priority radio button
        priority_radio = tb.Radiobutton(
            sort_window,
            text="Group by Priority",
            variable=sort_var,
            value="priority",
            bootstyle="info"
        )
        priority_radio.pack(pady=10)
        
        # Category radio button
        category_radio = tb.Radiobutton(
            sort_window,
            text="Group by Category",
            variable=sort_var,
            value="category",
            bootstyle="info"
        )
        category_radio.pack(pady=10)
        
        # Due date radio button
        due_date_radio = tb.Radiobutton(
            sort_window,
            text="Group by Due Date",
            variable=sort_var,
            value="due_date",
            bootstyle="info"
        )
        due_date_radio.pack(pady=10)
        
        # Apply button
        def apply_sort():
            sort_by = sort_var.get()
            if sort_by == "priority":
                self.tasks.sort(key=lambda x: self.priorities.index(x["priority"]))
            elif sort_by == "category":
                self.tasks.sort(key=lambda x: x["category"])
            elif sort_by == "due_date":
                self.tasks.sort(key=lambda x: x["due_date"] or "9999-99-99")  # Sort tasks without due date last
            self.refresh_grouped_task_list(sort_by)
            sort_window.destroy()
            
        apply_button = tb.Button(
            sort_window,
            text="Apply",
            width=10,
            bootstyle="success-outline",
            command=apply_sort
        )
        apply_button.pack(pady=10)

    def refresh_grouped_task_list(self, group_by):
        self.task_list.delete(0, tk.END)
        
        if group_by == "priority":
            # Group by priority
            for priority in self.priorities:
                self.task_list.insert(tk.END, f"━━━━━━━━━━ {priority} Priority ━━━━━━━━━━")
                self.task_list.itemconfig(tk.END, {'fg': '#FFD700'})
                for task in self.tasks:
                    if task["priority"] == priority:
                        self._insert_task(task)
                        
        elif group_by == "category":
            # Group by category
            for category in self.categories:
                self.task_list.insert(tk.END, f"━━━━━━━━━━ {category} ━━━━━━━━━━")
                self.task_list.itemconfig(tk.END, {'fg': '#FFD700'})
                for task in self.tasks:
                    if task["category"] == category:
                        self._insert_task(task)
                        
        elif group_by == "due_date":
            # Group by due date
            dates = sorted(set(task["due_date"] for task in self.tasks if task["due_date"]))
            for date in dates:
                self.task_list.insert(tk.END, f"━━━━━━━━━━ Due: {date} ━━━━━━━━━━")
                self.task_list.itemconfig(tk.END, {'fg': '#FFD700'})
                for task in self.tasks:
                    if task["due_date"] == date:
                        self._insert_task(task)
            # Tasks without due date
            self.task_list.insert(tk.END, "━━━━━━━━━━ No Due Date ━━━━━━━━━━")
            self.task_list.itemconfig(tk.END, {'fg': '#FFD700'})
            for task in self.tasks:
                if not task["due_date"]:
                    self._insert_task(task)
                    
    def is_task_expired(self, task):
        if not task["due_date"]:
            return False
        try:
            due_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
            return due_date < datetime.now().date()
        except ValueError:
            return False

    def _insert_task(self, task):
        if self.is_task_expired(task):
            return
            
        priority_icon = "❗" if task["priority"] == "High" else "🔸" if task["priority"] == "Medium" else "🔹"
        task_display = f"{priority_icon} {task['task']} ({task['category']})"
        if task["due_date"]:
            task_display += f" 📅 {task['due_date']}"
        if task["completed"]:
            task_display = f"✔️ {task_display}"
        self.task_list.insert(tk.END, task_display)
        self.task_list.itemconfig(tk.END, {'fg': 'gray' if task["completed"] else 'white'})

    def edit_task(self):
        try:
            selected_index = self.task_list.curselection()[0]
            selected_task = self.tasks[selected_index]
            
            # Create edit window
            edit_window = tb.Toplevel(self.root)
            edit_window.title("Edit Task")
            edit_window.geometry("400x200")
            edit_window.configure(bg="#1e1e2f")
            
            # Entry field with current task
            edit_entry = tb.Entry(
                edit_window,
                width=30,
                bootstyle="light",
                font=("Arial", 12)
            )
            edit_entry.insert(0, selected_task["task"])
            edit_entry.pack(pady=40)
            
            # Save button
            def save_changes():
                new_task = edit_entry.get()
                if new_task:
                    # Update task while preserving all properties
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                    self.tasks[selected_index].update({
                        "task": new_task,
                        "date": timestamp
                    })
                    self.task_list.delete(selected_index)
                    self.task_list.insert(
                        selected_index,
                        f"📝 {new_task} (edited: {timestamp})"
                    )
                    self.task_list.itemconfig(selected_index, {'fg': 'white'})
                    edit_window.destroy()
                else:
                    messagebox.showwarning("Warning", "Task cannot be empty!", parent=edit_window)
            
            save_button = tb.Button(
                edit_window,
                text="💾 Save",
                width=15,
                bootstyle="success-outline",
                command=save_changes
            )
            save_button.pack()
            
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to edit!", parent=self.root)

    def remove_task(self):
        try:
            selected_index = self.task_list.curselection()[0]
            self.task_list.delete(selected_index)
            self.tasks.pop(selected_index)
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to remove!", parent=self.root)

if __name__ == "__main__":
    root = tb.Window(themename="vapor")
    app = TodoApp(root)
    root.mainloop()
