from app.client.mysql.mysql_query_dao import insert, get_by_id, \
    search_all_videos_details
from app.vo.video_vo import VideoVO


class VideoDAO:
    @staticmethod
    def insert_video_dao(video_vo_create):
        
        inserted_video_vo = insert(video_vo_create)
        return inserted_video_vo

    @staticmethod
    def get_video_by_id(video_id: int):
        get_video_data = get_by_id(VideoVO, VideoVO.id, video_id)
        return get_video_data

    @staticmethod
    def get_video_search_dtls(search_keyword):
        video_dtls = search_all_videos_details(VideoVO, search_keyword)
        return video_dtls