from .Utility.ReplyMessage import ASKING_END_DATE, ASKING_START_DATE, FORMAT_ERROR, SELECTION_MESSAGE
from .Utility import UtilFunction
from .Utility import Order
CURRENT_SUMUP_STATE = "BEGIN"

start_date_buffer = None
end_date_buffer = None

def sumUpMainFunction(message):
    global CURRENT_SUMUP_STATE, start_date_buffer, end_date_buffer
    BACK_TO_SELECTION_MODE = False
    try:
        UtilFunction.leavingChecking(message)
        
        if CURRENT_SUMUP_STATE == "BEGIN":
            reply_message = ASKING_START_DATE
            CURRENT_SUMUP_STATE = "START"
        elif CURRENT_SUMUP_STATE == "START":
            start_date_buffer = UtilFunction.parseDate(message)
            reply_message = ASKING_END_DATE
            CURRENT_SUMUP_STATE = "END"
        elif CURRENT_SUMUP_STATE == "END":
            end_date_buffer = UtilFunction.parseDate(message)
            reply_message = Order.sumUpOrders(start_date_buffer, end_date_buffer) + "\n" + SELECTION_MESSAGE
            BACK_TO_SELECTION_MODE = True
            initializeParameter()
    except Exception as e:
        if str(e) == "Leaving":
            reply_message = SELECTION_MESSAGE
            initializeParameter()
            BACK_TO_SELECTION_MODE = True
        else:
            reply_message = f"{FORMAT_ERROR}\n{e}"
    return reply_message, BACK_TO_SELECTION_MODE
def initializeParameter():
    global CURRENT_SUMUP_STATE, end_date_buffer, start_date_buffer
    
    CURRENT_SUMUP_STATE = "BEGIN"
    start_date_buffer = None
    end_date_buffer = None
        
        