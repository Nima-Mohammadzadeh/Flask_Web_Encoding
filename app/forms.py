from io import BytesIO
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length
import pandas as pd
import openpyxl

class DatabaseForm(FlaskForm):
    serial = IntegerField('Serial Number', render_kw={'readonly': True})

    UPC = StringField('UPC', validators=[
        DataRequired(),
        Length(min=12, max=12, message="UPC must be exactly 12 characters long")
    ])

    quantity = IntegerField('Quantity', validators=[DataRequired()])
    two_percent = BooleanField('2%')
    seven_percent = BooleanField('7%')
    submit = SubmitField('Generate')

    def validate_UPC(self, field):
        if not field.data.isdigit():
            raise ValidationError("UPC must contain only digits")

    @staticmethod
    def dec_to_bin(value, length):
        return bin(int(value))[2:].zfill(length)

    @staticmethod
    def bin_to_hex(binary_str):
        hex_str = hex(int(binary_str, 2))[2:].upper()
        return hex_str.zfill(len(binary_str) // 4)

    def generate_epc(self, sn):
        upc = self.UPC.data
        gs1_company_prefix = "0" + upc[:6]
        item_reference_number = upc[6:11]
        header = "00110000"
        filter_value = "001"
        partition = "101"
        gs1_binary = self.dec_to_bin(gs1_company_prefix, 24)
        item_reference_binary = self.dec_to_bin(item_reference_number, 20)
        serial_binary = self.dec_to_bin(str(sn), 38)
        epc_binary = header + filter_value + partition + gs1_binary + item_reference_binary + serial_binary
        epc_hex = self.bin_to_hex(epc_binary)
        return epc_hex

    def generate_excel_file(self):
        upc = self.UPC.data
        start_serial = int(self.serial.data)
        qty = self.quantity.data
        two_percent = self.two_percent.data
        seven_percent = self.seven_percent.data

        if two_percent:
            qty += int(qty * 0.02)
        elif seven_percent:
            qty += int(qty * 0.07)
        
        end_serial = start_serial + qty

        epc_values = [self.generate_epc(sn) for sn in range(start_serial, end_serial)]

        df = pd.DataFrame({                
                'UPC': [upc] * qty,
                'Serial': list(range(start_serial, end_serial)),
                'EPC': epc_values,
            })

        # Create a BytesIO object
        excel_file = BytesIO()

        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
            worksheet = writer.sheets['Sheet1']
            worksheet.column_dimensions['C'].width = 40

        # move to the beginning of the BytesIO object
        excel_file.seek(0)

        return excel_file