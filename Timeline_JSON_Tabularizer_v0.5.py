import json
import csv
import os
import datetime
from pathlib import Path
from typing import List, Dict, Any

def parse_datetime(timestamp: str) -> datetime.datetime:
    """Parse a timestamp string into a datetime object for sorting."""
    if not timestamp:
        # Return a very early date for empty timestamps
        return datetime.datetime(1900, 1, 1)
    try:
        return datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        try:
            return datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            # Return a default date if parsing fails
            return datetime.datetime(1900, 1, 1)

def extract_data_from_json(json_file_path: str) -> List[Dict[str, Any]]:
    """Read a JSON file and extract all timeline objects into a list of dictionaries."""
    results = []
    
    # Read JSON
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
    except Exception as e:
        print(f"Error reading {json_file_path}: {e}")
        return []

    # Process each timelineObject
    for obj in data.get('timelineObjects', []):
        if 'activitySegment' in obj:
            objectType = 'activitySegment'
            activity_segment = obj['activitySegment']

            # startLocation
            startLat = activity_segment['startLocation'].get('latitudeE7', '')
            startLng = activity_segment['startLocation'].get('longitudeE7', '')
            startAddress = activity_segment['startLocation'].get('address', '')
            startName = activity_segment['startLocation'].get('name', '')

            # endLocation
            endLat = activity_segment['endLocation'].get('latitudeE7', '')
            endLng = activity_segment['endLocation'].get('longitudeE7', '')
            endAddress = activity_segment['endLocation'].get('address', '')
            endName = activity_segment['endLocation'].get('name', '')

            # duration
            startTime = activity_segment['duration'].get('startTimestamp', '')
            endTime = activity_segment['duration'].get('endTimestamp', '')

            distance = activity_segment.get('distance', '')
            activity = activity_segment.get('activityType', '')
            activityConfidence = activity_segment.get('confidence', '')
            editConfirmationStatus = activity_segment.get('editConfirmationStatus', '')

            results.append({
                'Object Type': objectType,
                'Start Lat': startLat, 
                'Start Lng': startLng, 
                'Start Add.': startAddress, 
                'Start Name': startName,
                'End Lat': endLat, 
                'End Lng': endLng, 
                'End Add.': endAddress, 
                'End Name': endName,
                'Start': startTime, 
                'End': endTime,
                'Activity Dist.': distance,
                'Activity': activity,
                'Activity Conf.': activityConfidence,
                'Edit Confirm Status': editConfirmationStatus,
                'Acc.': '',
                'Source': '',
                'Path Distance': '',
                'Loc. Conf.': '', 
                'Calibrated Prob.': '',
                'Place Conf.': '', 
                'Center Lat': '', 
                'Center Lng': '', 
                'Visit Conf.': '', 
                'Place Loc. Conf.': ''
            })

            waypointPath = activity_segment.get('waypointPath', {}).get('waypoints', [])
            for waypoints in waypointPath:
                pointLat = waypoints.get('latE7', '')
                pointLng = waypoints.get('lngE7', '')
                accuracy = waypoints.get('accuracyMeters', '')

                source = activity_segment.get('waypointPath', {}).get('source', '')
                distanceMeters = activity_segment.get('waypointPath', {}).get('distanceMeters', '')
                travelMode = activity_segment.get('waypointPath', {}).get('travelMode', '')
                confidence = activity_segment.get('waypointPath', {}).get('confidence', '')

                results.append({
                    'Object Type': 'waypointPath point',
                    'Start Lat': pointLat, 
                    'Start Lng': pointLng, 
                    'Start Add.': '', 
                    'Start Name': '',
                    'End Lat': '', 
                    'End Lng': '', 
                    'End Add.': '', 
                    'End Name': '',
                    'Start': '', 
                    'End': '',
                    'Activity Dist.': '',
                    'Activity': travelMode,
                    'Activity Conf.': confidence,
                    'Edit Confirm Status': '',
                    'Acc.': accuracy,
                    'Source': source,
                    'Path Distance': distanceMeters,
                    'Loc. Conf.': '', 
                    'Calibrated Prob.': '',
                    'Place Conf.': '', 
                    'Center Lat': '', 
                    'Center Lng': '', 
                    'Visit Conf.': '', 
                    'Place Loc. Conf.': ''
                })

            simplifiedRawPath = activity_segment.get('simplifiedRawPath', {}).get('points', [])
            for point in simplifiedRawPath:
                pointLat = point.get('latE7', '')
                pointLng = point.get('lngE7', '')
                accuracy = point.get('accuracyMeters', '')
                timestamp = point.get('timestamp', '')

                source = activity_segment.get('simplifiedRawPath', {}).get('source', '')
                distanceMeters = activity_segment.get('simplifiedRawPath', {}).get('distanceMeters', '')

                results.append({
                    'Object Type': 'rawPath point',
                    'Start Lat': pointLat, 
                    'Start Lng': pointLng, 
                    'Start Add.': '', 
                    'Start Name': '',
                    'End Lat': '', 
                    'End Lng': '', 
                    'End Add.': '', 
                    'End Name': '',
                    'Start': timestamp, 
                    'End': '',
                    'Activity Dist.': '',
                    'Activity': '',
                    'Activity Conf.': '',
                    'Edit Confirm Status': '',
                    'Acc.': accuracy,
                    'Source': source,
                    'Path Distance': distanceMeters,
                    'Loc. Conf.': '', 
                    'Calibrated Prob.': '',
                    'Place Conf.': '', 
                    'Center Lat': '', 
                    'Center Lng': '', 
                    'Visit Conf.': '', 
                    'Place Loc. Conf.': ''
                })
                
        elif 'placeVisit' in obj:
            objectType = 'placeVisit'
            place_visit = obj['placeVisit']

            # location
            placeLat = place_visit['location'].get('latitudeE7', '')
            placeLng = place_visit['location'].get('longitudeE7', '')
            placeAddress = place_visit['location'].get('address', '')
            placeName = place_visit['location'].get('name', '')
            locationLocationConfidence = place_visit['location'].get('locationConfidence', '')
            calibratedProbability = place_visit['location'].get('calibratedProbability', '')

            # duration
            start_time = place_visit['duration'].get('startTimestamp', '')
            end_time = place_visit['duration'].get('endTimestamp', '')

            placeConfidence = place_visit.get('placeConfidence', '')
            centerLatE7 = place_visit.get('centerLatE7', '')
            centerLngE7 = place_visit.get('centerLngE7', '')
            visitConfidence = place_visit.get('visitConfidence', '')
            editConfirmationStatus = place_visit.get('editConfirmationStatus', '')
            placeLocationConfidence = place_visit.get('locationConfidence', '')

            results.append({
                'Object Type': objectType,
                'Start Lat': placeLat, 
                'Start Lng': placeLng, 
                'Start Add.': placeAddress, 
                'Start Name': placeName,
                'End Lat': '', 
                'End Lng': '', 
                'End Add.': '', 
                'End Name': '',
                'Start': start_time, 
                'End': end_time,
                'Activity Dist.': '',
                'Activity': '',
                'Activity Conf.': '',
                'Edit Confirm Status': editConfirmationStatus,
                'Acc.': '',
                'Source': '',
                'Path Distance': '',
                'Loc. Conf.': locationLocationConfidence, 
                'Calibrated Prob.': calibratedProbability,
                'Place Conf.': placeConfidence, 
                'Center Lat': centerLatE7, 
                'Center Lng': centerLngE7, 
                'Visit Conf.': visitConfidence, 
                'Place Loc. Conf.': placeLocationConfidence
            })
    
    return results

