from flask import Flask, request, render_template
import joblib
import pandas as pd

app = Flask(__name__)

model = joblib.load("best_random_forest_model.pkl")
feature_names = ['StudyHours', 'Attendance', 'Resources', 'Internet', 'Gender', 'Age', 'AssignmentCompletion', 'OnlineCourses', 'StressLevel']

@app.route("/")
def home():
    return render_template("index.html")



@app.route("/predict", methods=["POST"])
def predict():
    try:
        input_data = pd.DataFrame([[
            float(request.form["StudyHours"]),
            float(request.form["Attendance"]),
            float(request.form["Resources"]),
            float(request.form["Internet"]),
            float(request.form["Gender"]),
            float(request.form["Age"]),
            float(request.form["AssignmentCompletion"]),
            float(request.form["OnlineCourses"]),
            float(request.form["StressLevel"])
        ]], columns=feature_names)
        

        prediction = model.predict(input_data)

        if prediction[0] == 0:
            result = "A"
        elif prediction[0] == 1:
            result = "B"
        elif prediction[0] == 2:
            result = "C"  
        else:            
            result = "F"
        
        

        return render_template("results.html", prediction_text=result)

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)