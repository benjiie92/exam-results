
 **Exam Prediction App*

An intelligent app built by students of **Aditya College, Kakinada** to help predict probable exam results based on lifestyle and study habits.  
This project explores how factors like **study hours, sports participation, sleep, and attendance** contribute to a student’s final score using **machine learning**.

## Features
- Predict exam scores based on multiple inputs (study hours, sports, sleep, etc.).
- Interactive visualisations to understand how habits affect performance.
- Machine learning models trained with real-world student data.
- Easy-to-use interface for students to input their details and get predictions.
- Model persistence with `joblib` for quick reuse.

## Tech Stack
- **Python 3.8+**
- **scikit-learn** → ML models (Linear Regression, Random Forest, etc.)
- **pandas** → Data handling
- **numpy** → Numerical operations
- **matplotlib** → Visualizations
- **joblib** → Model saving/loading

## Installation
Clone the repository and install dependencies:

git clone https://github.com/benjiie92/exam-results.git
cd exam-results
pip install -r requirements.txt

## Usage
1. Prepare your dataset (`student_data.csv`) with columns like:
   - study_hours
   - sports
   - sleep
   - attendance
   - exam_score


## Future Improvements
- Build a **Streamlit web app** for easy student interaction.
- Improve accuracy with advanced ML models.
- Deploy online for public use.

## Contributors
- International Students of **Aditya College, Kakinada**

## License
This project is licensed under the MIT License. Feel free to use, modify, and distribute.
