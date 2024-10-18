from enum import Enum


class VideoResponseMsgEnum(str, Enum):
    UPLOAD_SUCCESS_MSG = "Video Uploaded Successfully!"
    UPLOAD_FAILEd_MSG = "Failed To Upload Video!"
    VIDEO_NOT_FOUND_MSG = "Video Not Found!"
    VIDEO_SEARCH_SUCCESS_MSG = "Fetched Video Search Data Successfully!"
    VIDEO_BLOCKED_DOWNLOAD_ERROR = "The video is blocked and cannot be downloaded."
    VIDEO_BLOCKED_MSG = "Video Blocked Successfully!"
    VIDEO_UNBLOCKED_MSG = "Video UnBlocked Successfully!"
    VIDEO_ALREADY_BLOCKED_MSG = "Video Already Blocked!"

