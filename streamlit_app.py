import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd

# URL base de la API
API_URL = "https://ccdata.io/data"
API_KEY = "65e738d9d64faaea0623c4852f78c9aca5717450ba4e8f69cd66dae476b48256"

# Definir las criptomonedas que queremos consultar (las 5 principales)
CURRENCIES = ['BTC', 'ETH', 'XRP', 'LTC', 'ADA']

# Función para obtener los precios de las criptomonedas
def Precio_de_cryptomoneda(currencies):
    """Obtiene los precios de las criptomonedas desde la API."""
    params = {
        'key': API_KEY,
        'ids': ",".join(currencies),  # Definimos las criptomonedas que vamos a consultar
        'convert': 'USD'  # Convertir los valores a USD
        }

    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        # Extracción de la información relevante
        prices = {currency: None for currency in currencies}
        for coin in data:
            symbol = coin.get('symbol')
            price = coin.get('price')
            if symbol in prices:
                prices[symbol] = price
        return prices
    else:
        return {currency: 'Error' for currency in currencies}

# Función para calcular el porcentaje de cambio
def calcular_variacion_porcentual(precio_anterior, precio_actual):
    """Calcula el porcentaje de cambio entre el precio anterior y el actual."""
    if precio_anterior == 0:
        return 0
    return ((float(precio_actual) - float(precio_anterior)) / float(precio_anterior)) * 100

# Interfaz Streamlit
st.title('Precios de Criptomonedas')
st.write("Consulta los precios actuales de las 5 principales criptomonedas.")


# Obtener los precios
prices = Precio_de_cryptomoneda(CURRENCIES)

# Mostrar los precios en una tabla
st.write("### Precios en USD:")
st.table(prices)

# Si hay precios anteriores guardados en la sesión, calculamos el porcentaje de variación
if 'previous_prices' in st.session_state:
    # Usamos pandas para crear un DataFrame con los precios anteriores y actuales
    df = pd.DataFrame({
        'Criptomoneda': list(prices.keys()),
        'Precio Anterior': list(st.session_state.previous_prices.values()),
        'Precio Actual': list(prices.values())
    })

    # Calculamos la variación porcentual para cada criptomoneda
    df['Variación (%)'] = df.apply(lambda row: calcular_variacion_porcentual(row['Precio Anterior'], row['Precio Actual']), axis=1)

    # Mostrar la tabla con las variaciones porcentuales
    st.write("### Variación porcentual en las últimas 24 horas:")
    st.table(df[['Criptomoneda', 'Variación (%)']])
else:
    st.write("### No hay datos anteriores para comparar.")

# Guardar los precios actuales para la próxima sesión
st.session_state.previous_prices = prices

# Preparar los datos para el gráfico
labels = list(prices.keys())
values = [float(price) if price != 'Error' else 0 for price in prices.values()]

# Crear el gráfico
fig, ax = plt.subplots()
ax.bar(labels, values)
ax.set_xlabel('Criptomonedas')
ax.set_ylabel('Precio en USD')
ax.set_title('Precios de Criptomonedas')

# Mostrar el gráfico
st.pyplot(fig)
