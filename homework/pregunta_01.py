# pylint: disable=line-too-long
"""
Escriba el codigo que ejecute la accion solicitada.
"""
import os
import matplotlib.pyplot as plt
import pandas as pd


def pregunta_01():
    """
    El archivo `files//shipping-data.csv` contiene información sobre los envios
    de productos de una empresa. Cree un dashboard estático en HTML que
    permita visualizar los siguientes campos:

    * `Warehouse_block`

    * `Mode_of_Shipment`

    * `Customer_rating`

    * `Weight_in_gms`

    El dashboard generado debe ser similar a este:

    https://github.com/jdvelasq/LAB_matplotlib_dashboard/blob/main/shipping-dashboard-example.png

    Para ello, siga las instrucciones dadas en el siguiente video:

    https://youtu.be/AgbWALiAGVo

    Tenga en cuenta los siguientes cambios respecto al video:

    * El archivo de datos se encuentra en la carpeta `data`.

    * Todos los archivos debe ser creados en la carpeta `docs`.

    * Su código debe crear la carpeta `docs` si no existe.

    """
    input_file = "files/input/shipping-data.csv"
    output_dir = "docs"
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(input_file)

    create_visualizations(df, output_dir)

    generate_html_dashboard(output_dir)


def create_visualizations(df, output_dir):
    plt.figure()
    warehouse_counts = df["Warehouse_block"].value_counts()
    warehouse_counts.plot.bar(
        title="Shipping per Warehouse",
        xlabel="Warehouse block",
        ylabel="Record count",
        color="skyblue",
        fontsize=8,
    )
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.savefig(os.path.join(output_dir, "shipping_per_warehouse.png"))
    plt.close()

    plt.figure()
    shipment_counts = df["Mode_of_Shipment"].value_counts()
    shipment_counts.plot.pie(
        title="Mode of Shipment",
        wedgeprops=dict(width=0.35),
        ylabel="",
        colors=["lightcoral", "lightgreen", "lightskyblue"],
    )
    plt.savefig(os.path.join(output_dir, "mode_of_shipment.png"))
    plt.close()

    plt.figure()
    rating_stats = (
        df[["Mode_of_Shipment", "Customer_rating"]]
        .groupby("Mode_of_Shipment")
        .describe()
    )
    rating_stats.columns = rating_stats.columns.droplevel()
    rating_stats = rating_stats[["mean", "min", "max"]]

    plt.barh(
        y=rating_stats.index.values,
        width=rating_stats["max"].values - 1,
        left=rating_stats["min"].values,
        height=0.9,
        color="lightgray",
        alpha=0.8,
    )
    colors = [
        "lightgreen" if value >= 3.0 else "orange"
        for value in rating_stats["mean"].values
    ]
    plt.barh(
        y=rating_stats.index.values,
        width=rating_stats["mean"].values - 1,
        left=rating_stats["min"].values,
        color=colors,
        height=0.5,
        alpha=1.0,
    )
    plt.title("Average Customer Rating")
    plt.gca().spines["left"].set_color("gray")
    plt.gca().spines["bottom"].set_color("gray")
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.savefig(os.path.join(output_dir, "average_customer_rating.png"))
    plt.close()

    plt.figure()
    df["Weight_in_gms"].plot.hist(
        title="Shipped Weight Distribution", color="lightcoral", edgecolor="white"
    )
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.savefig(os.path.join(output_dir, "weight_distribution.png"))
    plt.close()


def generate_html_dashboard(output_dir):
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Shipping Dashboard</title>
            <style>
                body { font-family: Arial, sans-serif; }
                h1 { text-align: center; }
                .container { display: flex; flex-wrap: wrap; justify-content: space-around; }
                .container img { max-width: 45%; margin: 10px; }
            </style>
        </head>
        <body>
            <h1>Shipping Dashboard</h1>
            <div class="container">
                <img src="shipping_per_warehouse.png" alt="Shipping per Warehouse">
                <img src="mode_of_shipment.png" alt="Mode of Shipment">
                <img src="average_customer_rating.png" alt="Average Customer Rating">
                <img src="weight_distribution.png" alt="Weight Distribution">
            </div>
        </body>
    </html>
    """
    with open(os.path.join(output_dir, "index.html"), "w") as file:
        file.write(html_content)


pregunta_01()
