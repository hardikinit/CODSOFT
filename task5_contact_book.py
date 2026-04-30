import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import platform

IS_MAC = platform.system() == "Darwin"

DATA_FILE = "contacts.json"

BG = "#f7f6f3"
HEADER_BG = "#1e293b"
TEXT = "#1a1a2e"
ACCENT = "#3b82f6"
GREEN = "#16a34a"
RED = "#dc2626"
ORANGE = "#d97706"
GRAY = "#6b7280"
CARD = "#ffffff"
MUTED = "#9ca3af"
BORDER = "#e2e8f0"


def load_contacts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_contacts():
    with open(DATA_FILE, "w") as f:
        json.dump(contacts, f, indent=2)


def refresh_table(data=None):
    for row in tree.get_children():
        tree.delete(row)
    source = data if data is not None else contacts
    for i, c in enumerate(source):
        tag = "even" if i % 2 == 0 else "odd"
        tree.insert("", tk.END, iid=str(i),
                    values=(c["name"], c["phone"], c["email"], c["address"]),
                    tags=(tag,))


def get_selected_idx():
    sel = tree.selection()
    if not sel:
        messagebox.showinfo("Nothing selected", "Click a contact in the table first.")
        return None
    iid = sel[0]
    name = tree.item(iid)["values"][0]
    phone = tree.item(iid)["values"][1]
    for i, c in enumerate(contacts):
        if c["name"] == name and c["phone"] == phone:
            return i
    return None


def add_contact():
    name = e_name.get().strip()
    phone = e_phone.get().strip()
    email = e_email.get().strip()
    addr = e_addr.get().strip()
    if not name or not phone:
        messagebox.showwarning("Missing fields", "Name and Phone are required.")
        return
    for c in contacts:
        if c["phone"] == phone:
            messagebox.showwarning("Duplicate phone", f"Phone {phone} already exists.")
            return
    contacts.append({"name": name, "phone": phone, "email": email, "address": addr})
    save_contacts()
    refresh_table()
    clear_form()
    messagebox.showinfo("Added", f"'{name}' saved!")


def update_contact():
    idx = get_selected_idx()
    if idx is None:
        return
    name = e_name.get().strip()
    phone = e_phone.get().strip()
    if not name or not phone:
        messagebox.showwarning("Missing fields", "Name and Phone are required.")
        return
    contacts[idx] = {
        "name": name, "phone": phone,
        "email": e_email.get().strip(), "address": e_addr.get().strip()
    }
    save_contacts()
    refresh_table()
    clear_form()


def delete_contact():
    idx = get_selected_idx()
    if idx is None:
        return
    name = contacts[idx]["name"]
    if messagebox.askyesno("Delete", f"Remove '{name}'?"):
        contacts.pop(idx)
        save_contacts()
        refresh_table()
        clear_form()


def on_select(event):
    sel = tree.selection()
    if not sel:
        return
    vals = tree.item(sel[0])["values"]
    for entry, val in zip((e_name, e_phone, e_email, e_addr), vals):
        entry.delete(0, tk.END)
        entry.insert(0, val)


def clear_form():
    for e in (e_name, e_phone, e_email, e_addr):
        e.delete(0, tk.END)
    if tree.selection():
        tree.selection_remove(tree.selection())


def search():
    q = e_search.get().strip().lower()
    if not q:
        refresh_table()
        return
    results = [c for c in contacts if
               q in c["name"].lower() or q in c["phone"] or q in c["email"].lower()]
    refresh_table(results)
    if not results:
        messagebox.showinfo("No results", f"No contacts found for \"{q}\".")


def make_btn(parent, text, bg, hover_bg, cmd):
    f = tk.Frame(parent, bg=bg, cursor="hand2")
    lbl = tk.Label(f, text=text, font=("Helvetica", 11, "bold"),
                   bg=bg, fg="white", padx=16, pady=6)
    lbl.pack()
    for w in (f, lbl):
        w.bind("<Enter>", lambda e, b=hover_bg: [f.config(bg=b), lbl.config(bg=b)])
        w.bind("<Leave>", lambda e, b=bg: [f.config(bg=b), lbl.config(bg=b)])
        w.bind("<Button-1>", lambda e: cmd())
    return f


# ── window ──────────────────────────────────────────────────────
root = tk.Tk()
root.title("Contact Book")
root.geometry("800x600")
root.resizable(False, False)
root.configure(bg=BG)

