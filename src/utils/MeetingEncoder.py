import json

from src.model.meeting import Meeting


class MeetingEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Meeting):
            # Convert the Meeting object to a dictionary
            meeting_dict = {
                "requester": obj.requester,
                "reciever": obj.reciever,
                "date": obj.date,
                "status": obj.status
            }
            return meeting_dict
        # For other types, use the default encoder
        return super().default(obj)