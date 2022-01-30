import DBAccessor
from docxtpl import DocxTemplate, InlineImage

class AutoDocxTemplate:
    def __init__(self,data,column_names):
        self.title = ""
        self.day = "1"
        self.month = "1"
        self.year = "2001"
        self.table_context = []
        self.template = DocxTemplate(DBAccessor.base_path + r'reports/TemplateDouble.docx')
        # TODO: автоматический template
        
        for row in data:
            context = {}
            for i, col in enumerate(row, start = 1):
                context.update({
                    str(i): col
                })
            self.table_context.append(context)

        self.column_names = column_names

    def render(self):
        context = {
            'title': self.title,
            'day': self.day,
            'month': self.month,
            'year': self.year,
            'table_contents': self.table_context,
            }

        for i, name in enumerate(self.column_names, start=1):
            context.update({
                'column' + str(i): name
                })

        self.template.render(context)
        self.template.save(DBAccessor.base_path + r'reports/' + self.title + '.docx')


class DocxTemplate2(AutoDocxTemplate):
    def __init__(self, data, column_names):
        super().__init__(data, column_names)
        self.template = DocxTemplate(DBAccessor.base_path + r'reports/TemplateDouble.docx')
