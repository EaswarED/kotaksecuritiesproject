import pandas
from PyQt5 import QtWidgets
import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, \
    QPushButton, QItemDelegate, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5 import QtCore,QtGui
from PyQt5.QtGui import QDoubleValidator

import index
import rsi_interval_loop as ril

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(887, 758)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(10, 140, 201, 221))
        self.tableView.setObjectName("tableView")
        self.tableView_2 = QtWidgets.QTableView(self.centralwidget)
        self.tableView_2.setGeometry(QtCore.QRect(230, 140, 201, 221))
        self.tableView_2.setObjectName("tableView_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(380, 90, 131, 17))
        self.label.setObjectName("label")
        self.tableView_3 = QtWidgets.QTableView(self.centralwidget)
        self.tableView_3.setGeometry(QtCore.QRect(10, 480, 201, 221))
        self.tableView_3.setObjectName("tableView_3")
        self.tableView_4 = QtWidgets.QTableView(self.centralwidget)
        self.tableView_4.setGeometry(QtCore.QRect(230, 480, 201, 221))
        self.tableView_4.setObjectName("tableView_4")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(390, 430, 131, 17))
        self.label_2.setObjectName("label_2")
        self.tableView_5 = QtWidgets.QTableView(self.centralwidget)
        self.tableView_5.setGeometry(QtCore.QRect(450, 140, 201, 221))
        self.tableView_5.setObjectName("tableView_5")
        self.tableView_6 = QtWidgets.QTableView(self.centralwidget)
        self.tableView_6.setGeometry(QtCore.QRect(670, 140, 201, 221))
        self.tableView_6.setObjectName("tableView_6")
        self.tableView_7 = QtWidgets.QTableView(self.centralwidget)
        self.tableView_7.setGeometry(QtCore.QRect(670, 480, 201, 221))
        self.tableView_7.setObjectName("tableView_7")
        self.tableView_8 = QtWidgets.QTableView(self.centralwidget)
        self.tableView_8.setGeometry(QtCore.QRect(450, 480, 201, 221))
        self.tableView_8.setObjectName("tableView_8")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 120, 131, 17))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(230, 120, 131, 17))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(450, 120, 131, 17))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(670, 120, 131, 17))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(670, 460, 131, 17))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(230, 460, 131, 17))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(450, 460, 131, 17))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(10, 460, 131, 17))
        self.label_10.setObjectName("label_10")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(340, 20, 71, 41))
        self.lineEdit.setObjectName("lineEdit")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(510, 20, 71, 41))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_13.setFont(font)
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        tokens = ["16675", "2885", "25"]

        print(self.lineEdit.text())
        top_ranking_3min = []
        top_ranking_15min = []
        top_ranking_30min = []
        top_ranking_1hour = []
        top_ranking_oneday = []
        top_ranking_3min1 = []
        top_ranking_15min1 = []
        top_ranking_30min1 = []
        top_ranking_1hour1 = []
        j = 0
        while j < len(tokens):
            resp_instrument = index.get_instrument()
            df_instrument = pd.DataFrame(resp_instrument)
            df_instrument = df_instrument[
                (df_instrument['token'] == tokens[j]) & (df_instrument['exch_seg'] == 'NSE')]
            columns = {'token': 'tokenId', 'symbol': 'symbol', 'name': 'tokenName'}
            df_instrument = df_instrument[df_instrument.columns.intersection(columns)]

            df_3min = ril.df_interval_data(tokens[j], "THREE_MINUTE", "NSE", "2022-01-01 09:15", "2022-03-21 15:16",
                                       desc=True)
            df_15min = ril.df_interval_data(tokens[j], "FIFTEEN_MINUTE", "NSE", "2022-01-01 09:15", "2022-03-21 15:16",
                                        desc=True)
            df_30min = ril.df_interval_data(tokens[j], "THIRTY_MINUTE", "NSE", "2022-01-01 09:15", "2022-03-21 15:16",
                                        desc=True)
            df_1hour = ril.df_interval_data(tokens[j], "ONE_HOUR", "NSE", "2022-01-01 09:15", "2022-03-21 15:16",
                                        desc=True)
            # df_1day = df_interval_data(tokens[j], "ONE_DAY", "NSE", "2022-03-01 09:15", "2022-03-21 15:16", desc=True)

            writer = pd.ExcelWriter('{}.xlsx'.format(df_instrument['name'].values[0]), engine='xlsxwriter')

            df_3min.to_excel(writer, sheet_name='3min', index=False)
            df_15min.to_excel(writer, sheet_name='15min', index=False)
            df_30min.to_excel(writer, sheet_name='30min', index=False)
            df_1hour.to_excel(writer, sheet_name='1Hour', index=False)
            # df_1day.to_excel(writer, sheet_name='OneDay', index=False)
            # xls = pd.ExcelFile(
            #     '/home/edmonster/PycharmProjects/AngelBrokingProjects/{}.xlsx'.format(df_instrument['name'].values[0]))
            writer.save()
            df3min = pd.read_excel(
                '/home/edmonster/PycharmProjects/AngelBrokingProjects/{}.xlsx'.format(
                    df_instrument['name'].values[0]),
                sheet_name="3min")
            df15min = pd.read_excel(
                '/home/edmonster/PycharmProjects/AngelBrokingProjects/{}.xlsx'.format(
                    df_instrument['name'].values[0]),
                sheet_name="15min")
            df30min = pd.read_excel(
                '/home/edmonster/PycharmProjects/AngelBrokingProjects/{}.xlsx'.format(
                    df_instrument['name'].values[0]),
                sheet_name="30min")
            df1hour = pd.read_excel(
                '/home/edmonster/PycharmProjects/AngelBrokingProjects/{}.xlsx'.format(
                    df_instrument['name'].values[0]),
                sheet_name="1Hour")
            # dfoneday = pd.read_excel(
            #     '/home/edmonster/PycharmProjects/AngelBrokingProjects/{}.xlsx'.format(df_instrument['name'].values[0]),
            #     sheet_name="OneDay")
            print(df3min['total'].max())
            top_ranking_3min.append({
                "name": df_instrument['name'].values[0],
                "ranking_value": df3min['total'].max()
            })
            top_ranking_15min.append({
                "name": df_instrument['name'].values[0],
                "ranking_value": df15min['total'].max()
            })
            top_ranking_30min.append({
                "name": df_instrument['name'].values[0],
                "ranking_value": df30min['total'].max()
            })
            top_ranking_1hour.append({
                "name": df_instrument['name'].values[0],
                "ranking_value": df1hour['total'].max()
            })

            print(df3min['total'].max())
            top_ranking_3min1.append({
                "name": df_instrument['name'].values[0],
                "ranking_value": df3min['total'].min()
            })
            top_ranking_15min1.append({
                "name": df_instrument['name'].values[0],
                "ranking_value": df15min['total'].min()
            })
            top_ranking_30min1.append({
                "name": df_instrument['name'].values[0],
                "ranking_value": df30min['total'].min()
            })
            top_ranking_1hour1.append({
                "name": df_instrument['name'].values[0],
                "ranking_value": df1hour['total'].min()
            })

            # top_ranking_oneday.append({
            #     "name":df_instrument['name'].values[0],
            #     "ranking_value":dfoneday['total'].max()
            # })
            print("----------------3 min --------------------")
            df1 = pd.DataFrame(top_ranking_3min)
            df1 = df1.sort_values(by=['ranking_value'], ascending=False)
            df1.to_csv('/home/edmonster/PycharmProjects/AngelBrokingProjects/test1.csv')
            print(df1)
            print("----------------15 min --------------------")
            df2 = pd.DataFrame(top_ranking_15min)
            df2 = df2.sort_values(by=['ranking_value'], ascending=False)
            df1.to_csv('/home/edmonster/PycharmProjects/AngelBrokingProjects/test2.csv')
            print(df2)
            print("----------------30 min --------------------")
            df3 = pd.DataFrame(top_ranking_30min)
            df3 = df3.sort_values(by=['ranking_value'], ascending=False)
            df1.to_csv('/home/edmonster/PycharmProjects/AngelBrokingProjects/test3.csv')
            print(df3)
            print("----------------1 hour --------------------")
            df4 = pd.DataFrame(top_ranking_1hour)
            df4 = df4.sort_values(by=['ranking_value'], ascending=False)

            print(df4)
            # print("----------------One day --------------------")
            # df5 = pd.DataFrame(top_ranking_oneday)
            # df5 = df5.sort_values(by=['ranking_value'], ascending=False)
            # print(df5)
            print("----------------3 min --------------------")
            df5 = pd.DataFrame(top_ranking_3min1)
            df5 = df5.sort_values(by=['ranking_value'], ascending=True)

            print(df5)
            print("----------------15 min --------------------")
            df6 = pd.DataFrame(top_ranking_15min1)
            df6 = df6.sort_values(by=['ranking_value'], ascending=True)

            print(df6)
            print("----------------30 min --------------------")
            df7 = pd.DataFrame(top_ranking_30min1)
            df7 = df7.sort_values(by=['ranking_value'], ascending=True)

            print(df7)
            print("----------------1 hour --------------------")
            df8 = pd.DataFrame(top_ranking_1hour1)
            df8 = df8.sort_values(by=['ranking_value'], ascending=True)

            print(df8)

            j += 1

        model = PandasModel(df1)
        model1 = PandasModel(df2)
        model2 = PandasModel(df3)
        model3 = PandasModel(df4)
        model4 = PandasModel(df5)
        model5 = PandasModel(df6)
        model6 = PandasModel(df7)
        model7 = PandasModel(df8)

        self.tableView.setModel(model)
        self.tableView_2.setModel(model1)
        self.tableView_3.setModel(model4)
        self.tableView_4.setModel(model5)
        self.tableView_5.setModel(model2)
        self.tableView_6.setModel(model3)
        self.tableView_7.setModel(model7)
        self.tableView_8.setModel(model6)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 887, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "+VE 2 -VE"))
        self.label_2.setText(_translate("MainWindow", "-VE 2 +VE"))
        self.label_3.setText(_translate("MainWindow", "3 min"))
        self.label_4.setText(_translate("MainWindow", "15 min"))
        self.label_5.setText(_translate("MainWindow", "30 min"))
        self.label_6.setText(_translate("MainWindow", "1 Hours"))
        self.label_7.setText(_translate("MainWindow", "1 Hours"))
        self.label_8.setText(_translate("MainWindow", "15 min"))
        self.label_9.setText(_translate("MainWindow", "30 min"))
        self.label_10.setText(_translate("MainWindow", "3 min"))

