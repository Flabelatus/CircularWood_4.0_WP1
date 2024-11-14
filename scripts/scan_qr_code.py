import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow.production_run import Lector61x_V2D611D_MMSCE4

if __name__ == "__main__":
    lector = Lector61x_V2D611D_MMSCE4.Lector_QR_Reader()
    QR_data = lector.read_QR_Code()
    while QR_data == lector.get_NoRead_item():
        QR_data = lector.read_QR_Code()
    print(f"QR_data: {QR_data}")