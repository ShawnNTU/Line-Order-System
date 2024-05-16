from .Utility import UtilFunction
from .Utility import Order
from .Utility.ReplyMessage import FORMAT_ERROR, SELECTION_MESSAGE
from .Utility.ReplyMessage import ORDER_FORMAT_MESSAGE, GUARANTEEING_MESSAGE, YES, NO, MODIFY_INSTRUCTION

CURRENT_ADDING_STATE = "BEGIN"
content_buffer = None

def addingOrderMainFunction(message:str):
    global CURRENT_ADDING_STATE, content_buffer
    BACK_TO_SELECTION_MODE = False
    try:
        UtilFunction.leavingChecking(message)
        
        if CURRENT_ADDING_STATE == "BEGIN":
            reply_message = MODIFY_INSTRUCTION + ORDER_FORMAT_MESSAGE
            CURRENT_ADDING_STATE = "ASKING"
        elif CURRENT_ADDING_STATE == "ASKING":
            
            content_buffer = UtilFunction.parseText2Object(message)
            UtilFunction.newOrderContentChecking(content_buffer)
            reply_message = str(content_buffer) + "\n" + GUARANTEEING_MESSAGE
            CURRENT_ADDING_STATE = "WAITING"
                
        elif CURRENT_ADDING_STATE == "WAITING":
            UtilFunction.yesOrNoChecking(message)
            if message == NO:
                UtilFunction.Order.addNewOrder(content_buffer)
                reply_message = SELECTION_MESSAGE
                initializeParameter()
                BACK_TO_SELECTION_MODE = True
            elif message == YES:
                CURRENT_ADDING_STATE = "ASKING"
                reply_message = MODIFY_INSTRUCTION

    except Exception as e:
        if str(e) == "Leaving":
            reply_message = SELECTION_MESSAGE
            initializeParameter()
            BACK_TO_SELECTION_MODE = True
        else:
            reply_message = f"{FORMAT_ERROR}\n{e}"
    return reply_message, BACK_TO_SELECTION_MODE

def initializeParameter():
    global CURRENT_ADDING_STATE
    global content_buffer
    
    content_buffer = None
    CURRENT_ADDING_STATE = "BEGIN"
