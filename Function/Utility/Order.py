import datetime
import json
import os
ORDER_DATA = None

class Order:
    def __init__(self, date:datetime.date,name:str,content:dict, phone_num:str ) -> None:
        self.date = date
        self.name = name
        self.content = content
        self.phone_num = phone_num
        
    def update(self, date:datetime.date,name:str,content:dict, phone_num:str):
        self.date = date
        self.name = name
        self.content = content
        self.phone_num = phone_num
        
    def __str__(self) -> str:
        res = ""
        res += f"名字:{self.name}\n"
        res += f"電話:{self.phone_num}\n"
        res += f"日期:{self.date}\n"
        for key, val in self.content.items():
           res += f"{key}:{val}\n"
        return res

#======================== Add ========================

def addNewOrder(order:Order):
    ORDER_DATA.append(order)

#======================== Update(Edit) ========================

def updateOrder(modified_object, object_id):
    ORDER_DATA[object_id] = modified_object

def getOrder(num:int):
    return ORDER_DATA[num]

#======================== Search ========================

def searchTargetOrder(content_buffer:Order):
    target_list = []
    target_index_list = []
    for idx, order in enumerate(ORDER_DATA):
        # name condition
        if content_buffer.name == "":
            name_match = True
        else:    
            name_match = content_buffer.name in order.name
        # phone_nu condition
        if content_buffer.phone_num == "":
            phone_num_match = True
        else:    
            phone_num_match = content_buffer.phone_num == order.phone_num
        # date condition
        if content_buffer.date == "":
            date_match = True
        else: 
            date_match = content_buffer.date == order.date
        # content condition
        if content_buffer.content == {}:
            content_match = True
        else:# each content must match to those in order 
            content_match = False
            for key, val in content_buffer.content.items():
                for content_name in order.content.keys():
                    if key in content_name:
                        content_match = True
                if content_match == False:
                    break
                else:
                    # check value
                    if val != 0 and order.content[key] != val:
                        content_match = False
                        break
                    else:
                        content_match = True
        total_condition = name_match and phone_num_match and date_match and content_match
        if total_condition == True:
            target_list.append(order)
            target_index_list.append(idx)
    return target_list,target_index_list

#======================== Sum up ========================

def sumUpOrders(start_date:datetime.date, end_date:datetime.date):
    total_content = {}
    for order in ORDER_DATA:
        if order.date >= start_date and order.date <= end_date:
            # summing up the content
            for key, val in order.content.items():
                UpdateDictionary(total_content, key, val)
    result = sorted(list(zip(total_content.keys(),total_content.values())),key=lambda x: x[0])
    result_message = ""
    for x in result:
        result_message += f"{x[0]}:{x[1]:02d}\n"
    return result_message

#======================== Other Funtion ========================

def UpdateDictionary(dictionary:dict,key:str,value:str):
    try:
        dictionary[key] += int(value)
    except:
        dictionary[key] = int(value)
    return dictionary

#======================== File Operation ========================

def order2JSON(order):
    res = {}
    res["name"] = order.name
    res["phone_num"] = order.phone_num
    res["date"] = order.date.isoformat()
    res["content"] = order.content
    return res

def JSON2Order(order):
    name = order["name"]
    phone_num = order["phone_num"]
    date = datetime.date.fromisoformat(order["date"])
    content = order["content"]
    return Order(date, name, content, phone_num)

def savingOrder():
    print(os.getcwd())
    try:
        res = []
        for order in ORDER_DATA:
            res.append(order2JSON(order))
        with open("OrderData","w",encoding="UTF-8") as file:
            json.dump(res,file,ensure_ascii=False, indent=2)
        return "儲存完畢"
    except:
        return "發生意外"
    
def readOrderData():
    global ORDER_DATA
    ORDER_DATA = []
    print(os.getcwd())
    os.chdir("./Function/Utility")
    print(os.getcwd())
    with open("OrderData","r",encoding="UTF-8") as file:
        res = json.load(file)
    for x in res:
        ORDER_DATA.append(JSON2Order(x))