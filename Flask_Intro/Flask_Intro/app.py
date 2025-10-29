from flask import Flask, render_template, request

app = Flask(__name__)

# =====================================================
# LINKED LIST LOGIC
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

    def add(self, data: str):
        node = Node(data)
        if not self.head:
            self.head = node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node

    def remove_beginning(self):
        if not self.head:
            return None
        removed = self.head.data
        self.head = self.head.next
        return removed

    def remove_at_end(self):
        if not self.head:
            return None
        if not self.head.next:
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
        if not self.head:
            return None
        if self.head.data == data:
            removed = self.head.data
            self.head = self.head.next
            return removed
        current = self.head
        while current.next and current.next.data != data:
            current = current.next
        if not current.next:
            return None
        removed = current.next.data
        current.next = current.next.next
        return removed


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


sushi_steps = setup_sample_steps()

# =====================================================
# STACK + INFIX → POSTFIX LOGIC
# =====================================================
class StackNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class Stack:
    def __init__(self):
        self.top = None

    def push(self, data):
        new_node = StackNode(data)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        if not self.top:
            return None
        popped = self.top.data
        self.top = self.top.next
        return popped

    def peek(self):
        return self.top.data if self.top else None

    def is_empty(self):
        return self.top is None


def precedence(op):
    return {'^': 3, '*': 2, '/': 2, '+': 1, '-': 1}.get(op, 0)


def is_left_associative(op):
    return op in ('+', '-', '*', '/')


def infix_to_postfix(expression):
    stack = Stack()
    output = []

    for char in expression:
        if char == ' ':
            continue
        elif char.isalnum():
            output.append(char)
        elif char == '(':
            stack.push(char)
        elif char == ')':
            while not stack.is_empty() and stack.peek() != '(':
                output.append(stack.pop())
            stack.pop()
        else:  # operator
            while (not stack.is_empty() and
                   (precedence(stack.peek()) > precedence(char) or
                    (precedence(stack.peek()) == precedence(char) and is_left_associative(char))) and
                   stack.peek() != '('):
                output.append(stack.pop())
            stack.push(char)

    while not stack.is_empty():
        output.append(stack.pop())

    return ' '.join(output)

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
    result = ''
    active_tab = 'uppercase'  # default tab

    if request.method == 'POST':
        form = request.form
        active_tab = form.get('active_tab', 'uppercase')

        # ---------- UPPERCASE ----------
        if 'text' in form:
            uppercase_result = form.get('text', '').upper()
            active_tab = 'uppercase'

        # ---------- CIRCLE AREA ----------
        elif 'radius' in form:
            try:
                r = float(form.get('radius'))
                circle_area = round(3.1416 * r * r, 2)
            except ValueError:
                circle_area = 'Invalid input.'
            active_tab = 'circle'

        # ---------- TRIANGLE AREA ----------
        elif 'base' in form and 'height' in form:
            try:
                b = float(form.get('base'))
                h = float(form.get('height'))
                triangle_area = round(0.5 * b * h, 2)
            except ValueError:
                triangle_area = 'Invalid input.'
            active_tab = 'triangle'

        # ---------- LINKED LIST ----------
        elif 'action' in form:
            action = form.get('action')
            data = form.get('data', '').strip()
            active_tab = 'linkedlist'

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

        # ---------- INFIX → POSTFIX ----------
        elif 'expression' in form:
            expr = form.get('expression', '')
            active_tab = 'infix'
            if expr:
                result = infix_to_postfix(expr)

    return render_template(
        'works.html',
        uppercase_result=uppercase_result,
        circle_area=circle_area,
        triangle_area=triangle_area,
        linked_list_items=sushi_steps.display(),
        ll_message=ll_message,
        result=result,
        active_tab=active_tab
    )

# =====================================================
# MAIN
# =====================================================
if __name__ == '__main__':
    app.run(debug=True)