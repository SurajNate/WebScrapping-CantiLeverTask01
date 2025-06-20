from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    df = pd.read_csv('products.csv')
    query = request.form.get('query')

    if query:
        results = df[df['Title'].str.contains(query, case=False)]
    else:
        results = df

    return render_template("index.html", tables=results.to_dict(orient='records'), query=query)

if __name__ == '__main__':
    app.run(debug=True)
