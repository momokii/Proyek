import gtts
import PyPDF2


class textToSpeech:

    def text_to_speech(text):
        text_audio = gtts.gTTS(text)
        path_save = 'static/speech_output_from_text.mp3'
        text_audio.save(path_save)

        return path_save


    def pdf_to_speech(filepath):
        with open(filepath, "rb") as file:
            file_pdf = PyPDF2.PdfFileReader(file)
            jumlah_halaman_total = file_pdf.numPages

            if (jumlah_halaman_total > 5):
                jumlah_halaman_total = 5
            all_string = ""

            for num_page in range(jumlah_halaman_total):
                string_page = file_pdf.pages[num_page]
                string_page = string_page.extractText()
                all_string += f"{string_page} \n"

        path_save = 'static/speech_output_from_pdf.mp3'
        output_pdf = gtts.gTTS(all_string)
        output_pdf.save(path_save)

        return path_save
