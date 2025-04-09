import os
import shutil
from django.core.management.base import BaseCommand
from chatbot.vector_store_utils import index_all_sources

from chatbot.constants import VECTORSTORE_PATH, REFRESH_FLAG

class Command(BaseCommand):
   help = "Indexes PDF, DOCX, and support website content into vector store"

   def add_arguments(self, parser):
      parser.add_argument(
         REFRESH_FLAG,
         action='store_true',
         help='Delete and recreate the existing vector store before indexing'
      )

   def handle(self, *args, **options):
      if options['refresh']:
         path = VECTORSTORE_PATH
         if os.path.exists(path):
            self.stdout.write("Removing old vector store...")
            shutil.rmtree(path, ignore_errors=True)
            self.stdout.write(self.style.SUCCESS("Old vector store deleted."))

      self.stdout.write("Starting index process...")
      index_all_sources()
      self.stdout.write(self.style.SUCCESS("Vector store created successfully!"))