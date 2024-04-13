class Client:

    def __init__(self, name, salary=0, next=None):
        self.name = name
        self.salary = salary
        self.next = next

    def withdrawal(self, amount):
        if self.salary >= amount:
            self.salary = self.salary = amount
            print(f"{amount}EGP withdrawn successfully")
        else:
            print("The requested amount exceeds your salary.")

    def deposit(self, amount):
        self.salary += deposit
        print(f"{amount}EGP deposited successfully")

    def balance_inquiry(self):
        print(f"Your salary is {self.salary}EGP")


class BankSystem:
    # linked list
    def __init__(self):
        self.head = None

    # ///////////////////////////////////////////////////////////
    # /////////////////////////////////////////////////////////

    def print(self):
        if self.head is None:
            print("No currently clients!")
            return
        itr = self.head
        displayed_text = ''
        count = 1
        while itr:
            displayed_text += str(count) + '- ' + itr.name
            itr = itr.next
        print(displayed_text)

    # ///////////////////////////////////////////////////////////
    # /////////////////////////////////////////////////////////

    def get_length(self):
        count = 0
        itr = self.head
        while itr:
            count += 1
            itr = itr.next

        return count

    # ///////////////////////////////////////////////////////////
    # /////////////////////////////////////////////////////////

    def insert_at_begining(self, name, salary=0):
        client = Client(name, salary, self.head)
        self.head = client

    # ///////////////////////////////////////////////////////////
    # /////////////////////////////////////////////////////////

    def insert_at_end(self, data):
        if self.head is None:
            self.head = Node(data, None)
            return

        itr = self.head

        while itr.next:
            itr = itr.next

        itr.next = Node(data, None)

    # ///////////////////////////////////////////////////////////
    # /////////////////////////////////////////////////////////

    def insert_at(self, index, data):
        if index < 0 or index > self.get_length():
            raise Exception("Invalid Index")

        if index == 0:
            self.insert_at_begining(data)
            return

        count = 0
        itr = self.head
        while itr:
            if count == index - 1:
                node = Node(data, itr.next)
                itr.next = node
                break

            itr = itr.next
            count += 1

    # ///////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////////
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

    # ///////////////////////////////////////////////////////////
    # /////////////////////////////////////////////////////////

    def insert_values(self, data_list):
        self.head = None
        for data in data_list:
            self.insert_at_end(data)


li = BankSystem()
# li.insert_values([33, 44, 55])
# li.insert_at_end(99999)
li.insert_at_begining("ahmed", 10000)
# li.insert_at(2, 77777)
# li.remove_at(4)
li.print()


# print(c1.id)
# print(c2.id)
