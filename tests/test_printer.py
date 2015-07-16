import unittest
from mchoof.printer.base import BasePrinter
from mchoof.printer.base_escpos import SerialEscpos
from mako.template import Template
from mako.runtime import Context
from StringIO import StringIO


SERIAL_PORT = '/dev/ttyUSB0'


# class TestPrinter(unittest.TestCase):
#
#     def setUp(self):
#
#         self.printer = BasePrinter(SERIAL_PORT)
#
#     def tearDown(self):
#
#         del self.printer
#
#     def test_template(self):
#
#         self.printer.write_template(
#             'printer_templates/test_template.ptpl',
#             **{
#                 'name': 'Ricardo',
#                 'lastname': 'Siri'
#             }
#         )
#
#
class TestEscpos(unittest.TestCase):

    def setUp(self):

        self.printer = SerialEscpos(devfile=SERIAL_PORT)

    def tearDown(self):

        del self.printer

    def test_template(self):

        self.printer.write_template(
            'printer_templates/test_escpos.ptpl',
            **{
                'name': 'Ricardo',
                'lastname': 'Siri'
            }
        )


class TestMakoTemplates(unittest.TestCase):

    def test_unicode(self):

        data = {
            'name': 'Richar Siri'
        }

        template = Template(
            filename='printer_templates/test_escpos.ptpl',
            input_encoding='ISO-8859-1'
        )

        buff = StringIO()
        cxt = Context(buff, **data)
        template.render_context(cxt)


if __name__ == '__main__':

    unittest.main()