def process_all_json_files(json_dir: str) -> List[Dict[str, Any]]:
    """Process all JSON files in the given directory and return combined data."""
    all_data = []
    json_dir_path = Path(json_dir)
    
    # Create the directory if it doesn't exist
    if not json_dir_path.exists():
        print(f"Creating directory: {json_dir}")
        json_dir_path.mkdir(parents=True)
        return all_data
    
    # Get all JSON files
    json_files = list(json_dir_path.glob('*.json'))
    
    if not json_files:
        print(f"No JSON files found in {json_dir}")
        return all_data
    
    # Process each JSON file
    for json_file in json_files:
        print(f"Processing {json_file}")
        file_data = extract_data_from_json(str(json_file))
        all_data.extend(file_data)
    
    return all_data

def write_to_csv(data: List[Dict[str, Any]], csv_file_path: str):
    """Write the data to a CSV file."""
    if not data:
        print("No data to write to CSV")
        return
    
    # Get headers from the first item
    headers = list(data[0].keys())
    
    # Write CSV
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Write headers
        csv_writer.writerow(headers)
        
        # Write data rows
        for item in data:
            csv_writer.writerow([item.get(header, '') for header in headers])

def main():
    # Define paths
    json_dir = 'ChrisbonFootprint/JSON'
    output_csv = 'ChrisbonFootprint/Combined_Timeline_Data.csv'
    
    # Process all JSON files
    all_data = process_all_json_files(json_dir)
    
    if all_data:
        # Sort the data by 'Start' column
        sorted_data = sorted(all_data, key=lambda x: parse_datetime(x.get('Start', '')))
        
        # Write to CSV
        write_to_csv(sorted_data, output_csv)
        print(f"Successfully processed {len(all_data)} records from JSON files")
        print(f"Output written to {output_csv}")
    else:
        print("No data was processed.")

if __name__ == "__main__":
    main()
