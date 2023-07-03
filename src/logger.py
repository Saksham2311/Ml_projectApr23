import logging #stores all the deails regarding all the excecution in a file, erorrs etc
import os
from datetime import datetime
#on executing this it cretes the log folder
LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE)#add logs before log file name
os.makedirs(logs_path,exist_ok=True)

LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,

)

# if __name__=="__main__":
#     logging.info("Logging has started")