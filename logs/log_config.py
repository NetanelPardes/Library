import logging

logging.basicConfig(format='%(asctime)s | %(levelname)s |%(message)s' , level=logging.INFO,filename="logs/app.log")
logger = logging.getLogger(__name__)