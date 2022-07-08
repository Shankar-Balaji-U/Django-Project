if file.extension() == ".pdf":
	watermark_pdf = io.BytesIO()

	# Create the PDF object, using the buffer as its "file."
	p = canvas.Canvas(watermark_pdf)

	# Draw things on the PDF. Here's where the PDF generation happens.
	# See the ReportLab documentation for the full list of functionality.
	p.drawString(100, 100, request.user.username)
	p.drawString(100, 110, request.user.email)

	# Close the PDF object cleanly, and we're done.
	p.showPage()
	p.save()

	# FileResponse sets the Content-Disposition header so that browsers
	# present the option to save the file.
	watermark_pdf.seek(0)

	base_file = file.file.path

	# reads the watermark pdf file through 
	# PdfFileReader
	watermark_instance = PdfFileReader(watermark_pdf)

	# fetches the respective page of 
	# watermark(1st page)
	watermark_page = watermark_instance.getPage(0)

	# reads the input pdf file
	pdf_reader = PdfFileReader(base_file)

	# It creates a pdf writer object for the
	# output file
	pdf_writer = PdfFileWriter()

	# iterates through the original pdf to
	# merge watermarks
	for page in range(pdf_reader.getNumPages()):

		page = pdf_reader.getPage(page)

		# will overlay the watermark_page on top 
		# of the current page.
		page.mergePage(watermark_page)

	# add that newly merged page to the
	# pdf_writer object.
	pdf_writer.addPage(page)

	final_pdf = io.BytesIO()
	pdf_writer.write(final_pdf)
	final_pdf.seek(0)

	return FileResponse(final_pdf, as_attachment=False, filename='hello.pdf')