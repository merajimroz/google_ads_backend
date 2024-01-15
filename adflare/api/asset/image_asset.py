import requests
from PIL import Image
from io import BytesIO
import uuid

class AdflareAdImageAsset:

    def __init__(self, client, customer_id):

        self._client = client
        self._customer_id = customer_id

    def resize_image_to_custom_size(self, width, height, path):
                image = Image.open(path)
                resized_image = image.resize((width, height))

                bytes = BytesIO()
                bytes.seek(0)  # Go to the start of the BytesIO object
                img_bytes = bytes.read()  # Read the bytes

                return img_bytes


    def add_images(self, url, asset_name):
        # url = '/var/www/adflare/backend/google_ads_backend/assets/temp/2.jpg'
        try:
            asset_service = self._client.get_service("AssetService")
            asset_operation = self._client.get_type("AssetOperation")
            asset = asset_operation.create
            asset.type_ = self._client.enums.AssetTypeEnum.IMAGE

            with open(url, 'rb') as image_file:
                image_content = image_file.read()
                # Data field is the raw bytes data of an image.

                image = Image.open(image_file)
                resize = (612, 320)
                resized_image = image.resize(resize)

            img_byte_array = BytesIO()

            # Save the resized image to the BytesIO object in PNG format (you can change the format as needed)
            resized_image.save(img_byte_array, format='PNG')

            # Get the byte contents of the resized image
            img_byte_array.seek(0)  # Go to the start of the BytesIO object
            img_bytes = img_byte_array.read()

            # Data field is the raw bytes data of an image.
            asset.image_asset.data = img_bytes
            asset.image_asset.file_size = len(img_bytes)

            width, height = resized_image.size

            asset.image_asset.full_size.height_pixels = height
            asset.image_asset.full_size.width_pixels = width

            # MIME type of the image (IMAGE_JPEG, IMAGE_PNG, etc.).
            # See more types on the link below.
            # https://developers.google.com/google-ads/api/reference/rpc/v11/MimeTypeEnum.MimeType
            asset.image_asset.mime_type = self._client.enums.MimeTypeEnum.IMAGE_PNG
            # Use your favorite image library to determine dimensions
            
            asset.image_asset.full_size.url = url
            # Provide a unique friendly name to identify your asset.
            # When there is an existing image asset with the same content but a different
            # name, the new name will be dropped silently.
            asset.name = f'{asset_name} - {uuid.uuid4()}'

            mutate_asset_response = asset_service.mutate_assets(
                customer_id=self._customer_id, operations=[asset_operation]
            )

            print("Uploaded file(s) Image marketing images:")
            for row in mutate_asset_response.results:
                print(f"\tResource name: {row.resource_name}")

            image_asset_resource_name = mutate_asset_response.results[0].resource_name
            ad_image_asset = self._client.get_type('AdImageAsset')
            ad_image_asset.asset = image_asset_resource_name

            return ad_image_asset
        
        except Exception as ex:
            print('Exception in Add images', ex)

    def square_marketing_images(self, url, asset_name):
        
        try:
            with open(url, 'rb') as image_file:
                image_content = image_file.read()
                image = Image.open(url)

                resized_image = image.resize((600, 600))

            asset_service = self._client.get_service("AssetService")
            asset_operation = self._client.get_type("AssetOperation")
            asset = asset_operation.create
            asset.type_ = self._client.enums.AssetTypeEnum.IMAGE

            img_byte_array = BytesIO()

            # Save the resized image to the BytesIO object in PNG format (you can change the format as needed)
            resized_image.save(img_byte_array, format='PNG')

            # Get the byte contents of the resized image
            img_byte_array.seek(0)  # Go to the start of the BytesIO object
            img_bytes = img_byte_array.read()

            # Data field is the raw bytes data of an image.
            asset.image_asset.data = img_bytes
            asset.image_asset.file_size = len(img_bytes)

            # MIME type of the image (IMAGE_JPEG, IMAGE_PNG, etc.).
            asset.image_asset.mime_type = self._client.enums.MimeTypeEnum.IMAGE_PNG

            width, height = resized_image.size

            asset.image_asset.full_size.height_pixels = height
            asset.image_asset.full_size.width_pixels = width
            asset.image_asset.full_size.url = url
            asset.name = f'{asset_name} - {uuid.uuid4()}'

            mutate_asset_response = asset_service.mutate_assets(
                customer_id=self._customer_id, operations=[asset_operation]
            )
            print("Uploaded file(s) in Squarre marketing images:")
            for row in mutate_asset_response.results:
                print(f"\tResource name: {row.resource_name}")

            image_asset_resource_name = mutate_asset_response.results[0].resource_name

            ad_image_asset = self._client.get_type('AdImageAsset')
            ad_image_asset.asset = image_asset_resource_name

            return ad_image_asset

        except Exception as ex:
            print('Exception in Square Marketing Images', ex)