# Django
from django.core.management.base import BaseCommand
from django.db import transaction

# Services
from services.populate import populate_planets, populate_movies, populate_characters

# Utils
from utils.logger import logger


class Command(BaseCommand):
    """
    Custom management command to load Star Wars data into the database.
    
    This command performs the following operations in sequence:
    1. Populates planets data
    2. Populates movies data (including their relationships with planets)
    3. Populates characters data (including their relationships with movies)
    
    All operations are wrapped in a database transaction to ensure data consistency.
    If any operation fails, all changes will be rolled back.
    """
    help = "Load data from Star Wars API (SWAPI) into the database"
    
    @transaction.atomic
    def handle(self, *args, **options):
        """
        Execute the command to load Star Wars data.
        
        The method performs the following steps:
        1. Logs the start of the data loading process
        2. Populates planets data
        3. Populates movies data (with relationships)
        4. Populates characters data (with relationships)
        5. Logs successful completion
        
        In case of any exception during the process:
        - Logs the error with full traceback
        - Outputs the error to stderr
        - Re-raises the exception to trigger transaction rollback
        """
        try:
            logger.info("Starting Star Wars data load...")
            

            populate_planets()
            populate_movies()
            populate_characters()
            
            logger.info("Star Wars data loaded successfully.")
            self.stdout.write(self.style.SUCCESS("Data loaded successfully."))
        except Exception as e:
            logger.error(f"Error loading data: {e}", exc_info=True)
            self.stderr.write(self.style.ERROR(f"Error loading data: {e}"))
            raise
