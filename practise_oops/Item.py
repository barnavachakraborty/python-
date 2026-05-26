import csv

class Item:
    
    rate = 0.8
    all = []
    def __init__(self, name:str, price:float, quantity = 0):
        
        assert price >= 0 , f"Price : {price} is not an acceptable price"
        assert quantity >= 0 , f"Quantity : {quantity} is not an acceptable price"        
        
        self.__name = name
        self.price = price
        self.quantity = quantity
        
        Item.all.append(self)
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self,name)->bool:
        if(name == ''): 
            return False
        else:
            self.__name = name
            return True
    
    def apply_offer(self):
        self.price = self.price*Item.rate
    
    def total_cost(self):
        return self.quantity*self.price
    
    def print_attr(self):
        print(
            f"obg:{self.__dict__}\n"
            f"cls:\n"+
            "\n".join(f"{key}:{val}" for key,val in Item.__dict__.items()) 
        )
    @classmethod
    def instantiate_objs(cls):
        with open("Items.csv","r") as f:
            data = csv.DictReader(f)
            data_list = list(data)
        for items in data_list:
            Item(
                name = items["name"],
                price = float(items["price"]),
                quantity = int(items["quantity"])
            )
    def __repr__(self):
        return f"Item('{self.name}',{self.price},{self.quantity})"
   