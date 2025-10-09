class Test:
    def method(self):
        print("This is a test method")


a = Test()
a.method = lambda: print("This is a replaced method")
a.method()