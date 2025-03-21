from aiogram.enums.content_type import ContentType



def get_type(mess):
    match mess.content_type:
        case ContentType.PHOTO:
            return ['photo', mess.photo[-1].file_id]
        case ContentType.AUDIO:
            return ['audio', mess.audio.file_id]
        case ContentType.VIDEO:
            return ['video', mess.video.file_id]
        case ContentType.VOICE:
            return ['voice', mess.voice.file_id]
        case ContentType.VIDEO_NOTE:
            return ['video_note', mess.video_note.file_id]
        case ContentType.DOCUMENT:
            return ['doc', mess.document.file_id]
        case _:
            return ['text', mess.text]