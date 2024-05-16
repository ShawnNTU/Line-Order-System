import datetime
from . import Order
from .ReplyMessage import YES, NO

def parseDate(message:str):
    if message == "":
        return message
    try:
        content = message.strip().split("-")
        if len(content) == 2:
            year = 2024
            month, date = content
        else:
            year, month, date = content
        
        return datetime.date(int(year), int(month), int(date))
    except Exception:
        raise Exception("時間格式不對(格式:2024-1-1)")

def parseInputNumber(message:str):
    try:
        num = int(message)
        return num
    except:
        raise Exception("數字格式不對")

def UpdateDictionary(dictionary:dict,key:str,value:str):
    try:
        value = int(value)
    except:
        raise Exception("數值格式不對")
    try:
        dictionary[key] += int(value)
    except KeyError:
        dictionary[key] = int(value)
    return dictionary

def parseObject2Text(object:Order.Order):
    res = f"訂購者姓名:\n{object.name}\n訂購者電話:\n{object.phone_num}\n訂購日期:\n{object.date}\n訂購內容(有其他多的請換行):\n"
    for key, val in object.content.items():
       res += f"{key} {val}\n" 
    return res


def leavingChecking(message:str):
    if message == "離開":
        raise Exception("Leaving")

def yesOrNoChecking(message:str):
    if message != YES and message != NO:
        raise Exception(f"請輸入{YES}或{NO}")


def newOrderContentChecking(order:Order.Order):
    if order.name == "":
        raise Exception("要有名字")
    content = order.content
    if content == {}:
        raise Exception("要有內容")
    for key, val in content.items():
        if val == 0:
            raise Exception(f"{key}量不可為 0")

def formatChecking(lines:list):
    try: 
        if lines[0] != "訂購者姓名:":
            raise Exception("「訂購者姓名:」要在第一行")
        if lines[2] != "訂購者電話:":
            raise Exception("「訂購者電話:」要在第三行")
        if lines[4] != "訂購日期:":
            raise Exception("「訂購日期:」要在第五行")
        if lines[6] != "訂購內容(有其他多的請換行):":
            raise Exception("「訂購內容(有其他多的請換行):」要在第七行")
        for line in lines[7:]:
            content = line.strip().split(" ")
            if len(content) > 2:
                raise Exception("內容格式不對")
        return 0,"Good"
    except Exception as e:
        raise e

def parseText2Object(text:str):
    lines = text.strip().split("\n")
    try:
        formatChecking(lines)
        name = lines[1]
        phone_num = lines[3]
        date = parseDate(lines[5])
        content = {}
        for line in lines[7:]:
            each_content = line.strip().split(" ")
            if len(each_content) == 2:
                key, val = each_content
                val = int(val)
            elif len(each_content) == 1:
                key = each_content[0]
                val = 0
            UpdateDictionary(content, key, val)
        return Order.Order(date, name, content, phone_num)
    except Exception as e:
        raise e


def parseSearchResult(search_result):
    result_message = ""
    target_list,target_index_list = search_result 
    if target_list == []:
        return "沒有符合的訂單\n"
    total = {}
    for idx, object in enumerate(target_list):
        result_message += f"訂單搜尋編號:{target_index_list[idx]}\n"
        result_message += f"名字:{object.name}\n"
        result_message += f"電話:{object.phone_num}\n"
        result_message += f"日期:{object.date}\n"
        for key, val in object.content.items():
            result_message += f"{key}:{val}\n"
            UpdateDictionary(total,key,val)
        result_message += "\n"
    result_message += "總共統計：\n"
    result_message += dictToString(total)
    result_message += "\n"
    return result_message

def dictToString(obj:dict):
    res = ""
    for key, val in obj.items():
        res += f"{key}:{val}\n"
    return res