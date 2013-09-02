"""
api_activity.py : Trovebox Activity API Classes
"""
from trovebox import http
from trovebox.errors import TroveboxError
from trovebox.objects.activity import Activity

class ApiActivities(object):
    """ Definitions of /activities/ API endpoints """
    def __init__(self, client):
        self._client = client

    def list(self, **kwds):
        """ Returns a list of Activity objects """
        activities = self._client.get("/activities/list.json", **kwds)["result"]
        activities = http.result_to_list(activities)
        return [Activity(self._client, activity) for activity in activities]

    def purge(self, **kwds):
        """ Purge all activities """
        if not self._client.post("/activities/purge.json", **kwds)["result"]:
            raise TroveboxError("Purge response returned False")
        return True

class ApiActivity(object):
    """ Definitions of /activity/ API endpoints """
    def __init__(self, client):
        self._client = client

    def view(self, activity, **kwds):
        """
        View an activity's contents.
        Returns the requested activity object.
        """
        if not isinstance(activity, Activity):
            activity = Activity(self._client, {"id": activity})
        activity.view(**kwds)
        return activity