contacts = load_contacts()

# header
header = tk.Frame(root, bg=HEADER_BG, height=60)
header.pack(fill=tk.X)
header.pack_propagate(False)
tk.Label(header, text="Contact Book", font=("Georgia", 17, "bold"),
         bg=HEADER_BG, fg="white").pack(expand=True)

# search row
search_row = tk.Frame(root, bg=BG)
search_row.pack(fill=tk.X, padx=16, pady=10)

e_search = tk.Entry(search_row, font=("Helvetica", 12), width=30,
                    bd=0, highlightthickness=2,
                    highlightbackground=BORDER, highlightcolor=ACCENT,
                    fg=TEXT, bg=CARD, insertbackground=TEXT)
e_search.pack(side=tk.LEFT, ipady=6, padx=(0, 6))
e_search.bind("<Return>", lambda e: search())

make_btn(search_row, "Search", ACCENT, "#2563eb", search).pack(side=tk.LEFT, padx=3)
make_btn(search_row, "Show All", GRAY, "#4b5563",
         lambda: [e_search.delete(0, tk.END), refresh_table()]).pack(side=tk.LEFT, padx=3)

# treeview with ttk style override
style = ttk.Style()
style.theme_use("default")  # "default" renders consistently cross-platform

style.configure("Custom.Treeview",
                background=CARD,
                foreground=TEXT,
                fieldbackground=CARD,
                rowheight=28,
                font=("Helvetica", 11))
style.configure("Custom.Treeview.Heading",
                background=HEADER_BG,
                foreground="white",
                font=("Helvetica", 11, "bold"),
                relief="flat")
style.map("Custom.Treeview",
          background=[("selected", ACCENT)],
          foreground=[("selected", "white")])
style.map("Custom.Treeview.Heading",
          background=[("active", "#2d3f5e")])

tree_frame = tk.Frame(root, bg=BG)
tree_frame.pack(fill=tk.BOTH, padx=16, pady=(0, 8))

cols = ("Name", "Phone", "Email", "Address")
tree = ttk.Treeview(tree_frame, columns=cols, show="headings",
                    height=10, style="Custom.Treeview")

tree.tag_configure("even", background="#f8fafc")
tree.tag_configure("odd", background=CARD)

for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=180 if col != "Address" else 160, anchor="w")

vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=vsb.set)
vsb.pack(side=tk.RIGHT, fill=tk.Y)
tree.pack(fill=tk.BOTH)
tree.bind("<<TreeviewSelect>>", on_select)

# form
form = tk.LabelFrame(root, text="  Contact Details  ", font=("Helvetica", 10),
                     bg=BG, fg=MUTED, padx=14, pady=10, bd=1, relief="groove")
form.pack(fill=tk.X, padx=16, pady=(0, 8))

entry_style = dict(font=("Helvetica", 11), width=26, bd=0,
                   highlightthickness=2, highlightbackground=BORDER,
                   highlightcolor=ACCENT, fg=TEXT, bg=CARD, insertbackground=TEXT)

labels = ["Name *", "Phone *", "Email", "Address"]
entries = []
for i, lbl_txt in enumerate(labels):
    r, c = divmod(i, 2)
    tk.Label(form, text=lbl_txt, font=("Helvetica", 11),
             bg=BG, fg=TEXT, anchor="e", width=9).grid(row=r, column=c * 2,
                                                        padx=(8, 4), pady=5, sticky="e")
    e = tk.Entry(form, **entry_style)
    e.grid(row=r, column=c * 2 + 1, ipady=5, padx=(0, 18), pady=5)
    entries.append(e)

e_name, e_phone, e_email, e_addr = entries

# action buttons
btn_row = tk.Frame(root, bg=BG)
btn_row.pack(pady=(0, 10))

make_btn(btn_row, "Add", GREEN, "#15803d", add_contact).grid(row=0, column=0, padx=6)
make_btn(btn_row, "Update", ORANGE, "#b45309", update_contact).grid(row=0, column=1, padx=6)
make_btn(btn_row, "Delete", RED, "#b91c1c", delete_contact).grid(row=0, column=2, padx=6)
make_btn(btn_row, "Clear Form", GRAY, "#4b5563", clear_form).grid(row=0, column=3, padx=6)

tk.Label(root, text="* required fields", font=("Helvetica", 9),
         bg=BG, fg=MUTED).pack()

refresh_table()
root.mainloop()