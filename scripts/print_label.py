import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow.production_run.hsa_jet_mini_printer import InkJetLabelPrinter


def print_label(*args):
      printer = InkJetLabelPrinter()
      printer.print_out(args)


if __name__ == "__main__":

      print_label(
            "ID 1234567890 abcdefg",
            "123456789",
            3.5,
            60
      )
