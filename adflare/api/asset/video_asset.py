
class AdflareVideoAsset:

    def __init__(self, client, customer_id):
        self._client = client
        self._customer_id = customer_id

    def upload_videos(self, video_id, title):

        try:
            asset_service = self._client.get_service("AssetService")
            asset_operation = self._client.get_type("AssetOperation")
            asset = asset_operation.create
            asset.type_ = self._client.enums.AssetTypeEnum.YOUTUBE_VIDEO

            asset.youtube_video_asset.youtube_video_title = title
            asset.youtube_video_asset.youtube_video_id = video_id
            asset.name = f'Asset NAme - {title}'

            mutate_asset_response = asset_service.mutate_assets(
                customer_id=self._customer_id, operations=[asset_operation]
            )
            print("Uploaded file(s) Videos:")
            for row in mutate_asset_response.results:
                print(f"\tResource name: {row.resource_name}")

            video_asset_resource_name = mutate_asset_response.results[0].resource_name
            ad_video_asset_1 = self._client.get_type('AdVideoAsset')
            ad_video_asset_1.asset = video_asset_resource_name

            return ad_video_asset_1

        except Exception as ex:
            print('Exception in Video Uploading', ex)