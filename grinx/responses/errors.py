import os.path
from string import Template

from grinx.responses.base import BaseResponse, AbstractWriter

path_to_error_template = os.path.join(os.path.dirname(__file__), '..', 'base_templates', 'error.html')
with open(path_to_error_template, 'r') as f:
    content = ''.join(f.readlines())

ERROR_TEMPLATE = Template(content)


class ErrorBaseResponse(BaseResponse):
    def write_content(self, writer: AbstractWriter):
        payload = dict(
            error_name=self.status_message,
        )

        if self.content:
            payload['error_content'] = self.content.decode('utf-8')
        else:
            payload['error_content'] = ''

        error_html = ERROR_TEMPLATE.substitute(payload)

        writer(error_html.encode('utf-8'))
