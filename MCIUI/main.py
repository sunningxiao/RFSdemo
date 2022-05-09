



class control:

    def addawg(self, awgname):
        self.awgname = awgname
        self.AWGADD = QtWidgets.QWidget()
        self.AWGADD.setObjectName("AWGADD")
        self.AWG_1.addTab(self.AWGADD, "name".format(self.awgname))

    def addwave(self, chnl_num):
        self.chnl_num = chnl_num
        self.chnl_8.setText("chnlnum".format(chnl_num))
        self.chnl_wave_6.addWidget(SpectrumScreen())



