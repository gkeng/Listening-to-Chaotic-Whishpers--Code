import pickle


class Action(object):

    """
    Class that models a stock (action in French)
    """

    def __init__(self, name, path_dic):

        """
        Constructor of stock
        :param name: name of the stock
        :param path_dic: file path to the pickle of the stock
        """

        self.__setattr__('name', name)
        self.stock = {}
        with open(path_dic, 'rb') as handle:
            dico_stock = pickle.load(handle)
        for i, j in enumerate(dico_stock):
            if (i > 699) and (i < 1095):
                self.stock[str(j)] = dico_stock[str(j)]
        self.__setattr__('buy_value', 0)
        self.__setattr__('amount', 0)
        self.__setattr__('date', "0700")

    def __str__(self):

        """
        Métthode d'affichage de l'objet
        """

        return "name :  {}; buy_value {}; amount {}".format(
            self.name, self.buy_value, self.amount)

    def get_stock_value(self, day):

        """
        Returns the stock price of the day
        :param day: day number, integer
        :return: stock price
        """

        if (day >= 700) and (day < 1095):
            day = str(day).zfill(4)
        else:
            print("Errror key value, enter a value between 700 to 1094")
            return -100
        return self.stock[day]

    def set_date(self, date):
        if len(str(date)) == 4:
            date = str(date)
            self.__setattr__('date', date)
        else:
            print("A date is a str of size 4")


if __name__ == '__main__':

    action = Action("3M", '/Users/rugerypierrick/ZenIvest/pickle/3M .pkl')
    print(action.__str__())
    name = action.__getattribute__('name')
    print(name)
    print(action.get_stock_value(700))
    action.__setattr__('amount', 1000)
    print(action.__getattribute__('amount'))
    print(action.__getattribute__('date'))
