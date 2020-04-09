from django.shortcuts import render
from django.template import RequestContext
from imgpro.forms import UploadFileForm
import wget
from .models import ImageFile
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from PIL import Image, ImageOps,ImageFilter

def applyfilter(image_url, preset, filename):
	inputfile = image_url #"'/home/arshdeep/django/imagepro/media/' +"
	f=filename.split('.')
	outputfilename = f[0] + '-out.jpg'

	outputfile = outputfilename #" '/home/arshdeep/django/imagepro/myapp/templates/static/output/' +"

	im = Image.open(inputfile)
	if preset=='gray':
		im = ImageOps.grayscale(im)

	if preset=='edge':
		im = ImageOps.grayscale(im)
		im = im.filter(ImageFilter.FIND_EDGES)

	if preset=='poster':
		im = ImageOps.posterize(im,3)

	if preset=='solar':
		im = ImageOps.solarize(im, threshold=80) 

	if preset=='blur':
		im = im.filter(ImageFilter.BLUR)
	
	if preset=='sepia':
		sepia = []
		r, g, b = (239, 224, 185)
		for i in range(255):
			sepia.extend((r*i/255, g*i/255, b*i/255))
		im = im.convert("L")
		im.putpalette(sepia)
		im = im.convert("RGB")

	im.save(outputfile)
	return outputfilename

def handle_uploaded_file(f, preset,image_url):
	#uploadfilename='media/' + f.name
	#with open(uploadfilename, 'wb+') as destination:
	#	for chunk in f.chunks():
	#		destination.write(chunk)
#
	outputfilename=applyfilter(image_url, preset, f)
	return outputfilename

def home(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			image_file = request.FILES['myfilefield']
			document = ImageFile(myfilefield=image_file)
			document.save()
			image_url = document.myfilefield.url
			preset=request.POST['preset']
			outputfilename = handle_uploaded_file(request.FILES['myfilefield'],preset)
			return render(request, 'process.html',{'outputfilename': outputfilename})
	else:
		form = UploadFileForm() 
	return render(request, 'home.html', {'form': form})

def process(request):
	return render(request,'process.html')
