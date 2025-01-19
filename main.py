import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

import sys
from PyQt5.QtWidgets import (
    QApplication,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QHBoxLayout,
)
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtCore import Qt, QTimer


class SimpleTable(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Titanic Survivor Data")
        self.setGeometry(100, 100, 1200, 800)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.table = QTableWidget()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.table)


class PaginatedTable(SimpleTable):

    def __init__(self, data, rows_per_page=20):
        self.data = data
        self.rows_per_page = rows_per_page
        self.current_page = 0
        self.model = None
        super().__init__()
        self.make_prediction()

    def initUI(self):
        super().initUI()
        self.update_table()

        # Add navigation buttons
        button_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.next_button = QPushButton("Next")
        self.info_button = QPushButton("Info")

        # Apply styles
        self.prev_button.setStyleSheet(
            "padding: 10px; background-color: #3498db; color: white;"
        )
        self.next_button.setStyleSheet(
            "padding: 10px; background-color: #3498db; color: white;"
        )
        self.info_button.setStyleSheet(
            "padding: 10px; background-color: #3498db; color: white;"
        )
        self.prev_button.clicked.connect(self.previous_page)
        self.next_button.clicked.connect(self.next_page)
        self.info_button.clicked.connect(self.show_info)
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.info_button)
        button_layout.addWidget(self.next_button)

        # A new HBoxLayout for prediction, it should take sex and age as input and have predict button
        prediction_layout = QHBoxLayout()

        self.age_label = QLabel("Age:")
        self.age_input = QLineEdit()
        self.sex_label = QLabel("Sex:")
        self.sex_input = QComboBox()
        self.sex_input.addItems(["male", "female"])
        self.predict_button = QPushButton("Train Model")
        self.predict_survival_button = QPushButton("Predict Survival")

        prediction_layout.addWidget(self.age_label)
        prediction_layout.addWidget(self.age_input)
        prediction_layout.addWidget(self.sex_label)
        prediction_layout.addWidget(self.sex_input)
        prediction_layout.addWidget(self.predict_button)
        prediction_layout.addWidget(self.predict_survival_button)

        self.layout().addLayout(prediction_layout)
        self.layout().addLayout(button_layout)

        self.predict_button.clicked.connect(self.make_prediction)
        self.predict_survival_button.clicked.connect(self.predict_survival)

    def make_prediction(self):

        # Load the Titanic dataset
        self.data = pd.read_csv("titanic.csv")

        # Select features and target
        self.features = data[
            ["Pclass", "Age", "Sex", "Fare", "Cabin", "SibSp", "Parch"]
        ]
        self.features["Cabin"] = self.features["Cabin"].notnull().astype(int)
        self.target = data["Survived"]

        # Handle missing values
        self.features.loc[:, "Age"].fillna(self.features["Age"].median(), inplace=True)
        self.features.loc[:, "Fare"].fillna(
            self.features["Fare"].median(), inplace=True
        )

        # Encode categorical data
        le = LabelEncoder()
        self.features["Sex"] = le.fit_transform(self.features["Sex"])

        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            self.features, self.target, test_size=0.2, random_state=42
        )

        # Initialize and train the model
        self.model = LogisticRegression(max_iter=1000)
        self.model.fit(X_train, y_train)

        # Make predictions
        predictions = self.model.predict(X_test)

        # Evaluate the model
        accuracy = accuracy_score(y_test, predictions)

        # Display accuracy as a label at the bottom
        self.accuracy_label = QLabel(f"Model is trained with accuracy: {accuracy * 100:.2f}%")
        self.accuracy_label.setStyleSheet(
            "color: #2ecc71; font-size: 16px; font-weight: bold; margin: 20px;"
        )
        self.accuracy_label.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self.accuracy_label)
       

    def predict_survival(self):
        try:
            age = float(self.age_input.text())
            if age < 0:
                raise ValueError("Age cannot be negative")
        except ValueError as e:
            print(f"Invalid age: {e}")
            return

        sex = 1 if self.sex_input.currentText() == "male" else 0

        prediction = self.model.predict(
            [[3, age, sex, 0, 0, 0, 0]]
        )  # Example input, adjust as necessary

        result = "Survived" if prediction[0] == 1 else "Did not survive"

        # Display prediction result in a new window
        self.result_window = QWidget()
        self.result_window.setWindowTitle("Prediction Result")
        self.result_window.setGeometry(150, 150, 300, 100)

        layout = QVBoxLayout()
        self.result_window.setLayout(layout)

        result_label = QLabel(f"Prediction: {result}")
        result_label.setStyleSheet(
            "color: #2ecc71; font-size: 16px; font-weight: bold; margin: 20px;"
        )
        result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(result_label)

        self.result_window.show()

        # close the window after 5 seconds
        QTimer.singleShot(10000, self.result_window.close)

    def update_table(self):
        start_row = self.current_page * self.rows_per_page
        end_row = start_row + self.rows_per_page
        page_data = self.data.iloc[start_row:end_row]

        self.table.setRowCount(len(page_data))
        self.table.setColumnCount(len(page_data.columns))
        self.table.setHorizontalHeaderLabels(page_data.columns)

        for i in range(len(page_data)):
            for j in range(len(page_data.columns)):
                self.table.setItem(i, j, QTableWidgetItem(str(page_data.iat[i, j])))

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def next_page(self):
        if (self.current_page + 1) * self.rows_per_page < len(self.data):
            self.current_page += 1
            self.update_table()

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_table()

    def show_info(self):
        info = self.data.describe().to_string()

        self.info_window = QWidget()
        self.info_window.setWindowTitle("Data Info")
        self.info_window.setGeometry(150, 150, 400, 300)

        layout = QVBoxLayout()
        self.info_window.setLayout(layout)

        info_label = QLabel(info)
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        self.info_window.show()


if __name__ == "__main__":
    data = pd.read_csv("titanic.csv")
    app = QApplication(sys.argv)
    window = PaginatedTable(data)
    window.show()
    sys.exit(app.exec_())
