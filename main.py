import json


class Client:
    def __init__(self, name, salary=0, log=[], next=None):
        self.name = name
        self.salary = salary
        self.next = next
        self._log = log  # A queue of last 3 operation

    def withdrawal(self, amount):
        if self.salary >= amount:
            self.salary = self.salary - amount
            print(f"{amount}EGP withdrawn successfully")
            self.add_to_log(f"{amount}EGP Withdrawn from your balance")
        else:
            print("The requested amount exceeds your salary.")

    def deposit(self, amount):
        self.salary += amount
        print(f"{amount}EGP deposited successfully")
        self.add_to_log(f"{amount}EGP deposited from your balance")

    def balance_inquiry(self):
        print(f"Your salary is {self.salary}EGP")

    def add_to_log(self, data):
        if len(self._log) > 2:
            self._log.pop(0)
        self._log.append(data)

    def print_log(self):
        if len(self._log) == 0:
            print("No transaction made on salary")
        else:
            for transaction in self._log:
                print(transaction)


class BankSystem:
    # linked list
    def __init__(self):
        self.head = None

    def print(self):
        if self.head is None:
            print("No currently clients!")
            return
        itr: Client = self.head
        displayed_text = ''
        count = 1
        while itr:
            displayed_text += str(count) + '- ' + itr.name + f"   {itr.salary}EGP" + '\n'
            itr = itr.next
            count += 1
        print(displayed_text)

    def get_length(self):
        count = 0
        itr = self.head
        while itr:
            count += 1
            itr = itr.next

        return count

    def insert_at_begining(self, name, salary=0, log=[]):
        client = Client(name, salary, log, self.head)
        self.head = client

    def insert_at_end(self, name, salary=0, log=[]):
        if self.head is None:
            self.head = Client(name, salary, log, None)
            return

        itr = self.head

        while itr.next:
            itr = itr.next

        itr.next = Client(name, salary, None)

    def insert_at(self, index, name, salary=0, log=[]):
        if index < 0 or index > self.get_length():
            raise Exception("Invalid Index")

        if index == 0:
            self.insert_at_begining(name, salary, log)
            return

        count = 0
        itr = self.head
        while itr:
            if count == index - 1:
                client = Client(name, salary, itr.next)
                itr.next = client
                break

            itr = itr.next
            count += 1

    def remove_at(self, index):
        if index < 0 or index >= self.get_length():
            raise Exception("Invalid Index")

        if index == 0:
            self.head = self.head.next
            return

        count = 0
        itr = self.head
        while itr:
            if count == index - 1:
                itr.next = itr.next.next
                break

            itr = itr.next
            count += 1

    def insert_values(self, data_list):
        self.head = None
        for name, salary, log in data_list:
            self.insert_at_end(name, salary)

    def save(self):
        if self.head is None:
            print("No data to be saved!")
            return
        itr: Client = self.head
        json_opject = []
        while itr:
            json_opject.append((itr.name, itr.salary, itr._log))
            itr = itr.next
        print(json_opject)

        with open("data.json", "w") as file:
            json.dump(json_opject, file)

    def load_from_json(self):
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
                self.insert_values(data_list=data)

        except:
            pass


li = BankSystem()
li.load_from_json()
# li.insert_values([("ahmed", 300), ("mohamed", 400), ("ali", 500)])
# li.insert_at_end("marawan", 600)
# li.insert_at_begining("rami", 10000)
# li.insert_at(2, "khaled", 700)
# li.remove_at(4)
# li.save()
li.print()
