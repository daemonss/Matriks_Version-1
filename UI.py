import sys
import numpy as np
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGroupBox, QLabel, QLineEdit, QTextEdit,
                             QPushButton, QSpinBox, QComboBox, QTableWidget,
                             QTableWidgetItem, QMessageBox, QScrollArea, QDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator

# Import logika dari file T2_2A_017.py
from T2_2A_017 import tambah, kurang, kali, evaluasi

class MatrixInputDialog(QDialog):
    def __init__(self, parent=None, edit_mode=False, existing_matrix=None, var_name=""):
        super().__init__(parent)
        self.edit_mode = edit_mode
        self.existing_matrix = existing_matrix
        self.var_name = var_name
        
        if edit_mode:
            self.setWindowTitle(f"Edit Matriks {var_name}")
        else:
            self.setWindowTitle("Input Matriks")
            
        self.setGeometry(100, 100, 400, 300)
        self.setModal(True)
        self.layout = QVBoxLayout()
        
        # Input untuk ukuran matriks
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Baris:"))
        self.rows_input = QSpinBox()
        self.rows_input.setMinimum(1)
        self.rows_input.setMaximum(10)
        size_layout.addWidget(self.rows_input)
        
        size_layout.addWidget(QLabel("Kolom:"))
        self.cols_input = QSpinBox()
        self.cols_input.setMinimum(1)
        self.cols_input.setMaximum(10)
        size_layout.addWidget(self.cols_input)
        
        self.confirm_size_btn = QPushButton("Buat Matriks")
        self.confirm_size_btn.clicked.connect(self.create_matrix_table)
        size_layout.addWidget(self.confirm_size_btn)
        
        self.layout.addLayout(size_layout)
        
        # Keyboard instructions
        keyboard_info = QLabel("💡 Tips: Gunakan Arrow Keys, Tab, atau Enter untuk navigasi antar sel")
        keyboard_info.setStyleSheet("QLabel { color: #666; font-size: 10px; font-style: italic; }")
        keyboard_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(keyboard_info)
        
        # Area untuk tabel matriks
        self.matrix_table = QTableWidget()
        self.matrix_table.setTabKeyNavigation(True)  # Enable tab navigation
        self.matrix_table.setAlternatingRowColors(True)  # Alternating row colors for better visibility
        self.matrix_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectItems)
        self.matrix_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        # Enable keyboard navigation
        self.matrix_table.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        self.layout.addWidget(self.matrix_table)
        
        # Tombol konfirmasi dan cancel
        button_layout = QHBoxLayout()
        self.confirm_btn = QPushButton("Konfirmasi")
        self.confirm_btn.clicked.connect(self.confirm_matrix)
        self.cancel_btn = QPushButton("Batal")
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.confirm_btn)
        button_layout.addWidget(self.cancel_btn)
        self.layout.addLayout(button_layout)
        
        self.setLayout(self.layout)
        
        # Jika dalam mode edit, langsung populate data yang ada
        if self.edit_mode and self.existing_matrix is not None:
            self.populate_existing_matrix()
        
    def create_matrix_table(self):
        rows = self.rows_input.value()
        cols = self.cols_input.value()
        
        self.matrix_table.setRowCount(rows)
        self.matrix_table.setColumnCount(cols)
        
        # Set header labels
        self.matrix_table.setHorizontalHeaderLabels([f"Kolom {j+1}" for j in range(cols)])
        self.matrix_table.setVerticalHeaderLabels([f"Baris {i+1}" for i in range(rows)])
        
        # Clear all cells (don't pre-fill with "0")
        for i in range(rows):
            for j in range(cols):
                item = QTableWidgetItem("")
                self.matrix_table.setItem(i, j, item)
        
        # Resize columns to fit content
        self.matrix_table.resizeColumnsToContents()
        
        # Set focus to first cell and enable keyboard navigation
        if rows > 0 and cols > 0:
            self.matrix_table.setCurrentCell(0, 0)
            self.matrix_table.setFocus()
    
    def populate_existing_matrix(self):
        """Mengisi tabel dengan data matriks yang sudah ada (untuk mode edit)"""
        if self.existing_matrix is not None:
            rows, cols = self.existing_matrix.shape
            self.rows_input.setValue(rows)
            self.cols_input.setValue(cols)
            self.create_matrix_table()
            
            # Isi tabel dengan data yang sudah ada
            for i in range(rows):
                for j in range(cols):
                    value = self.existing_matrix[i, j]
                    # Format nilai dengan presisi yang wajar
                    if value % 1 == 0:
                        text_value = str(int(value))
                    else:
                        text_value = f"{value:.6f}".rstrip('0').rstrip('.')
                    item = QTableWidgetItem(text_value)
                    self.matrix_table.setItem(i, j, item)
            
            # Resize columns to fit content
            self.matrix_table.resizeColumnsToContents()
            
            # Set focus to first cell for keyboard navigation
            if rows > 0 and cols > 0:
                self.matrix_table.setCurrentCell(0, 0)
                self.matrix_table.setFocus()
        
    
    def confirm_matrix(self):
        # Validasi input matriks
        rows = self.matrix_table.rowCount()
        cols = self.matrix_table.columnCount()
        
        try:
            # Paksa commit editor pada sel yang sedang aktif agar nilai terbaru tersimpan
            self.confirm_btn.setFocus()
            QApplication.processEvents()

            matrix_data = []
            print(f"Memproses matriks {rows}x{cols}")
            
            for i in range(rows):
                row_data = []
                for j in range(cols):
                    item = self.matrix_table.item(i, j)
                    if item is None:
                        QMessageBox.warning(self, "Error", f"Sel pada baris {i+1}, kolom {j+1} tidak ada!")
                        return
                    
                    text_value = item.text().strip()
                    if text_value == "":
                        QMessageBox.warning(self, "Error", f"Sel pada baris {i+1}, kolom {j+1} harus diisi!")
                        return
                    
                    try:
                        value = float(text_value)
                        row_data.append(value)
                        print(f"Baris {i+1}, Kolom {j+1}: '{text_value}' -> {value}")
                    except ValueError:
                        QMessageBox.warning(self, "Error", f"Sel pada baris {i+1}, kolom {j+1} harus berupa angka! (Input: '{text_value}')")
                        return
                matrix_data.append(row_data)
                print(f"Baris {i+1} selesai: {row_data}")
            
            self.matrix = np.array(matrix_data)
            
            # Debug: Tampilkan matriks yang akan disimpan
            print(f"Matriks final yang disimpan:\n{self.matrix}")
            print(f"Shape: {self.matrix.shape}")
            
            # Tutup dialog dengan status Accepted
            self.accept()
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Terjadi kesalahan: {str(e)}")
            return

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧮 Kalkulator Matriks - Muhammad Arrafi")
        self.setGeometry(100, 100, 1000, 700)
        self.setMinimumSize(800, 600)
        
        # Data storage
        self.variables = {}
        
        # Setup UI
        self.init_ui()
        
    def init_ui(self):
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Left panel for input
        left_panel = QGroupBox("📥 Input Variabel")
        left_panel.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        left_layout = QVBoxLayout()
        
        # Variable type selection
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Jenis:"))
        self.var_type = QComboBox()
        self.var_type.addItems(["Matriks", "Skalar"])
        self.var_type.currentTextChanged.connect(self.toggle_input_type)
        type_layout.addWidget(self.var_type)
        left_layout.addLayout(type_layout)
        
        # Variable name input
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Nama Variabel:"))
        self.var_name = QLineEdit()
        self.var_name.setMaxLength(1)
        name_layout.addWidget(self.var_name)
        left_layout.addLayout(name_layout)
        
        # Matrix input akan ditangani langsung oleh add_variable
        
        # Scalar input
        scalar_layout = QHBoxLayout()
        self.scalar_label = QLabel("Nilai Skalar:")
        scalar_layout.addWidget(self.scalar_label)
        self.scalar_input = QLineEdit()
        self.scalar_input.setText("0")
        # Only allow numeric input (floats)
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.scalar_input.setValidator(validator)
        scalar_layout.addWidget(self.scalar_input)
        left_layout.addLayout(scalar_layout)
        
        # Add variable button
        self.add_var_btn = QPushButton("➕ Tambah Variabel")
        self.add_var_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 8px; }")
        self.add_var_btn.clicked.connect(self.add_variable)
        left_layout.addWidget(self.add_var_btn)
        
        # List of variables
        vars_label = QLabel("Variabel Tersedia:")
        vars_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        left_layout.addWidget(vars_label)
        self.vars_list = QTextEdit()
        self.vars_list.setReadOnly(True)
        left_layout.addWidget(self.vars_list)
        
        # Variable selection for deletion and editing
        var_manage_layout = QVBoxLayout()
        
        # Label untuk kelola variabel
        manage_label = QLabel("Kelola Variabel:")
        manage_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        var_manage_layout.addWidget(manage_label)
        
        # Combo box untuk pilih variabel
        self.var_manage_combo = QComboBox()
        self.var_manage_combo.setPlaceholderText("Pilih variabel")
        self.var_manage_combo.setMinimumHeight(30)
        var_manage_layout.addWidget(self.var_manage_combo)
        
        # Button layout for edit and delete
        button_manage_layout = QHBoxLayout()
        
        self.edit_var_btn = QPushButton("✏️ Edit")
        self.edit_var_btn.setStyleSheet("QPushButton { background-color: #FF9800; color: white; font-weight: bold; padding: 8px 12px; font-size: 11px; min-width: 60px; }")
        self.edit_var_btn.clicked.connect(self.edit_variable)
        button_manage_layout.addWidget(self.edit_var_btn)
        
        self.delete_var_btn = QPushButton("🗑️ Hapus")
        self.delete_var_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; font-weight: bold; padding: 8px 12px; font-size: 11px; min-width: 60px; }")
        self.delete_var_btn.clicked.connect(self.delete_variable)
        button_manage_layout.addWidget(self.delete_var_btn)
        
        var_manage_layout.addLayout(button_manage_layout)
        left_layout.addLayout(var_manage_layout)
        
        left_panel.setLayout(left_layout)
        left_panel.setMaximumWidth(350)
        left_panel.setMinimumWidth(320)
        main_layout.addWidget(left_panel)
        
        # Right panel for operation and result
        right_panel = QGroupBox("⚙️ Operasi dan Hasil")
        right_panel.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        right_layout = QVBoxLayout()
        
        # Expression input
        right_layout.addWidget(QLabel("Ekspresi Operasi (contoh: A + B * C):"))
        self.expression_input = QLineEdit()
        right_layout.addWidget(self.expression_input)
        
        # Calculate button
        self.calc_btn = QPushButton("🚀 Hitung")
        self.calc_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; font-weight: bold; padding: 10px; font-size: 14px; }")
        self.calc_btn.clicked.connect(self.calculate_expression)
        right_layout.addWidget(self.calc_btn)
        
        # Result display
        right_layout.addWidget(QLabel("📊 Hasil:"))
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setStyleSheet("QTextEdit { background-color: #4C566A; border: 2px solid #ddd; border-radius: 5px; padding: 10px; font-family: 'Courier New', monospace; }")
        right_layout.addWidget(self.result_display)
        
        # Clear result button (moved below result)
        self.clear_result_btn = QPushButton("🧹 Hapus Hasil")
        self.clear_result_btn.setStyleSheet("QPushButton { background-color: #FF9800; color: white; font-weight: bold; padding: 8px; }")
        self.clear_result_btn.clicked.connect(self.clear_result)
        right_layout.addWidget(self.clear_result_btn)
        
        right_panel.setLayout(right_layout)
        main_layout.addWidget(right_panel)
        
        # Initialize UI state
        self.toggle_input_type()
        self.update_variable_combo()
        
    def toggle_input_type(self):
        if self.var_type.currentText() == "Matriks":
            self.scalar_label.setVisible(False)
            self.scalar_input.setVisible(False)
        else:
            self.scalar_label.setVisible(True)
            self.scalar_input.setVisible(True)
    
    def add_variable(self):
        var_name = self.var_name.text().strip().upper()
        # Validate variable name: one alphabetic letter A-Z
        if not var_name:
            QMessageBox.warning(self, "Error", "Nama variabel tidak boleh kosong!")
            return
        if len(var_name) != 1 or not var_name.isalpha():
            QMessageBox.warning(self, "Error", "Nama variabel harus 1 huruf (A-Z)!")
            return
        
        if var_name in self.variables:
            QMessageBox.warning(self, "Error", f"Variabel {var_name} sudah ada!")
            return
        
        if self.var_type.currentText() == "Matriks":
            # Buka dialog matriks langsung
            self.matrix_dialog = MatrixInputDialog(self, edit_mode=False)
            result = self.matrix_dialog.exec()
            
            if result == QDialog.DialogCode.Accepted:
                # Simpan matriks ke variabel
                matrix_value = self.matrix_dialog.matrix
                self.variables[var_name] = matrix_value
                
                # Update UI
                self.update_variables_list()
                self.update_variable_combo()
                
                # Show success message
                matrix_str = ""
                for i, row in enumerate(self.variables[var_name]):
                    matrix_str += f"  [{', '.join([f'{x:.1f}' if x % 1 != 0 else f'{int(x)}' for x in row])}]\n"
                
                QMessageBox.information(self, "Sukses", 
                    f"Variabel '{var_name}' berhasil ditambahkan!\n"
                    f"Tipe: Matriks {self.variables[var_name].shape}\n"
                    f"Elemen:\n{matrix_str}")
                
                # Clear dialog reference
                del self.matrix_dialog
                
                # Reset input fields
                self.var_name.clear()
            
        else:  # Scalar
            try:
                scalar_value = float(self.scalar_input.text())
                self.variables[var_name] = scalar_value
                
                # Update UI
                self.update_variables_list()
                self.update_variable_combo()
                
                # Show success message
                QMessageBox.information(self, "Sukses", 
                    f"Variabel '{var_name}' berhasil ditambahkan!\n"
                    f"Tipe: Skalar\n"
                    f"Nilai: {scalar_value}")
                
                # Reset input fields
                self.var_name.clear()
                self.scalar_input.setText("0")
                
            except ValueError:
                QMessageBox.warning(self, "Error", "Nilai skalar harus berupa angka!")
                return
    
    def update_variables_list(self):
        text = ""
        for name, value in self.variables.items():
            if isinstance(value, np.ndarray):
                text += f"{name}: Matriks {value.shape}\n"
                text += f"Elemen:\n"
                # Format matriks dengan lebih jelas
                for i, row in enumerate(value):
                    text += f"  [{', '.join([f'{x:.1f}' if x % 1 != 0 else f'{int(x)}' for x in row])}]\n"
                text += "-" * 30 + "\n"
            else:
                text += f"{name}: Skalar ({value})\n"
                text += f"Nilai: {value}\n"
                text += "-" * 30 + "\n"
        self.vars_list.setText(text)
    
    def update_variable_combo(self):
        """Update combo box dengan variabel yang tersedia"""
        self.var_manage_combo.clear()
        for var_name in self.variables.keys():
            self.var_manage_combo.addItem(var_name)
    
    def edit_variable(self):
        """Mengedit variabel yang dipilih"""
        selected_var = self.var_manage_combo.currentText()
        if not selected_var:
            QMessageBox.warning(self, "Error", "Pilih variabel yang akan diedit!")
            return
        
        if selected_var not in self.variables:
            QMessageBox.warning(self, "Error", f"Variabel '{selected_var}' tidak ditemukan!")
            return
        
        existing_value = self.variables[selected_var]
        
        if isinstance(existing_value, np.ndarray):
            # Edit matriks
            self.matrix_dialog = MatrixInputDialog(self, edit_mode=True, 
                                                 existing_matrix=existing_value, 
                                                 var_name=selected_var)
            # Populate existing data
            self.matrix_dialog.populate_existing_matrix()
            
            result = self.matrix_dialog.exec()
            
            if result == QDialog.DialogCode.Accepted:
                # Update variabel dengan nilai baru
                self.variables[selected_var] = self.matrix_dialog.matrix
                self.update_variables_list()
                
                # Show success message
                matrix_str = ""
                for i, row in enumerate(self.variables[selected_var]):
                    matrix_str += f"  [{', '.join([f'{x:.1f}' if x % 1 != 0 else f'{int(x)}' for x in row])}]\n"
                
                QMessageBox.information(self, "Sukses", 
                    f"Variabel '{selected_var}' berhasil diedit!\n"
                    f"Tipe: Matriks {self.variables[selected_var].shape}\n"
                    f"Elemen:\n{matrix_str}")
                
                # Clear dialog reference
                del self.matrix_dialog
        else:
            # Edit skalar - buka dialog sederhana
            from PyQt6.QtWidgets import QInputDialog
            new_value, ok = QInputDialog.getDouble(self, f"Edit Skalar {selected_var}", 
                                                 f"Nilai baru untuk {selected_var}:", 
                                                 value=existing_value, 
                                                 decimals=6)
            if ok:
                self.variables[selected_var] = new_value
                self.update_variables_list()
                QMessageBox.information(self, "Sukses", 
                    f"Variabel '{selected_var}' berhasil diedit!\n"
                    f"Tipe: Skalar\n"
                    f"Nilai baru: {new_value}")
    
    def delete_variable(self):
        """Menghapus variabel yang dipilih"""
        selected_var = self.var_manage_combo.currentText()
        if not selected_var:
            QMessageBox.warning(self, "Error", "Pilih variabel yang akan dihapus!")
            return
        
        reply = QMessageBox.question(self, "Konfirmasi", 
                                   f"Yakin ingin menghapus variabel '{selected_var}'?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            del self.variables[selected_var]
            self.update_variables_list()
            self.update_variable_combo()
            QMessageBox.information(self, "Sukses", f"Variabel '{selected_var}' telah dihapus!")
    
    def clear_result(self):
        """Menghapus hasil operasi"""
        self.result_display.clear()
        QMessageBox.information(self, "Info", "Hasil operasi telah dihapus!")
    
    def calculate_expression(self):
        expression = self.expression_input.text().strip()
        if not expression:
            QMessageBox.warning(self, "Error", "Ekspresi tidak boleh kosong!")
            return
        # Validate expression characters: only A-Z, +, -, * and spaces
        allowed = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ+-*() ")
        if any(ch not in allowed for ch in expression.upper().replace(" ", "")):
            QMessageBox.warning(self, "Error", "Ekspresi hanya boleh mengandung huruf A-Z dan operator +, -, *!")
            return
            
        if not self.variables:
            QMessageBox.warning(self, "Error", "Belum ada variabel yang ditambahkan!")
            return
            
        try:
            # Menggunakan fungsi evaluasi yang diimport dari T2_2A_017.py
            hasil_akhir = evaluasi(expression.upper(), self.variables)
            
            # Format hasil yang lebih baik
            result_text = f"Ekspresi: {expression.upper()}\n"
            result_text += "=" * 50 + "\n\n"
            result_text += "HASIL PERHITUNGAN:\n"
            result_text += "=" * 50 + "\n"
            
            if isinstance(hasil_akhir, np.ndarray):
                result_text += f"Tipe: Matriks {hasil_akhir.shape}\n\n"
                result_text += "Data Matriks:\n"
                result_text += str(hasil_akhir)
            else:
                result_text += f"Tipe: Skalar\n\n"
                result_text += f"Nilai: {hasil_akhir}"
            
            result_text += "\n\n" + "=" * 50 + "\n"
            result_text += "Perhitungan berhasil!"
            
            self.result_display.setText(result_text)
                
        except ValueError as e:
            error_text = f"Ekspresi: {expression.upper()}\n"
            error_text += "=" * 50 + "\n\n"
            error_text += "❌ ERROR:\n"
            error_text += "=" * 50 + "\n"
            error_text += f"Pesan Error: {str(e)}\n\n"
            error_text += "Pastikan:\n"
            error_text += "1. Semua variabel dalam ekspresi sudah didefinisikan\n"
            error_text += "2. Ordo matriks sesuai untuk operasi yang dilakukan\n"
            error_text += "3. Ekspresi menggunakan operator yang benar (+, -, *)\n"
            
            self.result_display.setText(error_text)
            QMessageBox.warning(self, "Error", str(e))
            
        except Exception as e:
            error_text = f"Ekspresi: {expression.upper()}\n"
            error_text += "=" * 50 + "\n\n"
            error_text += "❌ ERROR TIDAK DIKENAL:\n"
            error_text += "=" * 50 + "\n"
            error_text += f"Pesan Error: {str(e)}\n"
            
            self.result_display.setText(error_text)
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()