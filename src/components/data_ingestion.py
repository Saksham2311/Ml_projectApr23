import os #module for file handling, interacting with os(creating,terminating processes
import sys 
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

# any i/p required for data ingestion(where to save training data,test data etc.) will be done by this data ingestion config 
# through dataclass we can define class variable outside without use of init
@dataclass 
class DataIngestionConfig: 
    train_data_path: str=os.path.join('artifacts','train.csv')
    test_data_path: str=os.path.join('artifacts','test.csv')
    raw_data_path: str=os.path.join('artifacts','data.csv')
    #now data ingestion knows where to save my train path,test path etc
    
class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()
        
    def initiate_data_ingestion(self):
        logging.info("enter the data ingestion method or component")
        try:
            df=pd.read_csv('notebook\data\stud.csv')# we can import from mongodb and mysql
            logging.info('Read the datset as datframe')
            
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            #make the folder to store training data if it doesnt exsist
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            
            logging.info("Train test split initiated")
            
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            
            logging.info("Ingestion of the data completed")
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path                
            )
                               
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__":
    obj=DataIngestion()
    obj.initiate_data_ingestion()
        