from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

stations = pd.read_csv("data_small/stations.txt", skiprows=17)

@app.route("/")
def home():
    return render_template("home.html", station_table=stations.to_html())


@app.route("/dictionary/")
def dictionary():
    return render_template("dictionary.html")


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    df = pd.read_csv("data_small/TG_STAID" + str(station).zfill(6) + ".txt", skiprows=20,
                     parse_dates=["    DATE"])
    temp = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10
    temperature = temp
    return {'station': station,
            'date': date,
            'temperature': temperature}


@app.route("/api/v1/<station>")
def all_data(station):
    df = pd.read_csv("data_small/TG_STAID" + str(station).zfill(6) + ".txt", skiprows=20,
                     parse_dates=["    DATE"])
    result = df.to_dict(orient="records")
    return result


@app.route("/api/v1/yearly/<station>/<year>")
def yearly_data(station, year):
    df = pd.read_csv("data_small/TG_STAID" + str(station).zfill(6) + ".txt", skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    result = df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")
    return result


@app.route("/dictionary/api/v1/<word>")
def word_meaning(word):
    df = pd.read_csv("dictionary.csv")
    defn = df.loc[df['word'] == word]['definition'].squeeze()
    return {"Definition": defn,
            "word": word}


if __name__ == "__main__":
    app.run(debug=True, port=5001)