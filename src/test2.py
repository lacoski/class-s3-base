class test(object):
    def __testmethod(self):
        print('test method')
    def pbmethods(self):
        self.__testmethod()

obj = test()
obj.pbmethods()