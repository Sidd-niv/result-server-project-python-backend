from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        # add logo in pdf
        self.image('fynd_logo.png', 10, 8, 25)
        # font
        self.set_font('times', 'BU', 30)
        # Title tp the page
        self.cell(0, 10, "Result", ln=True, align="C")
        # line break
        self.ln(20)

    # page footer
    def footer(self):
        # set position for footer
        self.set_y(-15)
        # set font
        self.set_font("times", "B", 10)
        # set page number
        self.cell(0, 10, "Page no.1", align="C")
