"""
api_activity.py : Trovebox Activity API Classes
"""
import json
from trovebox.objects.activity import Activity
from .api_base import ApiBase

class ApiActivities(ApiBase):
    """ Definitions of /activities/ API endpoints """
    def list(self, options=None, **kwds):
        """
        Endpoint: /activities[/<options>]/list.json

        Returns a list of Activity objects.
        The options parameter can be used to narrow down the activities.
        Eg: options={"type": "photo-upload"}
        """
        option_string = self._build_option_string(options)
        activities = self._client.get("/activities%s/list.json" % option_string,
                                      **kwds)["result"]
        activities = self._result_to_list(activities)
        return [Activity(self._client, activity) for activity in activities]

    def purge(self, **kwds):
        """
        Endpoint: /activities/purge.json

        Purges all activities.
        Returns True if successful.
        Raises a TroveboxError if not.
        Currently not working due to frontend issue #1368.
        """
        return self._client.post("/activities/purge.json", **kwds)["result"]

class ApiActivity(ApiBase):
    """ Definitions of /activity/ API endpoints """
    def view(self, activity, **kwds):
        """
        Endpoint: /activity/<id>/view.json

        Requests all properties of an activity.
        Returns the requested activity object.
        """
        result = self._client.get("/activity/%s/view.json" %
                                  self._extract_id(activity),
                                  **kwds)["result"]

        # TBD: Why is the result enclosed/encoded like this?
        result = result["0"]
        result["data"] = json.loads(result["data"])
        return Activity(self._client, result)
