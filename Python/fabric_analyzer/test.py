import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QFileDialog
import csv

class Spreadsheet(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        
        self.table = QTableWidget(10, 5)  # 10 rows, 5 columns
        self.layout.addWidget(self.table)
        
        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save_data)
        self.layout.addWidget(self.save_button)
        
        self.load_button = QPushButton('Load')
        self.load_button.clicked.connect(self.load_data)
        self.layout.addWidget(self.load_button)
        
        self.setLayout(self.layout)
        self.setWindowTitle('Spreadsheet')
        self.show()

    def save_data(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_path:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                for row in range(self.table.rowCount()):
                    row_data = []
                    for column in range(self.table.columnCount()):
                        item = self.table.item(row, column)
                        row_data.append(item.text() if item else '')
                    writer.writerow(row_data)

    def load_data(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_path:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                for row_idx, row in enumerate(reader):
                    for col_idx, cell in enumerate(row):
                        self.table.setItem(row_idx, col_idx, QTableWidgetItem(cell))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Spreadsheet()
    sys.exit(app.exec_())
