from PySide6 import QtWidgets
from PySide6.QtCore import Signal, QUrl
from PySide6.QtGui import QDesktopServices

from interface.ui_user_manager_widget import Ui_UserManagerWidget
from qt_owner import QtOwner
from server import req, Status
from task.qt_task import QtTaskBase
from tools.str import Str


class UserChangePasswordWidget:


    def __init__(self, owner):
        self.owner = owner
        self.token = ""
        self.userId = ""
        self.owner.verfyButton.clicked.connect(self.ClickButton)

    def Init(self):
        return

    def ClickButton(self):
        userId = self.owner.userChangeEdit.text()
        old = self.owner.passwordChangeEdit.text()
        new = self.owner.newPasswordEdit.text()
        if self.token and self.userId and self.userId == userId:
            self.ChangePassword(old, new)
        else:
            self.Login()

    def Login(self):
        userId = self.owner.userChangeEdit.text()
        oldPassword = self.owner.passwordChangeEdit.text()
        newPassword = self.owner.newPasswordEdit.text()
        if not userId or not oldPassword or not newPassword:
            QtOwner().ShowMsg(Str.GetStr(Str.NotSpace))
            return
        QtOwner().ShowLoading()
        self.owner.AddHttpTask(req.LoginReq(userId, oldPassword), self.LoginBack, (userId, oldPassword, newPassword))
        return

    def LoginBack(self, raw, v):
        QtOwner().CloseLoading()
        st = raw["st"]
        if st == Status.Ok:
            # QtOwner().ShowMsg(Str.GetStr(Str.RegisterSuc))
            token = raw["token"]
            self.token = token
            userId, oldPassword, newPassword = v
            self.userId = userId
            self.ChangePassword(oldPassword, newPassword)
        else:
            msg = raw["data"]
            QtOwner().ShowError(Str.GetStr(st) + "\n" + msg)

    def ChangePassword(self, oldPassword, newPassword):
        QtOwner().ShowLoading()
        self.owner.AddHttpTask(req.ChangePasswordReq(self.token, oldPassword, newPassword), self.ChangePasswordBack)
        return

    def ChangePasswordBack(self, raw):
        QtOwner().CloseLoading()
        st = raw["st"]
        if st == Status.Ok:
            QtOwner().ShowMsg(Str.GetStr(Str.Ok))
            return
        else:
            msg = raw["data"]
            QtOwner().ShowError(Str.GetStr(st) + "\n" + msg)