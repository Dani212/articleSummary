from werkzeug.utils import secure_filename

from ..setup import UPLOAD_FOLDER
import os
import fitz
import docx


class ExtractByFileType:
    __ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

    def __allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in self.__ALLOWED_EXTENSIONS

    def extract_text_by_type(self, request):
        file = request.files.get('file')

        if file and self.__allowed_file(file.filename):
            docx_and_pdf = GetTextByExtension()

            if (file.filename.endswith('.txt')):
                return docx_and_pdf.get_text_from_txt(file=file)
            elif (file.filename.endswith('.docx')):
                return docx_and_pdf.get_text_from_docx(file=file)
            elif (file.filename.endswith('.pdf')):
                return docx_and_pdf.get_text_from_pdf(file=file)


class GetTextByExtension:
    def get_text_from_txt(self, file):
        byte_text = file.read()
        return byte_text.decode("utf-8")

    def get_text_from_docx(self, file):
        filename = secure_filename(file.filename)

        path = os.path.join(UPLOAD_FOLDER, filename)
        # os.path.join is used so that paths work in every operating system
        file.save(path)

        doc = docx.Document(path)

        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)

        return '\n'.join(fullText)

    def get_text_from_pdf(self, file):
        filename = secure_filename(file.filename)

        # os.path.join is used so that paths work in every operating system
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        doc = fitz.open(UPLOAD_FOLDER+"/"+filename)

        text = ''
        for page in doc:
            text += page.get_text().rstrip()

        return text.replace('\n', '')
