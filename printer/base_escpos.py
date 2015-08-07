import os
from mchoof.core.get_settings import get_serial_port, get_printer_templates_dir
from escpos import printer
from mako.template import Template
from mako.runtime import Context
from StringIO import StringIO


class SerialEscpos(printer.Serial):

    def write_template(self, template_name, **data):

        template = Template(
            filename=template_name,
            input_encoding='ISO-8859-1'
        )
        buff = StringIO()
        cxt = Context(buff, **data)
        template.render_context(cxt)

        output = str(buff.getvalue())
        self.text(output.encode('latin-1'))


class TemplateEscpos:

    template_name = None

    def __init__(self):

        serial_port = get_serial_port()
        template_dir = get_printer_templates_dir()

        if self.template_name:

            self.template_path = os.path.join(template_dir, self.template_name)
            self.serial_escpos = SerialEscpos(devfile=serial_port)

    def send(self, **data):

        self.serial_escpos.write_template(self.template_path, **data)
