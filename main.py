import json
from datetime import datetime


class Client:
    def __init__(self, name, salary=0, log=[], date=None, next=None):
        self.name = name
        self.salary = salary
        self.next = next
        self.date_created = date if date else datetime.now()
        self._log = log  # A queue of last 3 operation

    def withdrawal(self, amount):
        if amount <= 0:
            print("Please, enter a positive value")
            return
        if self.salary >= amount:
            self.salary = self.salary - amount
            print(f"{amount}EGP withdrawn successfully")
            self.add_to_log(f"{amount}EGP Withdrawn from your balance")
        else:
            print("The requested amount exceeds your salary.")

    def deposit(self, amount):
        if amount <= 0:
            print("Please, enter a positive value")
            return
        self.salary += amount
        print(f"{amount}EGP deposited successfully")
        self.add_to_log(f"{amount}EGP deposited from your balance")

    def balance_inquiry(self):
        print(f"{self.name} has {self.salary}EGP")

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

    def __str__(self):
        return self.name + f" ({self.salary}EGP)  " + "Registered at " + self.date_created.strftime("%H:%M %Y-%m-%d")


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
            displayed_text += str(
                count) + '- ' + itr.name + f" ({itr.salary}EGP)  " + "Registered at " + itr.date_created.strftime(
                "%H:%M %Y-%m-%d") + '\n'
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
        client = Client(name, salary, log, next=self.head)
        self.head = client
        print(f"Client {name} has been added successfully")

    def insert_at_end(self, name, salary=0, date=None, log=[]):
        if self.head is None:
            self.head = Client(name=name, salary=salary, date=date, log=log, next=None)
            return

        itr = self.head

        while itr.next:
            itr = itr.next

        itr.next = Client(name=name, salary=salary, log=log, date=date, next=None)
        print(f"Client {name} has been added successfully")

    def insert_at(self, index, name, salary=0, log=[]):
        if index < 0 or index > self.get_length():
            raise Exception("Invalid Index")

        if index == 0:
            self.insert_at_begining(name, salary)
            return

        count = 0
        itr = self.head
        while itr:
            if count == index - 1:
                client = Client(name, salary, next=itr.next)
                print(f"Client {name} has been added successfully")
                itr.next = client
                break

            itr = itr.next
            count += 1

    def remove_at(self, index):
        index = index - 1
        if index < 0 or index >= self.get_length():
            raise Exception("Invalid Index!")

        if index == 0:
            self.head = self.head.next
            return

        count = 0
        itr = self.head
        while itr:
            if count == index - 1:
                itr.next = itr.next.next
                print(f"Client number {index + 1} has been removed successfully")
                break

            itr = itr.next
            count += 1

    def select_at(self, index):
        if self.head is None:
            print("No currently clients!")
            return
        elif index > self.get_length() + 1 or index < 1:
            raise Exception("Invalid Index!")

        count = 0
        itr = self.head
        while itr:
            if count == index - 1:
                print("here")
                return itr

            itr = itr.next
            count += 1
        return None

    def insert_values(self, data_list):
        self.head = None
        for name, salary in data_list:
            self.insert_at_end(name, salary)
        print(f"Clients have been added successfully")

    def insert_json_values(self, data: dict):
        for client in data:
            attrs = data[client]
            date = datetime.fromisoformat(attrs["date_created"])
            self.insert_at_end(name=client,
                               salary=attrs["salary"],
                               log=attrs["log"],
                               date=date)

    # sorting methods
    def odd_even_sort(self, attr):
        if self.head is None:
            return

        """
        match param:
            case 1:
                attr = "name"
            case 2:
                attr = "salary"
            case 3:
                attr = "date_created"
            case _:
                print("Invalid option!")
                return
        """

        sorted = False
        while not sorted:
            sorted = True
            odd = self.head
            even = self.head.next
            while even is not None:
                if getattr(odd, attr) > getattr(even, attr):
                    swap_clients(odd, even)
                    sorted = False
                if even.next is not None:
                    odd = even
                    even = even.next
                else:
                    break
        # print("sorted")

    def to_array(self):
        # adding the clients in an array to perform search accross them
        array = []
        itr = self.head
        while itr:
            array.append(itr)
            itr = itr.next
        return array

    def search_by_name(self, name: str):
        if self.head is None:
            print("No matches!")

        itr = self.head
        while itr:
            if itr.name.lower() == name.lower():
                print(itr)
                return

            itr = itr.next
        print("No matches!")

    def search_by_salary(self, target_salary):
        # performing binary search to get a target salary
        client_array = self.to_array()
        left = 0
        right = len(client_array) - 1
        while left <= right:
            mid = (left + right) // 2
            if client_array[mid].salary == target_salary:
                print(client_array[mid])
                return
            elif client_array[mid].salary < target_salary:
                left = mid + 1
            else:
                right = mid - 1
        print("no matches!")

    def search_by_range(self, min_salary, max_salary):
        # sort clients by salary first
        self.odd_even_sort("salary")

        # perform a binary search to get a range of salaries
        clients_array = self.to_array()
        n = len(clients_array)
        low_index = 0
        high_index = 0

        # get the leftmost search index
        if clients_array[0].salary >= min_salary:
            low_index = 0
        else:
            left = 0
            right = len(clients_array) - 1
            while left <= right:
                mid = (left + right) // 2
                if clients_array[mid - 1].salary < min_salary and clients_array[mid].salary >= min_salary:
                    low_index = mid
                    break
                elif clients_array[mid].salary < min_salary:
                    left = mid + 1
                else:
                    right = mid - 1

        # get the rightmost search index
        if clients_array[n - 1].salary <= max_salary:
            high_index = n - 1
        else:
            left = 0
            right = len(clients_array) - 1
            while left <= right:
                mid = (left + right) // 2
                if clients_array[mid + 1 if mid < 5 else mid].salary >= max_salary and clients_array[
                    mid].salary < max_salary:
                    high_index = mid
                    break
                elif clients_array[mid].salary > max_salary:
                    right = mid - 1
                else:
                    left = mid + 1

        result = clients_array[low_index:high_index + 1]
        if result:
            for client in result:
                print(client)
        else:
            print("No salaries found within this range!")

    def save(self):
        # sort entities by date before saving them in a json file
        self.odd_even_sort("date_created")
        if self.head is None:
            print("No data to be saved!")
            return
        itr: Client = self.head
        json_opject = {}
        while itr:
            json_opject[itr.name] = {"salary": itr.salary,
                                     "log": itr._log,
                                     "date_created": itr.date_created.isoformat()}
            itr = itr.next
        # print(json_opject)

        with open("data.json", "w") as file:
            json.dump(json_opject, file)

    def load_from_json(self):
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
                self.insert_json_values(data)

        except:
            print("Data file has been corrupted!")
            pass


