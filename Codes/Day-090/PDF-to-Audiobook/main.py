from pdfToAudio import PDFToAudio


PDFToAudio().pdf_to_audio(pdf_file='book.pdf', lang=PDFToAudio.ENGLISH)


# def text2audiofun(request):
#     language = 'en'
#     music = ''

#     if request.method == 'POST' and request.FILES['pdf']:
#         text = request.POST.get('text')
#         lang = request.POST.get('lang')
#         pdf = request.FILES['pdf'].read()
#         # if pdf available

#         if pdf:
#             pdfReader = PyPDF4.PdfFileReader(io.BytesIO(pdf))
#             content = ''
#             # creating a page object

#             content += pdfReader.getPage(2).extractText() + "\n"
#             text = content
#             myobj = gTTS(text=text, lang=lang, slow=False, )
#             myobj.save("static/speech.mp3")
#             music = 'ok'
#             context = {
#                 'music': music,
#             }
#             return render(request, 'text2audeo.html', context)

#         myobj = gTTS(text=text, lang=lang, slow=False, )
#         myobj.save("static/speech.mp3")
#         music = 'ok'
#         context = {
#             'music': music,
#         }
#         return render(request, 'text2audeo.html', context)

#     context = {
#         'music': music,
#     }
#     return render(request, 'text2audeo.html', context)
