import mimetypes
import mimetools

def encode_multipart_formdata(params, files):
    boundary = mimetools.choose_boundary()

    lines = []
    for name in params:
        lines.append("--" + boundary)
        lines.append("Content-Disposition: form-data; name=\"%s\"" % name)
        lines.append("")
        lines.append(str(params[name]))
    for name in files:
        filename = files[name]
        content_type, _ = mimetypes.guess_type(filename)
        if content_type is None:
            content_type = "application/octet-stream"

        lines.append("--" + boundary)
        lines.append("Content-Disposition: form-data; name=\"%s\"; filename=\"%s\"" % (name, filename))
        lines.append("Content-Type: %s" % content_type)
        lines.append("")
        lines.append(open(filename, "rb").read())
    lines.append("--" + boundary + "--")
    lines.append("")

    body = "\r\n".join(lines)
    headers = {'Content-Type': "multipart/form-data; boundary=%s" % boundary,
               'Content-Length': str(len(body))}
    return headers, body