def swap_clients(c1: Client, c2: Client):
    c1.name, c2.name = c2.name, c1.name
    c1.salary, c2.salary = c2.salary, c1.salary
    c1._log, c2._log = c2._log, c1._log
    c1.date_created, c2.date_created = c2.date_created, c1.date_created


# li = BankSystem()
# li.load_from_json()
# li.insert_values([("ahmed", 300), ("mohamed", 400), ("ali", 500)])
# li.insert_at_end("marawan", 600)
# li.insert_at_begining("rami", 10000)
# li.insert_at(2, "khaled", 700)
# li.remove_at(4)
# li.save()

# print("before sorting")
# li.print()
# li.odd_even_sort(2)
# print("after sorting")
# li.print()
# li.search_by_range(401, 400)
# li.search_by_name("AHmsed")
# for i in li.search_by_range(400, 30000):
#     print(i)

if __name__ == "__main__":
    print("Welcome to Bank Management System:")
    bank = BankSystem()
    while True:
        print("\t1- Add Client\n"
              "\t2- Remove Client\n"
              "\t3- Display All Clients\n"
              "\t4- Sort Clients\n"
              "\t5- Search On Client\n"
              "\t6- Select Client\n"
              "\t7- Save Data\n"
              "\t8- Load Saved Data\n"
              "\t9- Exit\n")
        option = input("Enter option number: ")

        match option:
            case "1":  # add client
                name = input("Client's name: ")
                salary = input("Client's initial salary (leave it blank to set 0EGP): ")
                bank.insert_at_end(name=name,
                                   salary=int(salary) if salary else 0)

            case "2":  # remove client
                bank.print()
                c = int(input("Enter client number to remove: "))
                bank.remove_at(c)

            case "3":  # display all
                bank.print()

            case "4":  # sort clients
                while True:
                    s = int(input("Sort by:\n"
                                  "\t1- Name\n"
                                  "\t2- Balance\n"
                                  "\t3- Date Created\n"
                                  "\nEnter option number: "))

                    match s:
                        case 1:
                            bank.odd_even_sort("name")
                            print("Clients sorted ascendingly according to name")
                            break
                        case 2:
                            bank.odd_even_sort("salary")
                            print("Clients sorted ascendingly according to balance")
                            break
                        case 3:
                            bank.odd_even_sort("date_created")
                            print("Clients sorted ascendingly according to date created")
                            break
                        case _:
                            print("Invalid option!")

            case "5":  # search on client
                while True:
                    s = int(input("Sort by:\n"
                                  "\t1- Name\n"
                                  "\t2- Salary\n"
                                  "\t3- Range of salaries\n"
                                  "\t4- Return to main menu\n"
                                  "\nEnter option number: "))

                    match s:
                        case 1:
                            name = input("Enter client's name: ")
                            bank.search_by_name(name)
                            break
                        case 2:
                            salary = int(input("Enter client's salary: "))
                            client = bank.search_by_salary(salary)
                            break
                        case 3:
                            min = int(input("Minimum salary: "))
                            max = int(input("Maximum salary: "))
                            bank.search_by_range(min, max)
                            break
                        case 4:
                            break
                        case _:
                            print("Invalid option!")

            case "6":  # select client
                if bank.get_length() == 0:
                    print("No currently clients!")
                else:
                    bank.print()
                    i = int(input("\nEnter client number: "))
                    client: Client = bank.select_at(i)
                    print(f"Client {client.name} has been selected")
                    while True:
                        print(f"{client.name}'s account:\n"
                              f"\t1- Withdrawal\n"
                              f"\t2- Deposit\n"
                              f"\t3- Balance Inquiry\n"
                              f"\t4- Log Activity\n"
                              f"\t5- Return to main menu\n")
                        o = int(input("Enter option number: "))
                        match o:
                            case 1:
                                w = int(input("Enter the amount: "))
                                client.withdrawal(w)
                            case 2:
                                d = int(input("Enter the amount: "))
                                client.deposit(d)
                            case 3:
                                client.balance_inquiry()
                            case 4:
                                client.print_log()
                            case 5:
                                break
                            case _:
                                print("Invalid option!")

                        print("\n" + "_" * 30 + "\n")

            case "7":  # save data
                print("Saving current changes to data.json ..")
                bank.save()
                print("Data Saved Successfully")

            case "8":  # load saved data
                print("Loading data from data.json ..")
                bank.load_from_json()
                print("Data loaded successfully")
                bank.print()

            case "9":  # exit
                while True:
                    e = input("Save data before exit (y/n)? ").lower()
                    if e == "y":
                        bank.save()
                        print("Data Saved Successfully\nExiting ..")
                        exit()
                    elif e == "n":
                        print("Exiting ..")
                        exit()
                    else:
                        print("Invalid input!")
            case _:
                print("Invalid option, please enter a value between 1 to 7")

        print("\n" + "_" * 60 + "\n")
