class Parent:
    def __init__(self, txt=None):
        self.txt = txt

    def printmessage(self):
        print(self.txt)
        return "Hello!"


class Child(Parent):
    def __init__(self, txt):
        super().__init__(txt)
        self.txt = txt

    def message1(self):
        print(self.txt)


class C2(Child):
    def __init__(self, txt):
        super().__init__(txt)
        self.txt = txt

    def gmes(self):
        print(self.txt)
        self.message1()
        self.m = self.printmessage()
        print(self.m)


# x = Parent("Hi")
# x.printmessage()

# y = Child("Hello Child")
# y.message1()
# y.printmessage()

z = C2("Hello Grand Child")
z.gmes()
