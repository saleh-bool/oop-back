from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
# from .task import add
import logging
logger = logging.getLogger(__name__)
# Create your views here.


def index(request):
 
 message = {
  'message' : "user visits"
 }
 logger.info(message)
 logger.warn("sdjinsvnn")
 return HttpResponse("hello shaghal")
 