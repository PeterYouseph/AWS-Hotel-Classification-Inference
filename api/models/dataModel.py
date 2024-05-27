import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import StandardScaler



# Função para mapear valores categóricos
# Função para mapear valores categóricos
def map_categorical_values(data):
    # Mapeamento de valores categóricos para tipo de plano de refeição
    meal_plan_mapping = {
        "Meal Plan 1": {"type_of_meal_plan_Meal Plan 1": True, "type_of_meal_plan_Meal Plan 2": False,
                        "type_of_meal_plan_Meal Plan 3": False, "type_of_meal_plan_Not Selected": False},
        "Meal Plan 2": {"type_of_meal_plan_Meal Plan 1": False, "type_of_meal_plan_Meal Plan 2": True,
                        "type_of_meal_plan_Meal Plan 3": False, "type_of_meal_plan_Not Selected": False},
        "Meal Plan 3": {"type_of_meal_plan_Meal Plan 1": False, "type_of_meal_plan_Meal Plan 2": False,
                        "type_of_meal_plan_Meal Plan 3": True, "type_of_meal_plan_Not Selected": False},
        "Not Selected": {"type_of_meal_plan_Meal Plan 1": False, "type_of_meal_plan_Meal Plan 2": False,
                         "type_of_meal_plan_Meal Plan 3": False, "type_of_meal_plan_Not Selected": True}
    }

    # Mapeamento de valores categóricos para tipo de segmento de mercado
    market_segment_mapping = {
        "Aviation": {"market_segment_type_Aviation": True, "market_segment_type_Complementary": False,
                     "market_segment_type_Corporate": False, "market_segment_type_Offline": False,
                     "market_segment_type_Online": False},
        "Complementary": {"market_segment_type_Aviation": False, "market_segment_type_Complementary": True,
                          "market_segment_type_Corporate": False, "market_segment_type_Offline": False,
                          "market_segment_type_Online": False},
        "Corporate": {"market_segment_type_Aviation": False, "market_segment_type_Complementary": False,
                      "market_segment_type_Corporate": True, "market_segment_type_Offline": False,
                      "market_segment_type_Online": False},
        "Offline": {"market_segment_type_Aviation": False, "market_segment_type_Complementary": False,
                    "market_segment_type_Corporate": False, "market_segment_type_Offline": True,
                    "market_segment_type_Online": False},
        "Online": {"market_segment_type_Aviation": False, "market_segment_type_Complementary": False,
                   "market_segment_type_Corporate": False, "market_segment_type_Offline": False,
                   "market_segment_type_Online": True}
    }

    # Mapeamento de valores categóricos para tipo de quarto reservado
    room_type_mapping = {
        "Room_Type 1": {"room_type_reserved_Room_Type_1": True, "room_type_reserved_Room_Type_2": False,
                        "room_type_reserved_Room_Type_3": False, "room_type_reserved_Room_Type_4": False,
                        "room_type_reserved_Room_Type_5": False, "room_type_reserved_Room_Type_6": False,
                        "room_type_reserved_Room_Type_7": False},
        "Room_Type 2": {"room_type_reserved_Room_Type_1": False, "room_type_reserved_Room_Type_2": True,
                        "room_type_reserved_Room_Type_3": False, "room_type_reserved_Room_Type_4": False,
                        "room_type_reserved_Room_Type_5": False, "room_type_reserved_Room_Type_6": False,
                        "room_type_reserved_Room_Type_7": False},
        "Room_Type 3": {"room_type_reserved_Room_Type_1": False, "room_type_reserved_Room_Type_2": False,
                        "room_type_reserved_Room_Type_3": True, "room_type_reserved_Room_Type_4": False,
                        "room_type_reserved_Room_Type_5": False, "room_type_reserved_Room_Type_6": False,
                        "room_type_reserved_Room_Type_7": False},
        "Room_Type 4": {"room_type_reserved_Room_Type_1": False, "room_type_reserved_Room_Type_2": False,
                        "room_type_reserved_Room_Type_3": False, "room_type_reserved_Room_Type_4": True,
                        "room_type_reserved_Room_Type_5": False, "room_type_reserved_Room_Type_6": False,
                        "room_type_reserved_Room_Type_7": False},
        "Room_Type 5": {"room_type_reserved_Room_Type_1": False, "room_type_reserved_Room_Type_2": False,
                        "room_type_reserved_Room_Type_3": False, "room_type_reserved_Room_Type_4": False,
                        "room_type_reserved_Room_Type_5": True, "room_type_reserved_Room_Type_6": False,
                        "room_type_reserved_Room_Type_7": False},
        "Room_Type 6": {"room_type_reserved_Room_Type_1": False, "room_type_reserved_Room_Type_2": False,
                        "room_type_reserved_Room_Type_3": False, "room_type_reserved_Room_Type_4": False,
                        "room_type_reserved_Room_Type_5": False, "room_type_reserved_Room_Type_6": True,
                        "room_type_reserved_Room_Type_7": False},
        "Room_Type 7": {"room_type_reserved_Room_Type_1": False, "room_type_reserved_Room_Type_2": False,
                        "room_type_reserved_Room_Type_3": False, "room_type_reserved_Room_Type_4": False,
                        "room_type_reserved_Room_Type_5": False, "room_type_reserved_Room_Type_6": False,
                        "room_type_reserved_Room_Type_7": True}
    }

    # Mapeamento de valores categóricos para status de reserva
    booking_status_mapping = {
        "Canceled": {"booking_status_Canceled": True, "booking_status_Not_Canceled": False},
        "Not_Canceled": {"booking_status_Canceled": False, "booking_status_Not_Canceled": True}
    }

    # Atualize o dicionário data com os valores mapeados
    data.update(meal_plan_mapping.get(data["type_of_meal_plan"], {}))
    data.update(market_segment_mapping.get(data["market_segment_type"], {}))
    data.update(room_type_mapping.get(data["room_type_reserved"], {}))
    data.update(booking_status_mapping.get(data["booking_status"], {}))

    return data

# Função para processar os dados de entrada
def preprocess_input(data):
    # Mapeamento de valores categóricos
    data = map_categorical_values(data)
    
    # Criar DataFrame apenas com os campos numéricos
    df = pd.DataFrame([data])
    
    # Remover campos categóricos não convertidos
    df.drop(columns=["Booking_ID", "type_of_meal_plan", "room_type_reserved", "market_segment_type", "booking_status"], inplace=True)
    
    # Adicionando total de hóspedes e total de noites
    df['total_guests'] = df['no_of_adults'] + df['no_of_children']
    df['total_nights'] = df['no_of_weekend_nights'] + df['no_of_week_nights']
    
    # Excluir a coluna avg_price_per_room
    df.drop(columns=['avg_price_per_room'], inplace=True)
    
    # Normalização das colunas numéricas
    numeric_columns = ['lead_time', 'arrival_year', 'arrival_month', 'arrival_date', 'no_of_special_requests', 'total_guests', 'total_nights']
    df[numeric_columns] = StandardScaler().fit_transform(df[numeric_columns])
    
    return df