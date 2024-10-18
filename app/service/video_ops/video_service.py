import os
import json
import shutil
import moviepy.editor as moviepy
from fastapi import HTTPException

from app.custom_enum.http_enum import HttpStatusCodeEnum
from app.custom_enum.video_enum import VideoResponseMsgEnum
from app.dao.video.video_dao import VideoDAO
from app.service.common.common_service import AppServices, logger
from app.utils import constant
from app.utils.date_parse_utils import DateParseUtils
from app.vo.video_vo import VideoVO
import redis

REDIS_HOST = constant.REDIS_HOST
REDIS_PORT = constant.REDIS_PORT
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)

class VideoService:
    def __init__(self):
        self.storage_path = "./videos/"
        self.blocked_set = "MI_task"

        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

    async def upload_and_convert(self, video_file):
        try:
            video_path = os.path.join(self.storage_path, video_file.filename)
            with open(video_path, "wb") as buffer:
                shutil.copyfileobj(video_file.file, buffer)
            if 'mp4' not in video_file.content_type:
                logger.info("converting video to mp4")
                mp4_path = video_path.replace(
                    video_file.filename.split('.')[-1], 'mp4')
                video_path = await self.convert_to_mp4_async(video_path,
                                                             mp4_path)
                os.remove(os.path.join(self.storage_path, video_file.filename))

            video_vo = VideoVO()
            video_vo.file_name = video_path.split("/")[-1]
            video_vo.path = video_path
            video_vo.size = video_file.size
            video_vo.is_deleted = False
            video_vo.created_on = DateParseUtils.get_current_epoch()
            video_vo.modified_on = DateParseUtils.get_current_epoch()
            video_dao = VideoDAO()
            inserted_video_dtls = video_dao.insert_video_dao(video_vo)
            if not inserted_video_dtls:
                return AppServices.app_response(
                            HttpStatusCodeEnum.INTERNAL_SERVER_ERROR,
                            VideoResponseMsgEnum.UPLOAD_FAILEd_MSG,
                            success=False,
                            data={})
            video_dict = VideoVO.serialize(inserted_video_dtls)
            return video_dict
        except Exception as exception:
            AppServices.handle_exception(exception, is_raise=True)

    async def convert_to_mp4_async(self,input_path: str, output_path: str):
        """
        Convert a video file to MP4 using moviepy asynchronously.
        """
        try:
            clip = moviepy.VideoFileClip(input_path)
            clip.write_videofile(output_path)
            return output_path
        except Exception as exception:
            AppServices.handle_exception(exception, is_raise=True)

    def get_video_path_by_id(self, video_id: int):
        try:
            video_dao = VideoDAO()
            video_details = video_dao.get_video_by_id(video_id)

            if not video_details or video_details.is_deleted:
                return None

            return video_details.path
        except Exception as exception:
            AppServices.handle_exception(exception, is_raise=True)

    def search_videos_by_metadata(self, search_keyword):
        try:
            video_dao = VideoDAO()
            video_list = video_dao.get_video_search_dtls(search_keyword)

            return video_list
        except Exception as exception:
            AppServices.handle_exception(exception, is_raise=True)

    def block_video(self, video_id: int):
        try:
            video_dao = VideoDAO()
            video = video_dao.get_video_by_id(video_id)

            if video and not video.is_deleted:
                """Check if the video id exist in blocked videos"""
                blocked_videos = self.is_video_blocked(video_id)
                if not blocked_videos:
                    redis_data = redis_client.get(self.blocked_set)

                    if not redis_data:
                        """if the video id doesnot exist in blocked videos add in 
                        redis"""
                        blocked_videos = json.dumps({"blocked_videos": [video_id]})
                        redis_client.set(self.blocked_set, blocked_videos)
                        return True
                    """if the video id  exist in blocked videos append in redis"""
                    redis_data = json.loads(redis_data)
                    blocked_videos = redis_data['blocked_videos']
                    blocked_videos.append(video_id)
                    blocked_videos = json.dumps({"blocked_videos": blocked_videos})
                    redis_client.set(self.blocked_set, blocked_videos)
                    return True
                else:
                    if video_id in blocked_videos:
                        raise HTTPException(
                            status_code=HttpStatusCodeEnum.BAD_REQUEST,
                            detail=VideoResponseMsgEnum.VIDEO_ALREADY_BLOCKED_MSG)
            return False
        except Exception as exception:
            AppServices.handle_exception(exception, is_raise=True)

    def unblock_video(self, video_id: int):
        try:
            blocked_videos = self.is_video_blocked(video_id)
            if not blocked_videos:
                return False
            blocked_videos.remove(video_id)
            blocked_videos = json.dumps({"blocked_videos": blocked_videos})
            redis_client.set(self.blocked_set, blocked_videos)

            return True
        except Exception as exception:
            AppServices.handle_exception(exception, is_raise=True)

    def is_video_blocked(self, video_id: int):
        try:
            redis_data = redis_client.get(self.blocked_set)
            logger.info(f"Redis Data: {redis_data}")
            if not redis_data:
                return False

            redis_data = json.loads(redis_data)
            blocked_videos = redis_data.get("blocked_videos")
            if video_id not in blocked_videos:
                return False

            return blocked_videos
        except Exception as exception:
            AppServices.handle_exception(exception, is_raise=True)