def test_data(tokens):
    top_ranking_3min = []
    top_ranking_15min = []
    top_ranking_30min = []
    top_ranking_1hour = []
    top_ranking_oneday = []
    top_ranking_3min1 = []
    top_ranking_15min1 = []
    top_ranking_30min1 = []
    top_ranking_1hour1 = []
    j = 0
    while j < len(tokens):
        resp_instrument = index.get_instrument()
        df_instrument = pd.DataFrame(resp_instrument)
        df_instrument = df_instrument[(df_instrument['token'] == tokens[j]) & (df_instrument['exch_seg'] == 'NSE')]
        columns = {'token': 'tokenId', 'symbol': 'symbol', 'name': 'tokenName'}
        df_instrument = df_instrument[df_instrument.columns.intersection(columns)]

        df3min,df15min, df30min, df1hour =ril.get_historial_data(tokens[j])
        print(df3min['total'].max())
        top_ranking_3min.append({
            "name": df_instrument['name'].values[0],
            "ranking_value": df3min['total'].max()
        })
        top_ranking_15min.append({
            "name": df_instrument['name'].values[0],
            "ranking_value": df15min['total'].max()
        })
        top_ranking_30min.append({
            "name": df_instrument['name'].values[0],
            "ranking_value": df30min['total'].max()
        })
        top_ranking_1hour.append({
            "name": df_instrument['name'].values[0],
            "ranking_value": df1hour['total'].max()
        })

        print(df3min['total'].max())
        top_ranking_3min1.append({
            "name": df_instrument['name'].values[0],
            "ranking_value": df3min['total'].min()
        })
        top_ranking_15min1.append({
            "name": df_instrument['name'].values[0],
            "ranking_value": df15min['total'].min()
        })
        top_ranking_30min1.append({
            "name": df_instrument['name'].values[0],
            "ranking_value": df30min['total'].min()
        })
        top_ranking_1hour1.append({
            "name": df_instrument['name'].values[0],
            "ranking_value": df1hour['total'].min()
        })

        # top_ranking_oneday.append({
        #     "name":df_instrument['name'].values[0],
        #     "ranking_value":dfoneday['total'].max()
        # })
        print("----------------3 min --------------------")
        df1 = pd.DataFrame(top_ranking_3min)
        df1 = df1.sort_values(by=['ranking_value'], ascending=False)
        df1.to_csv('/home/edmonster/PycharmProjects/AngelBrokingProjects/test1.csv')
        print(df1)
        print("----------------15 min --------------------")
        df2 = pd.DataFrame(top_ranking_15min)
        df2 = df2.sort_values(by=['ranking_value'], ascending=False)
        df1.to_csv('/home/edmonster/PycharmProjects/AngelBrokingProjects/test2.csv')
        print(df2)
        print("----------------30 min --------------------")
        df3 = pd.DataFrame(top_ranking_30min)
        df3 = df3.sort_values(by=['ranking_value'], ascending=False)
        df1.to_csv('/home/edmonster/PycharmProjects/AngelBrokingProjects/test3.csv')
        print(df3)
        print("----------------1 hour --------------------")
        df4 = pd.DataFrame(top_ranking_1hour)
        df4 = df4.sort_values(by=['ranking_value'], ascending=False)

        print(df4)
        # print("----------------One day --------------------")
        # df5 = pd.DataFrame(top_ranking_oneday)
        # df5 = df5.sort_values(by=['ranking_value'], ascending=False)
        # print(df5)
        print("----------------3 min --------------------")
        df5 = pd.DataFrame(top_ranking_3min1)
        df5 = df5.sort_values(by=['ranking_value'], ascending=False)

        print(df5)
        print("----------------15 min --------------------")
        df6 = pd.DataFrame(top_ranking_15min1)
        df6 = df6.sort_values(by=['ranking_value'], ascending=False)

        print(df6)
        print("----------------30 min --------------------")
        df7 = pd.DataFrame(top_ranking_30min1)
        df7 = df7.sort_values(by=['ranking_value'], ascending=False)

        print(df7)
        print("----------------1 hour --------------------")
        df8 = pd.DataFrame(top_ranking_1hour1)
        df8 = df8.sort_values(by=['ranking_value'], ascending=False)

        print(df8)

        j += 1
        return df1, df2, df3, df4, df5, df6, df7, df8

class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return QtCore.QVariant(str(
                    self._data.iloc[index.row()][index.column()]))
        return QtCore.QVariant()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
