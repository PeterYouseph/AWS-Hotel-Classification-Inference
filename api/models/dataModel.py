import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import StandardScaler



# Função para mapear valores categóricos
def map_categorical_values(data):
    meal_plan_mapping = {
        "1": "Meal_Plan_1",
        "2": "Meal_Plan_2",
        "3": "Meal_Plan_3",
        "Not Selected": "Not_Selected"
    }
    room_type_mapping = {
        "1": "Room_Type_1",
        "2": "Room_Type_2",
        "3": "Room_Type_3",
        "4": "Room_Type_4",
        "5": "Room_Type_5",
        "6": "Room_Type_6",
        "7": "Room_Type_7"
    }
    market_segment_mapping = {
        "Aviation": "Aviation",
        "Complementary": "Complementary",
        "Corporate": "Corporate",
        "Offline": "Offline",
        "Online": "Online"
    }
    booking_status_mapping = {
        "Yes": "Canceled",
        "No": "Not_Canceled"
    }
    
    data[f'type_of_meal_plan_{meal_plan_mapping[data["type_of_meal_plan"]]}'] = 1
    data[f'room_type_reserved_{room_type_mapping[data["room_type_reserved"]]}'] = 1
    data[f'market_segment_type_{market_segment_mapping[data["market_segment_type"]]}'] = 1
    data[f'booking_status_{booking_status_mapping[data["booking_status_Canceled"]]}'] = 1
    
    # Drop original categorical columns
    data.pop("type_of_meal_plan")
    data.pop("room_type_reserved")
    data.pop("market_segment_type")
    data.pop("booking_status_Canceled")
    
    return data

# Função para processar os dados de entrada
def preprocess_input(data):
    data = map_categorical_values(data)
    df = pd.DataFrame([data])
    
    # Adicionar colunas faltantes com valor 0
    expected_columns = [
        'no_of_adults', 'no_of_children', 'no_of_weekend_nights', 'no_of_week_nights', 
        'required_car_parking_space', 'lead_time', 'arrival_year', 'arrival_month', 
        'arrival_date', 'repeated_guest', 'no_of_previous_cancellations', 
        'no_of_previous_bookings_not_canceled', 'no_of_special_requests', 
        'type_of_meal_plan_Meal_Plan_1', 'type_of_meal_plan_Meal_Plan_2', 
        'type_of_meal_plan_Meal_Plan_3', 'type_of_meal_plan_Not_Selected', 
        'room_type_reserved_Room_Type_1', 'room_type_reserved_Room_Type_2', 
        'room_type_reserved_Room_Type_3', 'room_type_reserved_Room_Type_4', 
        'room_type_reserved_Room_Type_5', 'room_type_reserved_Room_Type_6', 
        'room_type_reserved_Room_Type_7', 'market_segment_type_Aviation', 
        'market_segment_type_Complementary', 'market_segment_type_Corporate', 
        'market_segment_type_Offline', 'market_segment_type_Online', 
        'booking_status_Canceled', 'booking_status_Not_Canceled'
    ]
    
    for col in expected_columns:
        if col not in df.columns:
            df[col] = 0

    # Feature engineering
    df['total_guests'] = df['no_of_adults'] + df['no_of_children'] + df['no_of_weekend_nights'] + df['no_of_week_nights']
    df['total_nights'] = df['no_of_weekend_nights'] + df['no_of_week_nights']

    # Normalização das features numéricas
    numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
    scaler = StandardScaler()
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
    
    return xgb.DMatrix(df)


# import pandas as pd
# from sklearn.preprocessing import StandardScaler

# class DataPreprocessor:
#     def __init__(self):
#         self.scaler = StandardScaler()

#     def preprocess_data(self, df):
#         df = self._convert_categorical(df)
#         df = self._create_label_column(df)
#         df = self._remove_missing_values(df)
#         df = self._remove_outliers(df)
#         df = self._normalize_numerical_features(df)
#         df = self._create_new_features(df)
#         return df

#     def _convert_categorical(self, df):
#         categorical_columns = ['type_of_meal_plan', 'room_type_reserved', 'market_segment_type', 'booking_status']
#         for col in categorical_columns:
#             if col in df.columns:
#                 df = pd.get_dummies(df, columns=[col])
#         return df

#     def _create_label_column(self, df):
#         if 'avg_price_per_room' in df.columns:
#             df['label_avg_price_per_room'] = pd.cut(df['avg_price_per_room'], bins=[0, 85, 115, float('inf')], labels=[1, 2, 3])
#             df.drop(columns=['avg_price_per_room'], inplace=True)
#         return df

#     def _remove_missing_values(self, df):
#         df.dropna(inplace=True)
#         return df

#     def _remove_outliers(self, df):
#         numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
#         Q1 = df[numerical_cols].quantile(0.25)
#         Q3 = df[numerical_cols].quantile(0.75)
#         IQR = Q3 - Q1
#         df = df[~((df[numerical_cols] < (Q1 - 1.5 * IQR)) | (df[numerical_cols] > (Q3 + 1.5 * IQR))).any(axis=1)]
#         return df

#     def _normalize_numerical_features(self, df):
#         numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
#         df[numerical_cols] = self.scaler.fit_transform(df[numerical_cols])
#         return df

#     def _create_new_features(self, df):
#         if all(col in df.columns for col in ['no_of_adults', 'no_of_children', 'no_of_weekend_nights', 'no_of_week_nights']):
#             df['total_guests'] = df['no_of_adults'] + df['no_of_children'] + df['no_of_weekend_nights'] + df['no_of_week_nights']
#             df['total_nights'] = df['no_of_weekend_nights'] + df['no_of_week_nights']
#         return df