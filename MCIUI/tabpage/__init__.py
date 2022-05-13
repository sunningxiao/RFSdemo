from PyQt5 import QtWidgets
from MCIUI.tabpage.addtabpage import Ui_addtab
from MCIUI.通道波形 import wave


class Tabadd(QtWidgets.QWidget, Ui_addtab):
    def __init__(self, ui_parent):
        super(Tabadd, self).__init__(ui_parent)
        self.setupUi(self)
        self.ui_parent = ui_parent

        self.frame_2.hide()
        self.frame_4.hide()
        self.comboBox_2.currentIndexChanged.connect(self.trig_mode)
        self.pushButton_2.clicked.connect(self.externalsign)
        self.Trig_2.clicked.connect(self.manualsign)
        self.trig_2.clicked.connect(self.internalsign)
        self.pushButton_4.clicked.connect(self.createpy)

        self.intrigtimes = self.repeat_times_2.text()
        self.intrigcycle = self.trigger_cycle.text()
        self.manualcycle = self.lineEdit_2.text()

        self.tabadd = self.frame_19

    def trig_mode(self, i):
        if i == 1:
            self.internal_trigger()
        elif i == 2:
            self.external_trigger()
        else:
            self.Manaul_trigger()

    def external_trigger(self):
        self.frame_2.show()
        self.frame_4.hide()
        self.frame_38.hide()

    def internal_trigger(self):
        self.frame_4.show()
        self.frame_2.hide()
        self.frame_38.hide()

    def Manaul_trigger(self):
        self.frame_38.show()
        self.frame_2.hide()
        self.frame_4.hide()

    def manualsign(self):
        pass

    def externalsign(self):
        pass

    def internalsign(self):
        pass

    def createpy(self):
        pass

    '''
    def addawg(self, tabname, chnlnum):
        self.tabname = tabname
        self.chnlnum = chnlnum
        self.pagea = Tabadd(self)
        self.AWGADD = QtWidgets.QWidget(self)
        awg_layout = QtWidgets.QGridLayout(self.AWGADD)
        awg_layout.addWidget(self.pagea)
        awg_layout.setContentsMargins(0, 0, 0, 0)
        self.AWGADD.setObjectName("AWGADD")
        from MCIUI.main_widget import MAIN
        self.Main = MAIN(self)
        self.Main.tab.addTab(self.AWGADD, '{}'.format(self.tabname))

        if self.chnlnum != 0:
            self.Main.verticalLayout_6.addWidget(MAIN.waves(self, 2))
            self.chnlnum = self.chnlnum - 1

    def waves(self, chnl_num):
        self.chnl_num = chnl_num
        self.waveui = wave(self)
        self.waveui.chnl_8.setText('{}'.format(chnl_num))
        self.waveui.verticalLayout_2.addWidget(self.wave_form())

    def wave_form(self):
        pass
'''