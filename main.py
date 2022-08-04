import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, Tk, Listbox, ANCHOR, Button
import json

class Item():
    def __init__(self, name, type, count, place):
        self.name = name
        self.type = type
        self.count = count
        self.place = place

    def serilize(items):
        datas = []

        for item in items:
            data = {
                "name": item.name,
                "type": item.type,
                "count": item.count,
                "place": item.place,
            }
            datas.append(data)
        return json.dumps(datas)

    def de_serilize(j_data):
        try:
            data = []
            datas = json.loads(j_data)
            for d in datas:
                data.append(Item(d['name'], d['type'], d['count'], d['place']))
        except:
            data = []
        return data

def enter_data(root, items):
    label = ttk.Label(root, text='Data enter Page')
    label.pack(ipadx=10, ipady=10)
    data = ttk.Frame(root)
    data.pack(padx=10, pady=10, fill='x', expand=True)

    name = tk.StringVar()
    type = tk.StringVar()
    count = tk.StringVar()
    place = tk.StringVar()

    def submit_clicked():
        item = Item(name.get(), type.get(), count.get(), place.get())
        items.append(item)
        messagebox.showinfo(
            title='Information',
            message="Added"
        )
        root.destroy()
        with open('data.txt', 'w') as f:
            f.write(Item.serilize(items))
            f.close()

    name_label = ttk.Label(data, text="Name:")
    name_label.pack(fill='x', expand=True)

    name_entry = ttk.Entry(data, textvariable=name)
    name_entry.pack(fill='x', expand=True)
    name_entry.focus()

    type_label = ttk.Label(data, text="Type:")
    type_label.pack(fill='x', expand=True)

    type_entry = ttk.Entry(data, textvariable=type)
    type_entry.pack(fill='x', expand=True)

    count_label = ttk.Label(data, text="Count:")
    count_label.pack(fill='x', expand=True)

    count_entry = ttk.Entry(data, textvariable=count)
    count_entry.pack(fill='x', expand=True)

    place_label = ttk.Label(data, text="Place:")
    place_label.pack(fill='x', expand=True)

    place_entry = ttk.Entry(data, textvariable=place)
    place_entry.pack(fill='x', expand=True)

    submit_button = ttk.Button(data, text="Submit", command=submit_clicked)
    submit_button.pack(fill='x', expand=True, pady=10)

def search_show_data(root, items):
    win = Toplevel(root)
    type_label = ttk.Label(win, text="This is school's searched items:")
    listbox = Listbox(win)
    for i, item in enumerate(items, start=1):

        item_data = str(i) + ")    " + item.name + " - " + item.type + " - " + item.count + " - " + item.place
        listbox.insert(i, item_data)
        # ttk.Label(win, text=item_data).pack(fill='x', expand=True, pady=10)
    type_label.pack()
    listbox.pack(fill='x', expand=True, pady=30)

def search(root, items):
    def show_data_clicked():
        name_searched_items = []
        type_searched_items = []
        searched_items = []
        searched_name = name.get()
        searched_type = type.get()
        for item in items:

            if searched_name == "":
                searched_name = None
            if searched_type == "":
                searched_type = None
            if searched_name is not None:
                if str(item.name).find(searched_name) != -1:
                    name_searched_items.append(item)
            if searched_type is not None:
                if str(item.type).find(searched_type) != -1:
                    type_searched_items.append(item)
        if searched_name is None:
            searched_items = type_searched_items
        elif searched_type is None:
            searched_items = name_searched_items
        else:
            [searched_items.append(d) for d in type_searched_items if d in name_searched_items]
        win.destroy()
        search_show_data(root, searched_items)
    win = Toplevel(root)
    name = tk.StringVar()
    type = tk.StringVar()
    name_label = ttk.Label(win, text="Name:")
    name_label.pack(fill='x', expand=True)

    name_entry = ttk.Entry(win, textvariable=name)
    name_entry.pack(fill='x', expand=True)

    type_label = ttk.Label(win, text="Type:")
    type_label.pack(fill='x', expand=True)

    type_entry = ttk.Entry(win, textvariable=type)
    type_entry.pack(fill='x', expand=True)

    submit_button = ttk.Button(win, text="Show data", command=show_data_clicked)
    submit_button.pack(fill='x', expand=True, pady=10)

def show_data(root, items):
    win = Toplevel(root)

    def search_clicked():
        win.destroy()
        search(root, items)

    type_label = ttk.Label(win, text="This is school's items:")
    listbox = Listbox(win)
    for i, item in enumerate(items, start=1):
        item_data = str(i) + ")    " + item.name + " - " + item.type + " - " + item.count + " - " + item.place
        listbox.insert(i, item_data)
        # ttk.Label(win, text=item_data).pack(fill='x', expand=True, pady=10)
    type_label.pack()
    def selected_item():
        for i in listbox.curselection():
            item = listbox.get(i)
            splited = item.split(' - ')
            name = splited[0].split(')    ')[1]
            type = splited[1]
            count = splited[2]
            place = splited[3]

            for i in items:
                if i.name == name and i.type == type and i.count == count and i.place == place:
                    items.remove(i)
            with open('data.txt', 'w') as f:
                f.write(Item.serilize(items))
                f.close()
        win.destroy()
        show_data(root, items)
    btn = Button(win, text="delete", command=selected_item)
    listbox.pack(fill='x', expand=True, pady=30)
    btn.pack()
    submit_button = ttk.Button(win, text="Search", command=search_clicked)
    submit_button.pack(fill='y', expand=True, pady=10)


def main():
    items = []
    try:
        with open('data.txt', 'r') as f:
            j_data= f.read()
            items = Item.de_serilize(j_data)
            f.close()
    except:
        with open('data.txt', 'w') as f:
            items = []
            f.close()

    root = tk.Tk()
    root.geometry('300x200')
    label = ttk.Label(root, text='Wellcome!')
    label.pack(ipadx=10, ipady=10)
    def enter_data_clicked():
        win = Toplevel(root)
        enter_data(win, items)
    def show_data_clicked():
        show_data(root, items)
    submit_button = ttk.Button(root, text="Enter data", command=enter_data_clicked)
    submit_button.pack(fill='x', expand=True, pady=10)
    submit_button = ttk.Button(root, text="Show data", command=show_data_clicked)
    submit_button.pack(fill='x', expand=True, pady=10)
    root.mainloop()

if __name__ == '__main__':
    main()
