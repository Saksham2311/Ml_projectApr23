import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
import os

from sklearn.compose import ColumnTransformer # merge columns after applying scaling and one hot encoder
from sklearn.impute import SimpleImputer
#used to handle missing values in a dataset by replacing them with a specified strategy(mean,median,most freq etc)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler 
#OneHotEncoder-convert cat feature into vectors like {1,0,0}
#scaler-normalizes values and brings them b/w [-1,1] such that they have 0 mean and standard dev=1

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object
#class to handle any input
@dataclass
class DataTranfromationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts','preprocessor.pkl')

class DataTranformation:
    def __init__(self):
        self.data_transformation_config=DataTranfromationConfig()
        
    #func to convert cat to numerical features, standard scaler
    def get_data_transformer_object(self):
        try:
            Numerical_cols=['reading_score', 'writing_score']
            Categorical_cols=['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']

            num_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),#replace missing values with median
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )
            cat_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder",OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                     ]
            )
            logging.info("Categorical and Numerical Columns encodng and scaling done")
            
            preprocessor=ColumnTransformer( # to add back the columns 
                [
                    ("num_pipeline",num_pipeline,Numerical_cols),
                    ("cat_pipeline",cat_pipeline,Categorical_cols)
                ]
            )
            return preprocessor
            
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):# inputs we are receiving from data ingestion
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            logging.info("Read train and test data read")
            logging.info("obtaining preprocessing object")
            
            preprocessing_obj=self.get_data_transformer_object()
            target_column_name="math_score"
            numerical_columns = ["writing_score", "reading_score"]

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e,sys)