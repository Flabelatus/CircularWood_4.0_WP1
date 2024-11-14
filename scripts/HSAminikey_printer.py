import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from settings import WorkflowManagerConfig

from workflow.production_run import HSAJETminikeyPrinter

printer_params = WorkflowManagerConfig().get_socket_params()['LABEL_PRINTER']
print(printer_params)

HSAJETminikeyPrinter.Printer(IPadressInput=printer_params['ip'],
      netmaskInput=printer_params['netmask'],
      StringValue="ID 1234567890 abcdefg",
      QRCodeValue="123456789",
      Velocity=3.5,
      Onduration=60)


