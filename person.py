from tkinter import *
from tkinter import messagebox

class Person():
    def __init__(self, name, age, has_mobile):
        """Initialise a person"""
        self.name = name
        self.age = age
        self.has_mobile = has_mobile

class GUI:
    def __init__(self, parent):
        """Initialise the GUI"""
        self.parent = parent

        self.people = []

        # Create frames
        self.collect_frame = Frame(parent)
        self.view_frame = Frame(parent)

        # Create collection title and button
        self.collect_label = Label(self.collect_frame, text="Collecting Person Data")
        self.leave_collect_btn = Button(self.collect_frame, text="View All", command=self.view_data)
        self.leave_collect_btn.configure(state=DISABLED)
        self.collect_label.grid(column=0, row=0)
        self.leave_collect_btn.grid(column=1, row=0, columnspan=2)

        # Create collection labels and entries
        self.name_label = Label(self.collect_frame, text="Name: ")
        self.age_label = Label(self.collect_frame, text="Age: ")
        self.mobile_label = Label(self.collect_frame, text="Do you have a mobile phone?")
        self.name_entry = Entry(self.collect_frame)
        self.age_entry = Entry(self.collect_frame)
        
        # Create mobile radiobuttons
        self.mobile_var = IntVar(value = 0)
        self.mobile_no = Radiobutton(self.collect_frame, variable=self.mobile_var, value=0, text="No")
        self.mobile_yes = Radiobutton(self.collect_frame, variable=self.mobile_var, value=1, text="Yes")

        # Place collection labels, entries, and radiobuttons
        self.name_label.grid(column=0, row=1)
        self.age_label.grid(column=0, row=2)
        self.mobile_label.grid(column=0, row=3)
        self.name_entry.grid(column=1, row=1, columnspan=2)
        self.age_entry.grid(column=1, row=2, columnspan=2)
        self.mobile_no.grid(column=1, row=3)
        self.mobile_yes.grid(column=2, row=3)

        # Create add person button
        self.add_person_btn = Button(self.collect_frame, text="Add Data", command=self.add_person)
        self.add_person_btn.grid(column=0, row=4, columnspan=3)

        # Create view title and button
        self.view_label = Label(self.view_frame, text="Displaying Person Data")
        self.leave_view_btn = Button(self.view_frame, text="Add New Person", command=self.collect_data)
        self.view_label.grid(column=0, row=0)
        self.leave_view_btn.grid(column=2, row=0)

        # Create view labels
        self.name_label_view = Label(self.view_frame, text="Name: ")
        self.age_label_view = Label(self.view_frame, text="Age: ")
        self.mobile_label_view = Label(self.view_frame, text="")

        # Create view display labels
        self.name_display_view = Label(self.view_frame, text="")
        self.age_display_view = Label(self.view_frame, text="")

        # Place view labels, and display labels
        self.name_label_view.grid(column=0, row=1)
        self.age_label_view.grid(column=0, row=2)
        self.mobile_label_view.grid(column=0, row=3, columnspan=3)
        self.name_display_view.grid(column=2, row=1)
        self.age_display_view.grid(column=2, row=2)

        # Define view indexing for collection and view buttons
        self.cur_person = 0
        self.prev_btn = Button(self.view_frame, text="Previous", command=lambda : self.change_person(-1))
        self.next_btn = Button(self.view_frame, text="Next", command=lambda : self.change_person(1))
        self.index_label = Label(self.view_frame, text="1/1")
        self.prev_btn.grid(column=0, row=4)
        self.next_btn.grid(column=2, row=4)
        self.index_label.grid(column=1, row=4)

        # Display the collection frame first
        self.collect_frame.pack()

    def view_data(self):
        """Frame is switched to data viewing"""
        self.collect_frame.pack_forget()
        self.view_frame.pack()
        self.update_view() # Update collection view

    def collect_data(self):
        """Frame is switched to data collection"""
        self.collect_frame.pack()
        self.view_frame.pack_forget()

    def add_person(self):
        """Add a new person to the collection"""
        try:
            age = int(self.age_entry.get())
            if age < 0: # Age was negative
                messagebox.showerror(title="Age error", message=f"Invalid age: {self.age_entry.get()}\nAge cannot be negative.")
                self.age_entry.focus_set()
                return
        except: # Age was not an integer
            messagebox.showerror(title="Age error", message=f"Invalid age: {self.age_entry.get()}\nAge must be a discrete number.")
            self.age_entry.focus_set()
            return
        # All entries valid, add person to collection, clear all entries
        self.people.append(Person(self.name_entry.get(), self.age_entry.get(), self.mobile_var.get()))
        self.name_entry.delete(0, END)
        self.age_entry.delete(0, END)
        self.mobile_var.set(0)
        self.leave_collect_btn.configure(state=NORMAL)

    def update_view(self):
        """Update the collection frame and labels for the current person"""
        if len(self.people) == 0: # No peeople in collection, halt
            return
        if len(self.people) == 1: # Only one person in collection, disable increment buttons
            self.prev_btn.configure(state=DISABLED)
            self.next_btn.configure(state=DISABLED)
        else: # More than one person in collection, enable increment buttons
            self.prev_btn.configure(state=NORMAL)
            self.next_btn.configure(state=NORMAL)
        # Update collection labels for the current person
        index = self.cur_person
        self.name_display_view.configure(text=f"{self.people[index].name}")
        self.age_display_view.configure(text=f"{self.people[index].age}")
        self.mobile_label_view.configure(text=f"{self.people[index].name} {"has" if self.people[index].has_mobile == 1 else "does not have"} a mobile phone")
        self.index_label.configure(text=f"{self.cur_person + 1}/{len(self.people)}")

    def change_person(self, index):
        """Increment the current person selection in the collection"""
        self.cur_person += index
        length = len(self.people)
        self.cur_person = ((self.cur_person % length) + length) % length # Loop index at boundaries
        self.update_view()

if __name__=="__main__":
    """Main routine"""
    root = Tk()
    root.geometry("300x250")
    buttons = GUI(root)
    root.mainloop()