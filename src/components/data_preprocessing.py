import os
import pandas as pd
import numpy as np
import joblib
from configuration.paths_config import *
from src.utils import read_yaml,load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

class DataProcessor:
    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir

        self.config = read_yaml(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)
        
    
    def preprocess_data(self, df, is_train=False):
        try:
            df.drop_duplicates(inplace=True)

            if "Booking_ID" in df.columns:
                df.drop(columns=["Booking_ID"], inplace=True)

            cat_cols = self.config["data_processing"]["categorical_columns"]
            num_cols = self.config["data_processing"]["numerical_columns"]

            label_encoders = {}
            for col in cat_cols:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col])
                label_encoders[col] = le
                encoded = np.array(le.transform(le.classes_))
                print(f"Encoding mapping for '{col}': { {label: int(code) for label, code in zip(le.classes_, encoded)} }")

            skew_threshold = self.config["data_processing"]["skewness_threshold"]
            skewness = df[num_cols].apply(lambda x: x.skew())
            skewed_cols = skewness[skewness > skew_threshold].index.tolist()

            for column in skewed_cols:
                df[column] = np.log1p(df[column])

            if is_train:
                os.makedirs(os.path.dirname(LABEL_ENCODER_PATH), exist_ok=True)
                joblib.dump(label_encoders, LABEL_ENCODER_PATH)
                joblib.dump(skewed_cols, SKEWED_COLUMNS_PATH)
                print(f"Saved label encoders to {LABEL_ENCODER_PATH}")
                print(f"Saved skewed columns {skewed_cols} to {SKEWED_COLUMNS_PATH}")

            return df

        except Exception as e:
            print(f"Error {e}")
        
    def balance_data(self,df):
        try:
            X = df.drop(columns='booking_status')
            y = df["booking_status"]
            smote = SMOTE(random_state=42)
            X_resampled , y_resampled = smote.fit_resample(X,y)
            balanced_df = pd.DataFrame(X_resampled , columns=X.columns)
            balanced_df["booking_status"] = y_resampled
            return balanced_df
        
        except Exception as e:
            print(f"Error while balancing datam {e}")
    
    def select_features(self,df):
        try:
            X = df.drop(columns='booking_status')
            y = df["booking_status"]

            model =  RandomForestClassifier(random_state=42)
            model.fit(X,y)

            feature_importance = model.feature_importances_
            feature_importance_df = pd.DataFrame({'feature':X.columns,'importance':feature_importance})
            top_features_importance_df = feature_importance_df.sort_values(by="importance" , ascending=False)

            num_features_to_select = self.config["data_processing"]["no_of_features"]

            top_10_features = top_features_importance_df["feature"].head(num_features_to_select).values
            top_10_df = df[top_10_features.tolist() + ["booking_status"]]

            return top_10_df
        
        except Exception as e:
            print(f"Error while feature selection {e}")
    
    def save_data(self,df , file_path):
        try:
            df.to_csv(file_path, index=False)
        except Exception as e:
            print(f"Error while saving data {e}")

    def process(self):
        try:
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            train_df = self.preprocess_data(train_df, is_train=True)
            test_df = self.preprocess_data(test_df, is_train=False)

            train_df = self.balance_data(train_df)

            train_df = self.select_features(train_df)
            test_df = test_df[train_df.columns]  

            self.save_data(train_df,PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_df , PROCESSED_TEST_DATA_PATH)
 
        except Exception as e:
            print(f"Error while data preprocessing pipeline {e}")
              
    
    
if __name__=="__main__":
    processor = DataProcessor(TRAIN_FILE_PATH,TEST_FILE_PATH,PROCESSED_DIR,CONFIG_PATH)
    processor.process()       
    
        


