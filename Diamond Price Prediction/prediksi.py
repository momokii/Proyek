import tensorflow as tf
import pandas as pd
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, OneHotEncoder, MinMaxScaler, Normalizer


class Prediksi:
    def __init__(self, model_path_name):
        # load model
        self.model = tf.keras.models.load_model(model_path_name)

    # column transfomer yang sama dengan yang digunakan pembuatan model
    def column_transformer_df(self, dataframe, scaler_column = [], oneHot_column = [],
                          ordinalEnc_column = [], minmax_column = [],
                          normalize_column = []):
        columm_transformer = make_column_transformer(

            (StandardScaler(), scaler_column),
            (MinMaxScaler(), minmax_column),
            (OneHotEncoder(), oneHot_column),
            (OrdinalEncoder(), ordinalEnc_column),
            (Normalizer(), normalize_column),
            remainder="passthrough",
            n_jobs=-1

        )

        return pd.DataFrame(columm_transformer.fit_transform(dataframe))

    # pipeline untuk penyesuaian saat transform nilai dari input ke bentuk yang dibutuhkan model
    def transform_column(self, data_prediksi):
        # Data dari inputan user dalam bentuk list diubah -> DataFrame dan berikan kolom sesuai agar
        # bisa menyesuaikan dengan data utama
        data_x_trans = pd.DataFrame(data=data_prediksi).T
        data_x_trans.columns = ['carat', 'cut', 'color', 'clarity', 'depth', 'table', 'volume']

        # tambah DF user ke DF utama, disini ditambahkan agar mengikuti konfigurasi seperti saat
        # data train yaitu untuk data yang dinormalisasi maupun diencode pada data non-numerikan
        data_bantu = pd.read_csv('bantuan_preprocessing.csv')
        data_bantu.drop('Unnamed: 0', axis='columns', inplace=True)
        data_bantu = data_bantu.append(data_x_trans)

        scaler = ['carat', 'depth', 'table', 'volume']
        oneHot = []
        OrdinalEnc = ['cut', 'color', 'clarity']

        # transform dengan fungsi sebelumnya untuk transform
        # dengan input berupa dataframe dengan isi (data bantu + data_input_prediksi [pada last row])
        kolom_transformer = self.column_transformer_df(data_bantu, minmax_column=scaler
                                                  , ordinalEnc_column=OrdinalEnc)

        # ambil hanya data paling bawah ( DATA INPUTAN USER ) sebagai output
        return pd.DataFrame(kolom_transformer.iloc[-1]).T

    def prediksi(self, data_input_prediksi):
        data_transform = self.transform_column(data_input_prediksi)

        return self.model.predict(data_transform)[0][0]











