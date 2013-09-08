"""
api_activity.py : Trovebox Activity API Classes
"""
from trovebox import http
from trovebox.errors import TroveboxError
from trovebox.objects.activity import Activity
from .api_base import ApiBase

class ApiActivities(ApiBase):
    """ Definitions of /activities/ API endpoints """
    def list(self, filters=None, **kwds):
        """
        Endpoint: /activities/[<filters>]/list.json

        Returns a list of Activity objects.
        The filters parameter can be used to narrow down the activities.
        Eg: filters={"type": "photo-upload"}
        """
        filter_string = self._build_filter_string(filters)
        activities = self._client.get("/activities/%slist.json" % filter_string,
                                      **kwds)["result"]
        activities = http.result_to_list(activities)
        return [Activity(self._client, activity) for activity in activities]

    def purge(self, **kwds):
        """
        Endpoint: /activities/purge.json

        Purges all activities.
        Currently not working due to frontend issue #1368
        """
        if not self._client.post("/activities/purge.json", **kwds)["result"]:
            raise TroveboxError("Purge response returned False")
        return True

class ApiActivity(ApiBase):
    """ Definitions of /activity/ API endpoints """
    def view(self, activity, **kwds):
        """
        Endpoint: /activity/<id>/view.json

        Requests all properties of an activity.
        Returns the requested activity object.
        """
        if not isinstance(activity, Activity):
            activity = Activity(self._client, {"id": activity})
        activity.view(**kwds)
        return activity
