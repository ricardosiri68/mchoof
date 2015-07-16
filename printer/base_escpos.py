from escpos import printer
from mako.template import Template
from mako.runtime import Context
from StringIO import StringIO


class SerialEscpos(printer.Serial):

    def write_template(self, template_name, **data):

        for i in range(100):
            self._raw('\xa4')

        template = Template(
            filename=template_name,
            input_encoding='ISO-8859-1'
        )
        buff = StringIO()
        cxt = Context(buff, **data)
        template.render_context(cxt)

        self.text(str(buff.getvalue()))
