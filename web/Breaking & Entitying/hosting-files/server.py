from flask import Flask, request, redirect, make_response, render_template, send_file
import jwt
from lxml import etree
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)

JWT_SECRET = "sillygoose"
JWT_ALGO = "HS256"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    
    # put JWT in a cookie
    payload = {
        "username": "Goose",
        "name": "Goose",
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

    resp = make_response(redirect("/home"))
    resp.set_cookie("token", token)
    return resp

@app.route("/home")
def home():
    #  make sure user is logged in
    token = request.cookies.get("token")
    if not token:
        return redirect("/")
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
    except Exception:
        return redirect("/")
    
    # get name and username from the JWT
    username = decoded.get("username", "None").strip()
    name = decoded.get("name", "None").strip()

    return render_template("home.html", username=username, name=name)

@app.route("/account", methods=["POST"])
def account():
    token = request.cookies.get("token")
    if not token:
        return redirect("/")

    # verify JWT
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
    except Exception:
        return "Invalid token", 403

    if decoded.get("username") != "Admin":
        return "You must be logged in with the username 'Admin' to get your account details", 403

    jwt_username = decoded.get("username")

    # read the POST body
    xml_data = request.data
    if not xml_data:
        return "XML not present in the POST request", 400

    # xml parser
    parser = etree.XMLParser(
        resolve_entities=True,
        load_dtd=True,
        no_network=False
    )

    # parse XML
    try:
        root = etree.fromstring(xml_data, parser)
    except Exception as e:
        return f"Invalid XML: {e}", 400

    xml_username = root.findtext("username")
    xml_name = root.findtext("name")

    # check the username matches in the passed XML and the JWT
    if xml_username.strip() != jwt_username.strip():
        return "Username supplied does not match the username in the JWT", 403

    # generate the PDF
    pdf_buffer = io.BytesIO()
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)

    pdf.setFont("Helvetica-Bold", 24)
    title_text = "Account Details"
    pdf.drawString(72, 720, title_text)
    title_width = pdf.stringWidth(title_text, "Helvetica-Bold", 24)
    pdf.setLineWidth(1)
    pdf.line(72, 716, 72 + title_width, 716)

    pdf.setFont("Helvetica-Bold", 16)
    username_label = "Username:"
    pdf.drawString(72, 672, username_label)
    label_width = pdf.stringWidth(username_label, "Helvetica-Bold", 16)
    pdf.setFont("Helvetica", 16)
    pdf.drawString(72 + label_width + 8, 672, xml_username)
    
    pdf.setFont("Helvetica-Bold", 16)
    name_label = "Name:"
    pdf.drawString(72, 648, name_label)
    label_width = pdf.stringWidth(name_label, "Helvetica-Bold", 16)
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontName = "Helvetica"
    style.fontSize = 15
    style.leading = 18
    style.alignment = TA_LEFT
    max_width = letter[0] - label_width - 152
    para = Paragraph(xml_name, style)
    para.wrapOn(pdf, max_width, 500)
    para.drawOn(pdf, 80 + label_width, 648 - para.height + 15)
    
    pdf.drawImage("pic.png", 172.5, 15, width=250, height=125)

    pdf.save()
    pdf_buffer.seek(0)

    return send_file(
        pdf_buffer,
        download_name="account.pdf",
        mimetype="application/pdf"
    )

@app.route("/logout")
def logout():
    resp = make_response(redirect("/"))
    resp.delete_cookie("token")
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)    
