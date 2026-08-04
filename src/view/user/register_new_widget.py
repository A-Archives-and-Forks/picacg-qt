from functools import partial

from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QRegularExpression, Signal, QUrl, QEvent
from PySide6.QtGui import QRegularExpressionValidator, QPixmap, QDesktopServices
from PySide6.QtWidgets import QHBoxLayout, QRadioButton, QCommandLinkButton, QSpacerItem, QSizePolicy, QButtonGroup

from component.label.msg_label import MsgLabel
from qt_owner import QtOwner
from server import req, Status
from config.global_config import GlobalConfig
from config.setting import Setting
from task.qt_task import QtTaskBase
from tools.str import Str


class RegisterNewWidget:
    def __init__(self, owner):
        self.owner = owner
        self.owner.registerButton.clicked.connect(self.ClickButton)
        self.isInit = False

        reg = QRegularExpression("^[A-Z0-9a-z\\.\\_]{1,16}$")
        validator = QRegularExpressionValidator(reg, self.owner.userEdit)
        self.owner.userEdit.setValidator(validator)

    def Init(self):
        return

    def ClickButton(self):
        self.Register()

    def Register(self):
        if not self.owner.sexGroup.checkedButton():
            # QtWidgets.QMessageBox.information(self, '错误', "不能为空", QtWidgets.QMessageBox.Yes)
            QtOwner().ShowError(Str.GetStr(Str.NotSpace))
            return
        if len(self.owner.passwdEdit.text()) < 8:
            # QtWidgets.QMessageBox.information(self, '错误', "密码太短", QtWidgets.QMessageBox.Yes)
            QtOwner().ShowError(Str.GetStr(Str.PasswordShort))
            return
        birthday = self.owner.birthdayEdit.date()
        data = {
            "email": self.owner.userEdit.text(),
            "password": self.owner.passwdEdit.text(),
            "name": self.owner.nameEdit.text(),
            "birthday": birthday.toString("yyyy-MM-dd"),
            "gender": self.owner.sexGroup.checkedButton().objectName().replace("gender_", ""),  # m, f, bot
            "answer1": self.owner.answer1Edit.text(),
            "answer2": self.owner.answer2Edit.text(),
            "answer3": self.owner.answer3Edit.text(),
            "question1": self.owner.question1Edit.text(),
            "question2": self.owner.question2Edit.text(),
            "question3": self.owner.question3Edit.text()
        }
        for v in data.values():
            if not v:
                # QtWidgets.QMessageBox.information(self, '错误', "不能为空", QtWidgets.QMessageBox.Yes)
                QtOwner().ShowError(Str.GetStr(Str.NotSpace))
                return

        QtOwner().ShowLoading()
        self.owner.AddHttpTask(req.RegisterReq(data), self.RegisterBack)
        return

    def RegisterBack(self, raw):
        QtOwner().CloseLoading()
        st = raw["st"]
        if st == Status.Ok:
            # self.close()
            # QtWidgets.QMessageBox.information(self, '注册成功', "注册成功", QtWidgets.QMessageBox.Yes)
            QtOwner().ShowMsg(Str.GetStr(Str.RegisterSuc))
        else:
            msg = raw["data"]
            # QtWidgets.QMessageBox.information(self, '注册失败', msg, QtWidgets.QMessageBox.Yes)
            QtOwner().ShowError(Str.GetStr(st) + "\n" + msg)