from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime
import joblib


class Machine:

    def __init__(self, df: DataFrame):
        self.name = 'Random Forest Classifier'
        target = df['Rarity']
        features = df[['Level', 'Health', 'Energy', 'Sanity']]
        self.model = RandomForestClassifier()
        self.model.fit(features, target)
        self.time = datetime.now()

    def __call__(self, feature_basis: DataFrame):
        prediction = self.model.predict(feature_basis)[0]
        confidence = max(self.model.predict_proba(feature_basis)[0])
        return prediction, confidence

    def save(self, filepath: str):
        joblib.dump(self, filepath)

    @staticmethod
    def open(filepath: str):
        return joblib.load(filepath)

    def info(self):
        return f"Base Model: {self.name}<br>Timestamp: {self.time}"
