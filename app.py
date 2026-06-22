
from flask import Flask, render_template, request
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

app = Flask(__name__)

# Sample dataset
data = pd.DataFrame({
    'duration':[10,20,30,40,50,60,70,80],
    'src_bytes':[100,200,300,400,500,600,700,800],
    'dst_bytes':[50,60,70,80,90,100,110,120],
    'attack':[0,0,0,1,1,1,1,1]
})

X = data[['duration','src_bytes','dst_bytes']]
y = data['attack']

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)

model = RandomForestClassifier()
model.fit(X_train,y_train)

@app.route("/", methods=["GET","POST"])
def home():
    result = None
    if request.method == "POST":
        duration = float(request.form["duration"])
        src_bytes = float(request.form["src_bytes"])
        dst_bytes = float(request.form["dst_bytes"])

        prediction = model.predict([[duration,src_bytes,dst_bytes]])[0]

        result = "Intrusion Detected" if prediction == 1 else "Normal Traffic"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
