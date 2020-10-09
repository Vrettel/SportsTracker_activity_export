########################################################################################################################
## File name     : sports_tracker_api.py
## Date created  : 04/10/2020
## Last update   : 09/10/2020
## Author        : George Vrettos
## Description   : The utility file for the sports tracker api,
##                 containing all the functions used for the API interaction.
########################################################################################################################

# Imports
import requests
import json
import xml.etree.ElementTree as xml
import os
import sys

# Constants
ST_API_PATH = 'https://api.sports-tracker.com/apiserver/v1'
ST_API_EXPORT_PATH = 'https://api.sports-tracker.com/apiserver/v1/workout/exportGpx/'
ST_API_WORKOUT_LIST_PATH = 'https://api.sports-tracker.com/apiserver/v1/workouts'

class SportsTrackerAPI:

    def __init__(self, token=None, out_dir=None):
        print("Initiating Sports Tracker API")

        # Retrieve all the workout keys
        all_workout_keys = self.get_workout_list(token=token)
        # Sort the workouts according to their timestamp
        all_workout_keys.sort(key=lambda x: x.get('startTime'))

        # Creating gpx directory if not exist
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        # Retrieve every workout by their key
        for i in range(len(all_workout_keys)):
            # Save every workout to a separate gpx file
            workout_name_str = "Sports Tracker Activity " + str(i+1)
            with open(out_dir + "/SportsTracker_" + str(i) + ".gpx", 'w+', encoding='utf-8') as f:
                f.write(self.get_single_workout(workout_name= workout_name_str,
                                                workout_key=all_workout_keys[i].get('workoutKey'),
                                                workout_type=all_workout_keys[i].get('activityId'),
                                                token=token))
        print("Operation Completed!")
        print("Workout directory: " + out_dir)

    def get_workout_list (self, url=ST_API_WORKOUT_LIST_PATH, token=None):
        print("Trying to retrieve workout list from: " + url)

        request_payload = {'limited': 'true', 'limit': 1000000}
        request_headers = {'STTAuthorization': token}
        response = json.loads(requests.get(url, headers=request_headers, params=request_payload).text)

        if response['error'] is not None:
            print('Unable to retrieve workout list')
            sys.exit(2)

        workout_key_list = []

        for workout in response['payload']:
            workout_key = workout['workoutKey']
            workout_ts = workout['startTime']
            workout_type = workout['activityId']
            workout_key_list.append({'workoutKey': workout_key,
                                     'startTime': workout_ts,
                                     'activityId': workout_type})
        return workout_key_list

    def get_single_workout (self, url=ST_API_EXPORT_PATH, workout_name="Uncategorized", workout_key=None, workout_type=4, token=None):

        if workout_key is not None:
            print("Trying to retrieve workout " + workout_key + " data from: " + url)
            request_payload = {'token': token}
            raw_text_response = requests.get(url + workout_key, params=request_payload).text
            if raw_text_response is None:
                print('Unable to retrieve workout')
                sys.exit(2)

            # Workout types according to Sports Tracker
            workout_types = {
                0: "walking",
                1: "running",
                2: "cycling",
                4: "other",
                11: "hiking"
            }

            # Trim XML
            xml_namespace_start = raw_text_response.index('xmlns') - 1
            xml_namespace_end = raw_text_response.index('>', xml_namespace_start, len(raw_text_response))
            xml_without_namespace = raw_text_response[0:xml_namespace_start] + raw_text_response[xml_namespace_end:len(raw_text_response)]

            # Format XML and add the 'type' and 'name'
            root = xml.fromstring(xml_without_namespace)

            # Add new elements to the correct place in the XML
            name_element = xml.SubElement(root[1], 'name')
            name_element.text = workout_name
            type_element = xml.SubElement(root[1], 'type')
            type_element.text = workout_types.get(workout_type)
            xml_without_namespace = xml.tostring(root, 'unicode')

            # rejoin namespace
            final_str_with_namespace = raw_text_response[0:xml_namespace_end] + xml_without_namespace[4:len(xml_without_namespace)]
            return final_str_with_namespace
        else:
            print("No workout key specified")
            return ""





