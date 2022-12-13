import joblib
import sklearn
import numpy as np
import pkg_resources


class Profanity:
    vectorizer: sklearn.feature_extraction.text.TfidfVectorizer = joblib.load(
        pkg_resources.resource_filename("profanity_check", "data/vectorizer.joblib")
    )
    model: sklearn.calibration.CalibratedClassifierCV = joblib.load(
        pkg_resources.resource_filename("profanity_check", "data/model.joblib")
    )

    def __init__(self, censor_char: str = '*'):
        self.censor_char = censor_char

    def censor(self, text: str):
        words = text.split(' ')
        preds = self.model.predict(
            self.vectorizer.transform(words)
        )

        for i in np.where(preds == 1)[0]:
            words[i] = ''.join([char if not char.isalpha() else self.censor_char for char in words[i]])

        return ' '.join(words)



