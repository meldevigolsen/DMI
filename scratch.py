class A:
    def __init__(self):
        self.__a = 1

    @property
    def a(self):
        return self.__a


class B(A):
    pass


b = B()

print(b.a)
