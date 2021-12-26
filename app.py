import os
from flask import Flask, render_template, request
from flask_ngrok import run_with_ngrok
from werkzeug.utils import secure_filename
import layoutparser as lp
import cv2
ocr_agent = lp.TesseractAgent(languages='eng') 
import time
import tabula
import cv2
import img2pdf
import ocrmypdf
from PIL import Image
app = Flask(__name__)
#run_with_ngrok(app)  # Start ngrok when app is run
@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def uploadfile():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join('static/', secure_filename(f.filename)))	
        image = cv2.imread("static/"+f.filename)
        image = image[..., ::-1] 
        model = lp.Detectron2LayoutModel('lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config', 
                                       extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8],
                                       label_map={0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"})
        layout = model.detect(image)
        id=0
        data=dict()
        for block in layout:
            if block.type=='Text':
                segment_image = (block                       .pad(left=5, right=5, top=5, bottom=5)                       .crop_image(image))
#                time.sleep(2)
                text = ocr_agent.detect(segment_image)
                id+=1
                data['p'+str(id)]=text
            if block.type=='Title':
                segment_image = (block                       .pad(left=5, right=5, top=5, bottom=5)                       .crop_image(image))
                text = ocr_agent.detect(segment_image)
                id+=1
                data['h'+str(id)]=text
            if block.type=='Figure':
                segment_image = (block                       .pad(left=5, right=5, top=5, bottom=5)                       .crop_image(image))
                cv2.imwrite('static/'+str(id)+'table.jpg', segment_image)
                text='static/'+str(id)+'table.jpg'
                id+=1
                data['f'+str(id)]=text
            if block.type=='Table':
                segment_image1 = (block                       .pad(left=5, right=5, top=5, bottom=5)                       .crop_image(image))
                cv2.imwrite('table.jpg', segment_image1)
#                time.sleep(25)
                text='table.jpg'

                image_jpg = Image.open('table.jpg')
                pdf_bytes = img2pdf.convert(image_jpg.filename)
                file = open(str(id)+'img.pdf', "wb")
                file.write(pdf_bytes)
                image_jpg.close()
                file.close()
                ocrmypdf.ocr(str(id)+'img.pdf', 'output.pdf', deskew=True)
                id+=1
                df=tabula.read_pdf("output.pdf",pages="all")
                data['t'+str(id)]=df[0]
    time.sleep(10)
    return render_template('result.html',data=data)

if __name__ == '__main__':
#   app.run()
    app.run()