
import ftplib, os, sys, re
from smtplib import SMTP_SSL as SMTP
from Settings import ftp_settings, email_settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


address = ftp_settings['address']
username = ftp_settings['username']
password = ftp_settings['password']

email_server = email_settings['server']
email_addr = email_settings['address']
email_pw = email_settings['password']


def upload(input_file, upload_file):
	"""Upload text or binary file to server."""

	print '- connecting...'
	ftp = ftplib.FTP(address)
	ftp.login(username, password)
	ftp.cwd('whitenoiseboutique')

	total_size = os.path.getsize(input_file)

	# print '- uploading (' + str(total_size / 1024.0) + ' kb)...'
	ext = os.path.splitext(input_file)[1]
	if ext in ('.txt', '.html'):
		ftp.storlines('STOR ' + upload_file, open(input_file))
	else:
		upload_progress = UploadProgress(int(total_size))
		ftp.storbinary('STOR ' + upload_file, open(input_file, 'rb'), 1024, upload_progress.handle)

	print '- closing connection...'
	ftp.quit()


class UploadProgress:
	"""Class gives a simple upload progress bar, called by ftplib."""
	size_written = 0
	total_size = 0
	prev_percent = 0

	def __init__(self, total_size):
		self.total_size = total_size
		sys.stdout.write('- uploading: 0% ')

	def handle(self, block):
		self.size_written += 1024
		percent_complete = round((float(self.size_written) / float(self.total_size)) * 100)

		if self.prev_percent != percent_complete:
			self.prev_percent = percent_complete
			if self.prev_percent % 10 == 0:
				if percent_complete == 50:
					sys.stdout.write(' 50% ')
				elif percent_complete >= 100:
					sys.stdout.flush()
					print ' 100%'
				else:
					sys.stdout.write('>')


def send_email(receiver, url, stats, salt):
	"""
	Send email with download link.
	Mostly via: http://stackoverflow.com/a/882770/1167783
	"""

	# header
	msg = MIMEMultipart('alternative')
	msg['Subject'] = 'Your white noise is ready!'
	msg['From'] = 'White Noise Boutique <' + email_addr + '>'
	msg['To'] = receiver

	# text-only version
	text = "Your white noise has been prepared."

	# html version
	html = """
	<html style="font-family:'Open Sans', Helvetica, Arial, sans-serif";>
		<head></head>
		<body>
			<style>
				tr {
					background-color: white;
				}
				tr:hover {
					background-color: rgb(245,245,245);
				}
			</style>
			<h3>Your white noise is ready for download!</h3>
			<p>You selected the generator <strong>""" + stats[0][1] + """</strong> and it has been working hard to produce your white noise: now it's ready! Please use <a href=\"""" + url + """"\">this link to download your file</a> &mdash; it will be deleted after 30 days.</p>"""


	if salt != None:
		html += """<p>The "salt" used in creating your noise's filename: <strong>""" + salt + """</strong>. This can be used to reconstruct your noise's data and should be treated like a secret password, especially if you want to use your noise for cryptographic purposes. Please <a href="http://www.whitenoiseboutique.com/faq">visit the FAQ</a> if you'd like to know more about this.</p>"""

	html += """<p>Here are the results of the statistical tests applied to your unique white noise:</p>"""

	html += """<table style="width:100%; border-collapse:collapse">
					<tr style="border-collapse:collapse">
						<td width="30%" style="border:1px solid rgb(150,150,150); padding:5px"><strong>TESTS</strong></td>
						<td width="30%" style="border:1px solid rgb(150,150,150); padding:5px"><strong>RESULT</strong></td>
						<td width="30%" style="border:1px solid rgb(150,150,150); padding:5px"><strong>PASSED?</strong></td>
					</tr>"""

	for test in stats[1:]:
		test_name = test[0].replace('_', ' ')
		test_name = test_name.title()
		test_name = test_name.replace('Rgb', 'RGB')
		test_name = test_name.replace('Sts', 'STS')

		html += """<tr style="border-collapse:collapse"><td width="30%" style="border:1px solid rgb(150,150,150); padding:5px">""" + test_name + '</td>'
		html += """<td width="30%" style="border:1px solid rgb(150,150,150); padding:5px">""" + str(test[1]) + '</td>'
		html += """<td width="30%" style="border:1px solid rgb(150,150,150); padding:5px">""" + test[2] + '</td>'
		html += '</tr>'

	html += """</table>

			<p>If you have questions about these tests, how your noise was generated, random numbers, or crypography, please <a href="http://www.whitenoiseboutique.com/faq">visit our FAQ</a>.</p>

			<p>&nbsp;</p>
			<!-- <p><img src="http://www.whitenoiseboutique.com/images/Brighton-Digital-Festival-200px.jpg"></p> -->

			<p style="color:rgb(150,150,150)"><em>White Noise Boutique is a project by <a href="http://www.jeffreythompson.org">Jeff Thompson</a> and supported by <a href="http://brightondigitalfestival.co.uk/">Brighton Digital Festival</a>. This is the last email you'll receive from us and we won't share your address with anyone.</em></p>
		</body>
	</html>
	"""

	# add text to email
	msg.attach(MIMEText(text, 'plain'))
	msg.attach(MIMEText(html, 'html'))

	# connect to server
	print '- connecting to server...'
	conn = SMTP(email_server)
	conn.set_debuglevel(False)
	conn.login(email_addr, email_pw)

	# and send it!
	print '- sending...'
	try:
		conn.sendmail(email_addr, receiver, msg.as_string())
	except Exception, e:
		print e

