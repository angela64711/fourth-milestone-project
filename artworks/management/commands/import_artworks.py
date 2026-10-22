from datetime import date
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from openpyxl import load_workbook

from artworks.models import Artwork, Collection


class Command(BaseCommand):
    """
    Import artwork records and images from the prepared Excel workbook.
    """

    # Django displays this description with:
    # python manage.py help import_artworks
    help = "Import artwork collections and images from Excel."

    def add_arguments(self, parser):
        """
        Define the information the user supplies when running the command.
        """
        parser.add_argument("spreadsheet", type=Path)
        parser.add_argument("images_folder", type=Path)

        # Allows a small trial import before processing the full workbook.
        # Optional: limit the number of rows processed during an import.
        # Usage(windows): python manage.py import_artworks
        #  "C:\..\path to spreadsheet" "C:\..\path to images folder" --limit 3
        parser.add_argument(
            "--limit",
            type=int,
            default=None,
            help="Maximum number of spreadsheet rows to process.",
        )

    def handle(self, *args, **options):
        """
        Django calls handle() when the management command is executed.
        """
        spreadsheet = options["spreadsheet"]
        images_folder = options["images_folder"]
        limit = options["limit"]

        # Stop early if the input files or arguments are invalid.
        if not spreadsheet.is_file():
            raise CommandError(f"Excel file not found: {spreadsheet}")

        if not images_folder.is_dir():
            raise CommandError(f"Images folder not found: {images_folder}")

        if limit is not None and limit < 1:
            raise CommandError("--limit must be a positive number.")

        # Open the workbook for reading only. The original
        #  Excel file will not be modified or saved by this command.
        workbook = load_workbook(
            spreadsheet,
            read_only=True,
            data_only=True,
        )

        try:
            # Select the worksheet tab containing the artwork records.
            sheet_name = "Master Artwork Import"

            if sheet_name not in workbook.sheetnames:
                raise CommandError(f"Worksheet not found: {sheet_name}")

            sheet = workbook[sheet_name]

            # Read the first row as column headings, then use their
            # positions to find values in each subsequent artwork row.
            rows = sheet.iter_rows(values_only=True)
            headers = next(rows, None)

            if not headers:
                raise CommandError("The worksheet is empty.")

            columns = {
                str(name).strip(): index
                for index, name in enumerate(headers)
                if name is not None
            }

            required = [
                "Collection",
                "Artwork title",
                "Year",
                "Description",
                "Expected local image path",
            ]

            # A missing column means the spreadsheet does not match
            # the format expected by this importer.
            for name in required:
                if name not in columns:
                    raise CommandError(f"Missing Excel column: {name}")

            created_collections = 0
            created_artworks = 0
            skipped = 0
            processed = 0

            for row_number, row in enumerate(rows, start=2):

                if limit is not None and processed >= limit:
                    break

                # Ignore completely empty spreadsheet rows.
                if not any(cell is not None for cell in row):
                    continue

                processed += 1

                # Look up a value by column name rather than relying
                # on a fixed column position such as row[0] or row[2].
                def value(column):
                    index = columns[column]
                    return row[index] if index < len(row) else None

                collection_name = str(value("Collection") or "").strip()

                title = str(value("Artwork title") or "").strip()

                image_path = str(value("Expected local image path") or "").strip()

                if not collection_name or not title or not image_path:
                    self.stderr.write(f"Row {row_number}: Missing required data.")
                    skipped += 1
                    continue

                # Existing titles are skipped so rerunning the command
                # does not import the same artwork twice.
                if Artwork.objects.filter(title__iexact=title).exists():
                    self.stdout.write(f"Row {row_number}: Already exists: {title}")
                    skipped += 1
                    continue

                artwork_slug = slugify(title)
                collection_slug = slugify(collection_name)

                # Slugs are also unique in the Django models.
                if (
                    not artwork_slug
                    or Artwork.objects.filter(slug=artwork_slug).exists()
                ):
                    self.stderr.write(
                        f"Row {row_number}: Invalid or duplicate "
                        f"artwork slug for '{title}'."
                    )
                    skipped += 1
                    continue

                if not collection_slug or (
                    Collection.objects.filter(slug=collection_slug)
                    .exclude(name=collection_name)
                    .exists()
                ):
                    # If an image doesn't exist the row is skipped
                    self.stderr.write(f"Row {row_number}: Collection slug conflict.")
                    skipped += 1
                    continue

                # Check that the image path stays inside the supplied
                # images folder and points to an existing file.
                relative_path = Path(image_path)
                full_path = (images_folder / relative_path).resolve()
                images_root = images_folder.resolve()

                if not full_path.is_relative_to(images_root) or not full_path.is_file():
                    self.stderr.write(
                        f"Row {row_number}: Image not found "
                        f"or invalid path: {image_path}"
                    )
                    skipped += 1
                    continue

                # The year is optional, but if supplied it must be
                # a whole year between 2010 and the current year.
                year_value = value("Year")
                year = None

                if year_value is not None and str(year_value).strip():
                    try:
                        numeric_year = float(year_value)

                        if not numeric_year.is_integer():
                            raise ValueError

                        year = int(numeric_year)

                        if not 2010 <= year <= date.today().year:
                            raise ValueError

                    except (ValueError, TypeError, OverflowError):
                        self.stderr.write(
                            f"Row {row_number}: Invalid year: " f"{year_value}"
                        )
                        skipped += 1
                        continue

                description = value("Description")

                # Create the collection only when a valid artwork
                # actually needs it. Existing collections are reused.
                collection, collection_created = Collection.objects.get_or_create(
                    name=collection_name,
                    defaults={
                        "slug": collection_slug,
                        "description": "",
                    },
                )

                if collection_created:
                    created_collections += 1

                artwork = Artwork(
                    title=title,
                    slug=artwork_slug,
                    collection=collection,
                    year=year,
                    description=(str(description) if description is not None else ""),
                )

                # Django's ImageField uses the configured storage
                # backend, so the image is uploaded to Cloudinary.
                with full_path.open("rb") as image_file:
                    artwork.image.save(
                        full_path.name,
                        File(image_file),
                        save=False,
                    )

                # Save the artwork record to the Django database.
                artwork.save()
                created_artworks += 1

                self.stdout.write(f"Imported: {title}")

            # Summarize what happened when the command finishes.
            self.stdout.write(
                self.style.SUCCESS(
                    f"Import finished. "
                    f"Collections created: {created_collections}. "
                    f"Artworks created: {created_artworks}. "
                    f"Rows skipped: {skipped}."
                )
            )

        finally:
            # Close the workbook even if an error interrupts the import.
            workbook.close()
