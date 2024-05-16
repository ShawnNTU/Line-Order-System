from .Utility import UtilFunction
from .Utility import Order
from .Utility.ReplyMessage import FORMAT_ERROR, SELECTION_MESSAGE
from .Utility.ReplyMessage import ORDER_FORMAT_MESSAGE, GUARANTEEING_MESSAGE, YES, NO, MODIFY_INSTRUCTION

CURRENT_SEARCHING_STATE = "BEGIN"
content_buffer = None

def searchngOrderMainFunction(message):
    global CURRENT_SEARCHING_STATE, content_buffer
    BACK_TO_SELECTION_MODE = False
    try:
        UtilFunction.leavingChecking(message)
        
        if CURRENT_SEARCHING_STATE == "BEGIN":
            reply_message = MODIFY_INSTRUCTION + ORDER_FORMAT_MESSAGE
            CURRENT_SEARCHING_STATE = "ASKING"
        elif CURRENT_SEARCHING_STATE == "ASKING":
            content_buffer = UtilFunction.parseText2Object(message)
            reply_message = message + "\n" + GUARANTEEING_MESSAGE
            CURRENT_SEARCHING_STATE = "WAITING"
            
        elif CURRENT_SEARCHING_STATE == "WAITING":
            UtilFunction.yesOrNoChecking(message)
            if message == NO:
                search_result = Order.searchTargetOrder(content_buffer)
                reply_message = UtilFunction.parseSearchResult(search_result)
                reply_message += "\n"
                reply_message += SELECTION_MESSAGE
                BACK_TO_SELECTION_MODE = True
                initializeParameter()
            elif message == YES:
                CURRENT_SEARCHING_STATE = "ASKING"
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
    global CURRENT_SEARCHING_STATE
    global content_buffer
    
    content_buffer = None
    CURRENT_SEARCHING_STATE = "BEGIN"
    
def searchingProcess():
    global content_buffer
    
