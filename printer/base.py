import serial
from mako.template import Template
from mako.runtime import Context
from StringIO import StringIO


class BasePrinter(serial.Serial):

    def write_line(self, line):

        self.write(line)

    def write_template(self, template_name, **data):

        template = Template(filename=template_name)
        buff = StringIO()
        cxt = Context(buff, **data)
        template.render_context(cxt)

        self.write(str(buff.getvalue()))

        print self.inWaiting()

    def __del__(self):

        self.close()
