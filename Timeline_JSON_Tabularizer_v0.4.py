import json
import csv

def json_to_csv(json_file_path, csv_file_path):
    # Read JSON
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    
    # Prep CSV
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Write headers
        csv_writer.writerow([
            #activitySegments, waypointPaths, simplifiedRawPaths, and placeVisits
            'Object Type',
            'Start Lat', 'Start Lng', 'Start Add.', 'Start Name',
            'End Lat', 'End Lng', 'End Add.', 'End Name',
            'Start', 'End',
            'Activity Dist.',
            'Activity',
            'Activity Conf.',
            'Edit Confirm Status',
            #waypointPaths and simplifiedRawPaths only
            'Acc.',
            'Source',
            'Path Distance',
            #placeVisits only
            'Loc. Conf.', 'Calibrated Prob.',
            'Place Conf.', 'Center Lat', 'Center Lng', 'Visit Conf.', 'Place Loc. Conf.'
        ])

        # Process each timelineObject
        for obj in data.get('timelineObjects', []):
            if 'activitySegment' in obj:
                objectType = 'activitySegment'
                activity_segment = obj['activitySegment']

                #startLocation
                startLat = activity_segment['startLocation'].get('latitudeE7', '')
                startLng = activity_segment['startLocation'].get('longitudeE7', '')
                startAddress = activity_segment['startLocation'].get('address', '')
                startName = activity_segment['startLocation'].get('name', '')

                #endLocation
                endLat = activity_segment['endLocation'].get('latitudeE7', '')
                endLng = activity_segment['endLocation'].get('longitudeE7', '')
                endAddress = activity_segment['endLocation'].get('address', '')
                endName = activity_segment['endLocation'].get('name', '')

                #duration
                startTime = activity_segment['duration'].get('startTimestamp', '')
                endTime = activity_segment['duration'].get('endTimestamp', '')

                distance = activity_segment.get('distance', '')
                activity = activity_segment.get('activityType', '')
                activityConfidence = activity_segment.get('confidence', '')
                editConfirmationStatus = activity_segment.get('editConfirmationStatus', '')

                waypointPath = activity_segment.get('waypointPath', {}).get('waypoints', [])
                simplifiedRawPath = activity_segment.get('simplifiedRawPath', {}).get('points', [])

                csv_writer.writerow([
                    objectType,
                    startLat, startLng, startAddress, startName,
                    endLat, endLng, endAddress, endName,
                    startTime, endTime,
                    distance,
                    activity,
                    activityConfidence,
                    editConfirmationStatus
                ])

                for waypoints in waypointPath:
                    pointLat = waypoints.get('latE7', '')
                    pointLng = waypoints.get('lngE7', '')
                    accuracy = waypoints.get('accuracyMeters', '')

                    source = activity_segment.get('waypointPath', {}).get('source', '')
                    distanceMeters = activity_segment.get('waypointPath', {}).get('distanceMeters', '')
                    travelMode = activity_segment.get('waypointPath', {}).get('travelMode', '')
                    confidence = activity_segment.get('waypointPath', {}).get('confidence', '')

                    csv_writer.writerow([
                        'waypointPath point',
                        pointLat, pointLng, '', '',
                        '', '', '', '',
                        '', '',
                        '',
                        travelMode,
                        confidence,
                        '',
                        accuracy,
                        source,
                        distanceMeters
                    ])

                for point in simplifiedRawPath:

                    pointLat = point.get('latE7', '')
                    pointLng = point.get('lngE7', '')
                    accuracy = point.get('accuracyMeters', '')
                    timestamp = point.get('timestamp', '')

                    source = activity_segment.get('simplifiedRawPath', {}).get('source', '')
                    distanceMeters = activity_segment.get('simplifiedRawPath', {}).get('distanceMeters', '')

                    csv_writer.writerow([
                        'rawPath point',
                        pointLat, pointLng, '', '',
                        '', '', '', '',
                        timestamp,'',
                        '',
                        '',
                        '',
                        '',
                        accuracy,
                        source,
                        distanceMeters
                    ])
                    
            elif 'placeVisit' in obj:
                objectType = 'placeVisit'
                place_visit = obj['placeVisit']

                #location
                placeLat = place_visit['location'].get('latitudeE7', '')
                placeLng = place_visit['location'].get('longitudeE7', '')
                placeAddress = place_visit['location'].get('address', '')
                placeName = place_visit['location'].get('name', '')
                locationLocationConfidence = place_visit['location'].get('locationConfidence', '')
                calibratedProbability = place_visit['location'].get('calibratedProbability', '')

                #duration
                start_time = place_visit['duration'].get('startTimestamp', '')
                end_time = place_visit['duration'].get('endTimestamp', '')

                placeConfidence = place_visit.get('placeConfidence', '')
                centerLatE7 = place_visit.get('centerLatE7', '')
                centerLngE7 = place_visit.get('centerLngE7', '')
                visitConfidence = place_visit.get('visitConfidence', '')
                editConfirmationStatus = place_visit.get('editConfirmationStatus', '')
                placeLocationConfidence = place_visit.get('locationConfidence', '')

                csv_writer.writerow([
                    objectType,
                    placeLat, placeLng, placeAddress, placeName,
                    '', '', '', '',
                    start_time, end_time,
                    '',
                    '',
                    '',
                    editConfirmationStatus,
                    '',
                    '',
                    '',
                    locationLocationConfidence, calibratedProbability,
                    placeConfidence, centerLatE7, centerLngE7, visitConfidence, placeLocationConfidence
                ])

# Example usage
json_file_path = '2022_APRIL.json'
csv_file_path = '2022_APRIL Tabularized.csv'
json_to_csv(json_file_path, csv_file_path)
