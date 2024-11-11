
#TODO imports

if __name__ == "__main__":
    lector = Lector_QR_Reader()
    QR_data = lector.read_QR_Code()
    while QR_data == lector.get_NoRead_item():
        QR_data = lector.read_QR_Code()
    print(f"QR_data: {QR_data}")