from flask import Flask, render_template, request

app = Flask(__name__)

# =====================================================
# LINKED LIST LOGIC (your full working version below)
# =====================================================
class Node:
    def __init__(self, data: str):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def display(self):
        current = self.head
        steps = []
        while current:
            steps.append(current.data)
            current = current.next
        return steps

    def remove_beginning(self):
        if self.head is None:
            return None
        removed_data = self.head.data
        self.head = self.head.next
        return removed_data

    def remove_at_end(self):
        if self.head is None:
            return None
        if self.head.next is None:
            removed = self.head.data
            self.head = None
            return removed
        current = self.head
        while current.next.next:
            current = current.next
        removed = current.next.data
        current.next = None
        return removed

    def remove_at(self, data: str):
        if self.head is None:
            return None
        if self.head.data == data:
            removed = self.head.data
            self.head = self.head.next
            return removed
        current = self.head
        while current.next and current.next.data != data:
            current = current.next
        if current.next is None:
            return None
        removed = current.next.data
        current.next = current.next.next
        return removed

    def add(self, data: str):
        node = Node(data)
        if self.head is None:
            self.head = node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = node


def setup_sample_steps():
    L = LinkedList()
    for step in ["A. Prepare", "B. Cook rice", "C. Place on mat", "D. Roll", "E. Eat"]:
        L.add(step)
    return L


def normalize_step_input(inp: str):
    inp = inp.strip()
    if not inp:
        return ""
    letter = inp.upper()
    if len(letter) == 1 and letter in "ABCDE":
        mapping = {
            "A": "A. Prepare",
            "B": "B. Cook rice",
            "C": "C. Place on mat",
            "D": "D. Roll",
            "E": "E. Eat",
        }
        return mapping[letter]
    return inp


# Global Linked List instance
sushi_steps = setup_sample_steps()

# =====================================================
# ROUTES
# =====================================================

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/works', methods=['GET', 'POST'])
def works():
    global sushi_steps
    uppercase_result = ''
    circle_area = ''
    triangle_area = ''
    ll_message = ''

    if request.method == 'POST':
        form = request.form

        # ---------- UPPERCASE ----------
        if 'text' in form:
            uppercase_result = form.get('text', '').upper()

        # ---------- CIRCLE AREA ----------
        elif 'radius' in form:
            try:
                r = float(form.get('radius'))
                circle_area = round(3.1416 * r * r, 2)
            except ValueError:
                circle_area = 'Invalid input.'

        # ---------- TRIANGLE AREA ----------
        elif 'base' in form and 'height' in form:
            try:
                b = float(form.get('base'))
                h = float(form.get('height'))
                triangle_area = round(0.5 * b * h, 2)
            except ValueError:
                triangle_area = 'Invalid input.'

        # ---------- LINKED LIST ----------
        elif 'action' in form:
            action = form.get('action')
            data = form.get('data', '').strip()

            if action == 'add' and data:
                sushi_steps.add(data)
                ll_message = f"✅ Added: {data}"
            elif action == 'remove_beginning':
                removed = sushi_steps.remove_beginning()
                ll_message = f"🗑️ Removed beginning: {removed}" if removed else "⚠️ List is empty."
            elif action == 'remove_end':
                removed = sushi_steps.remove_at_end()
                ll_message = f"🗑️ Removed end: {removed}" if removed else "⚠️ List is empty."
            elif action == 'remove_at' and data:
                step_name = normalize_step_input(data)
                removed = sushi_steps.remove_at(step_name)
                ll_message = f"🗑️ Removed: {removed}" if removed else f"⚠️ Step '{data}' not found."
            else:
                ll_message = "⚠️ Invalid or missing input."

    return render_template(
        'works.html',
        uppercase_result=uppercase_result,
        circle_area=circle_area,
        triangle_area=triangle_area,
        linked_list_items=sushi_steps.display(),
        ll_message=ll_message
    )

if __name__ == '__main__':
    app.run(debug=True)
