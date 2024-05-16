from .Utility import UtilFunction
from .Utility import Order
from .Utility.ReplyMessage import FORMAT_ERROR, SELECTION_MESSAGE, EDIT_SUCCESS_MESSAGE
from .Utility.ReplyMessage import ASKING_ORDER_NUMBER,GUARANTEEING_MESSAGE, MODIFY_INSTRUCTION, YES, NO

CURRENT_EDITING_STATE = "BEGIN"
content_buffer = None
target_num = None

def editingOrderMainFunction(message:str):
    global CURRENT_EDITING_STATE, content_buffer,target_num
    BACK_TO_SELECTION_MODE = False
    
    try:
        UtilFunction.leavingChecking(message)
        
        if CURRENT_EDITING_STATE == "BEGIN":
            reply_message = ASKING_ORDER_NUMBER
            CURRENT_EDITING_STATE = "ASKING"
        elif CURRENT_EDITING_STATE == "ASKING":
            target_num = UtilFunction.parseInputNumber(message)
            target_content = Order.getOrder(target_num)
            reply_message = UtilFunction.parseObject2Text(target_content) + "\n" + MODIFY_INSTRUCTION
            CURRENT_EDITING_STATE = "EDITING"
        
        elif CURRENT_EDITING_STATE == "EDITING":
            content_buffer = UtilFunction.parseText2Object(message)
            reply_message = message + "\n" + GUARANTEEING_MESSAGE
            CURRENT_EDITING_STATE = "WAITING"
    
        elif CURRENT_EDITING_STATE == "WAITING":
            UtilFunction.yesOrNoChecking(message)
            if message == NO:
                Order.updateOrder(content_buffer, target_num)
                reply_message = EDIT_SUCCESS_MESSAGE + "\n" + SELECTION_MESSAGE
                BACK_TO_SELECTION_MODE = True
                initializeParameter()
            elif message == YES:
                CURRENT_EDITING_STATE = "EDITING"
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
    global CURRENT_EDITING_STATE
    global content_buffer,target_num
    
    content_buffer = None
    target_num = None
    CURRENT_EDITING_STATE = "BEGIN"

    