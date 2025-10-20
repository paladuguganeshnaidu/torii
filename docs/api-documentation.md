# API Documentation

Base URL: http://127.0.0.1:5000

Content type: All endpoints accept multipart/form-data and respond with HTML containing a <pre> of JSON. The frontend strips the wrapper.

Endpoints

- POST /api/analyze_email
	- form fields: email_file (file: .eml)
	- response: { status, filename, message } or { error }

- POST /api/scan_url
	- form fields: urls (text, newline separated), follow (optional checkbox)
	- response: { count, results: [{ url, ok, status, message }] }

- POST /api/crack_hash
	- form fields: hash (text), wordlist (optional text)
	- response: { hash, wordlist, result, note } or { error }

- POST /api/test_sms
	- form fields: text (text)
	- response: { status, text_preview, spam_score, likely_spam, note } or { error }

- POST /api/analyze_file
	- form fields: file (file)
	- response: { status, filename, size, note } or { error }

- POST /api/recon_target
	- form fields: target (text)
	- response: { target, note } or { error }

- POST /api/detect_stego
	- form fields: image (file: PNG/JPG)
	- response: {
			filename, file_hash, is_stego, detected_methods[], extracted_data,
			risk_level, analysis_details: { lsb?, exif?, statistics? }
		} or { error }

Notes
- In production, consider switching responses to application/json.
- For cross-origin use in dev, CORS is enabled for /api/*.
