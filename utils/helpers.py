from io import BytesIO
import pandas as pd
import openpyxl

def dec_to_bin(value, length):
    return bin(int(value))[2:].zfill(length)

def bin_to_hex(binary_str):
    hex_str = hex(int(binary_str, 2))[2:].upper()
    return hex_str.zfill(len(binary_str) // 4)

def generate_epc(upc, sn):
    gs1_company_prefix = "0" + upc[:6]
    item_reference_number = upc[6:11]
    header = "00110000"
    filter_value = "001"
    partition = "101"
    gs1_binary = dec_to_bin(gs1_company_prefix, 24)
    item_reference_binary = dec_to_bin(item_reference_number, 20)
    serial_binary = dec_to_bin(str(sn), 38)
    epc_binary = header + filter_value + partition + gs1_binary + item_reference_binary + serial_binary
    epc_hex = bin_to_hex(epc_binary)
    return epc_hex

def calculate_adjusted_quantity(qty, two_percent, seven_percent):
    if two_percent:
        qty += int(qty * 0.02)
    elif seven_percent:
        qty += int(qty * 0.07)
    return qty

def generate_excel_file(upc, start_serial, qty, two_percent, seven_percent):
    adjusted_qty = calculate_adjusted_quantity(qty, two_percent, seven_percent)
    
    end_serial = start_serial + adjusted_qty

    epc_values = [generate_epc(upc, sn) for sn in range(start_serial, end_serial)]

    df = pd.DataFrame({                
            'UPC': [upc] * adjusted_qty,
            'Serial': list(range(start_serial, end_serial)),
            'EPC': epc_values,
        })

    excel_file = BytesIO()

    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        worksheet = writer.sheets['Sheet1']
        worksheet.column_dimensions['C'].width = 40

    excel_file.seek(0)

    return excel_file