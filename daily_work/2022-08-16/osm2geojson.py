      
import argparse
import copy
import json
import sys
import xml.etree.ElementTree as ET
from typing import Union, Set, Dict, List, Any, Tuple, Optional
import re
from tqdm import tqdm
import numpy as np
from collections import defaultdict
from uuid import uuid4
import time
import geojson
import psutil
from types import ModuleType, FunctionType
from gc import get_referents

BLACKLIST = type, ModuleType, FunctionType
def getsize(obj):
    """sum size of object & members."""
    if isinstance(obj, BLACKLIST):
        raise TypeError('getsize() does not take argument of type: '+ str(type(obj)))
    seen_ids = set()
    size = 0
    objects = [obj]
    while objects:
        need_referents = []
        for obj in objects:
            if not isinstance(obj, BLACKLIST) and id(obj) not in seen_ids:
                seen_ids.add(id(obj))
                size += sys.getsizeof(obj)
                need_referents.append(obj)
        objects = get_referents(*need_referents)
    return size

def _get(properties: Dict, key: str) -> Any:
    return properties.get(key, properties.get(f'.{key}'))


def uuid() -> str:
    return str(uuid4())[:8]


def infer_str(text: str, key: str) -> Union[str, int, float, Dict, bool]:
    if key in ('uuid', '.uuid'):
        return text
    is_json_object = text.startswith('{') and text.endswith('}')
    is_json_list = text.startswith('[') and text.endswith(']')
    if is_json_list or is_json_object:
        try:
            return json.loads(text)
        except Exception:
            pass
    if text in ('True', 'False'):
        return text == 'True'
    else:
        try:
            return int(text)
        except Exception:
            try:
                return float(text)
            except Exception:
                return text


def node_properties(node) -> Dict:
    properties = {
        tag.attrib['k']: tag.attrib['v'] for tag in node.findall('tag')
    }
    if any([k.startswith('.') for k in properties.keys()]):
        properties = {(k[1:] if k.startswith('.') else f'{k}'): v
                      for k, v in properties.items()}
    properties = {k: infer_str(v, k) for k, v in properties.items()}
    if 'type' not in properties:
        if 'highway' in properties:
            hihgway_value = properties['highway']
            if hihgway_value == 'lane-centerline':
                properties['type'] = 'road_mark.lane_centerline'
            elif hihgway_value.startswith('lane'):
                properties['type'] = 'road_mark.lane_line'
            elif hihgway_value == 'road-border':
                properties['type'] = 'road_boundary'
        elif 'roadmark' in properties:
            properties['type'] = 'road_mark.stop_line'
    text = json.dumps(properties)
    # if 'type' not in properties.keys():
    #     print('not type')
    if 'LaneBorder' in text:
        # properties.setdefault('type', 'road_mark.lane_line')

        # if 'type' in properties.keys():
        #     if not properties['type'] == 'road_mark.lane_line':
        #         print('LaneBorder type is nq')
        # else:
        #     print('LaneBorder no type')
        properties['type'] = 'road_mark.lane_line'
    elif 'RoadBorder' in text:
        # if 'type' in properties.keys():
        #     if not properties['type'] == 'road_boundary':
        #         print('RoadBorder type is nq')
        # else:
        #     print('RoadBorder no type')
        # properties.setdefault('type', 'road_boundary')
        properties['type'] = 'road_boundary'
    elif 'pole' in text or 'Pole' in text:
        # if 'type' in properties.keys():
        #     if not properties['type'] == 'pole':
        #         print('Pole type is nq')
        # else:
        #     print('Pole no type')
        # properties.setdefault('type', 'pole')
        properties['type'] = 'pole'
    elif 'sign' in text or 'TrafficSign' in text:
        # if 'type' in properties.keys():
        #     if 'trafficsign.' not in properties['type']:
        #         print('TrafficSign type is nq')
        # else:
        #     print('TrafficSign no type')
        # properties.setdefault('type', 'trafficsign.rectangle')
        if 'Rectangle' in text or 'rectangle' in text:
            properties['type'] = 'trafficsign.rectangle'
        elif 'circle' in text or 'Circle' in text:
            properties['type'] = 'trafficsign.circle'
        elif 'triangle' in text or 'Triangle' in text:
            properties['type'] = 'trafficsign.triangle'
        elif 'diamond' in text or 'Diamond' in text:
            properties['type'] = 'trafficsign.diamond'
    elif 'RoadCenter' in text:
        # if 'type' in properties.keys():
        #     if not properties['type'] == 'roadcenter':
        #         print('RoadCenter type is nq')
        # else:
        #     print('RoadCenter no type')
        # properties.setdefault('type', 'roadcenter')
        properties['type'] = 'roadcenter'
    elif 'LaneCenter' in text:
        # properties.setdefault('type', 'lanecenter')
        properties['type'] = 'lanecenter'
    elif 'RoadMark' in text and 'GuideArrow' in text:
        # if 'type' in properties.keys():
        #     if not properties['type'] == 'road_marking':
        #         print('RoadMark type is nq')
        # else:
        #     print('RoadMark no type')
        # properties.setdefault('type', 'road_marking')
        properties['type'] = 'road_marking'
    elif 'light' in text or 'TrafficLight' in text:
        # properties.setdefault('type', 'trafficlight')
        properties['type'] = 'trafficlight'
    elif 'stop_line' in text or 'StopLine' in text:
        # properties.setdefault('type', 'stop_line')
        properties['type'] = 'stop_line'
    elif 'DashedSegment' in text and 'RoadMark' in text:
        # if 'type' in properties.keys():
        #     if not properties['type'] == 'road_mark.lane_mark.dashed_segment':
        #         print('DashedSegment type is nq')
        # else:
        #     print('DashedSegment no type')
        # properties.setdefault('type', 'road_mark.lane_mark.dashed_segment')
        properties['type'] = 'road_mark.lane_mark.dashed_segment'
    # elif 'crosswalk' in text:
    elif 'Crosswalk' in text and 'RoadMark' in text:
        # properties.setdefault('type', 'crosswalks')
        properties['type'] = 'crosswalk'
    elif 'IndicatedLine' in text and 'RoadMark' in text:
        properties['type'] = 'indicatedline'
    elif 'LateralDecelerationMarking' in text and 'RoadMark' in text:
        properties['type'] = 'lateraldecelerationmarking'
    elif 'OverheadPassage' in text and 'RoadFacility' in text:
        properties['type'] = 'OverheadPassage'
    elif 'StaticBlock' in text:
        properties['type'] = 'StaticBlock'
    elif 'SpeedBump' in text and 'RoadMark' in text:
        properties['type'] = 'SpeedBump'
    elif 'NoParkingZone' in text and 'RoadMark' in text:
        properties['type'] = 'NoParkingZone'
    elif 'GateMachine' in text and 'RoadFacility' in text:
        properties['type'] = 'GateMachine'
    elif 'ConstructionArea' in text and 'AOI' in text:
        properties['type'] = 'ConstructionArea'
    elif 'TollGate' in text and 'AOI' in text:
        properties['type'] = 'TollGate'
    elif 'CentralCircle' in text and 'RoadMark' in text:
        properties['type'] = 'CentralCircle'
    elif 'Intersection' in text and 'AOI' in text:
        properties['type'] = 'Intersection'

    properties.setdefault('type', 'unknown')
    # exit(-1)
    return properties

def set_properties(properties) -> Dict:
    properties = {k: infer_str(v, k) for k, v in properties.items()}
    if 'type' not in properties:
        if 'highway' in properties:
            hihgway_value = properties['highway']
            if hihgway_value == 'lane-centerline':
                properties['type'] = 'road_mark.lane_centerline'
            elif hihgway_value.startswith('lane'):
                properties['type'] = 'road_mark.lane_line'
            elif hihgway_value == 'road-border':
                properties['type'] = 'road_boundary'
        elif 'roadmark' in properties:
            properties['type'] = 'road_mark.stop_line'
    text = json.dumps(properties)
    if 'LaneBorder' in text:
        properties['type'] = 'road_mark.lane_line'
    elif 'RoadBorder' in text:
        properties['type'] = 'road_boundary'
    elif 'pole' in text or 'Pole' in text:
        properties['type'] = 'pole'
    elif 'sign' in text or 'TrafficSign' in text:
        if 'Rectangle' in text or 'rectangle' in text:
            properties['type'] = 'trafficsign.rectangle'
        elif 'circle' in text or 'Circle' in text:
            properties['type'] = 'trafficsign.circle'
        elif 'triangle' in text or 'Triangle' in text:
            properties['type'] = 'trafficsign.triangle'
        elif 'diamond' in text or 'Diamond' in text:
            properties['type'] = 'trafficsign.diamond'
    elif 'RoadCenter' in text:
        properties['type'] = 'roadcenter'
    elif 'LaneCenter' in text:
        properties['type'] = 'lanecenter'
    elif 'RoadMark' in text and 'GuideArrow' in text:
        properties['type'] = 'road_marking'
    elif 'light' in text or 'TrafficLight' in text:
        properties['type'] = 'trafficlight'
    elif 'stop_line' in text or 'StopLine' in text:
        properties['type'] = 'stop_line'
    elif 'DashedSegment' in text and 'RoadMark' in text:
        properties['type'] = 'road_mark.lane_mark.dashed_segment'
    elif 'Crosswalk' in text and 'RoadMark' in text:
        properties['type'] = 'crosswalk'
    elif 'IndicatedLine' in text and 'RoadMark' in text:
        properties['type'] = 'indicatedline'
    elif 'LateralDecelerationMarking' in text and 'RoadMark' in text:
        properties['type'] = 'lateraldecelerationmarking'
    elif 'OverheadPassage' in text and 'RoadFacility' in text:
        properties['type'] = 'OverheadPassage'
    elif 'StaticBlock' in text:
        properties['type'] = 'StaticBlock'
    elif 'SpeedBump' in text and 'RoadMark' in text:
        properties['type'] = 'SpeedBump'
    elif 'NoParkingZone' in text and 'RoadMark' in text:
        properties['type'] = 'NoParkingZone'
    elif 'GateMachine' in text and 'RoadFacility' in text:
        properties['type'] = 'GateMachine'
    elif 'ConstructionArea' in text and 'AOI' in text:
        properties['type'] = 'ConstructionArea'
    elif 'TollGate' in text and 'AOI' in text:
        properties['type'] = 'TollGate'
    elif 'CentralCircle' in text and 'RoadMark' in text:
        properties['type'] = 'CentralCircle'
    elif 'Intersection' in text and 'AOI' in text:
        properties['type'] = 'Intersection'

    properties.setdefault('type', 'unknown')
    return properties

class Osm2Geojson(object):

    def __init__(self):
        pass

    @staticmethod
    def convert(osm_path: str, geojson_path: Optional[str] = None):
        geojson_path = geojson_path or osm_path[:osm_path.rfind('.'
                                                               )] + '.geojson'
        feature_collection = Osm2Geojson.parse(osm_path=osm_path)
        with open(geojson_path, 'w') as f:
            json.dump(feature_collection, f, indent=4)

    @staticmethod
    def convert_dict(osm_path: str)->dict:
        return Osm2Geojson.parse(osm_path=osm_path)

    @staticmethod
    def parse(
            *,
            osm_path: Optional[str] = None,
            osm_doc: Optional[ET.Element] = None,
    ) -> Dict:
        
        # xml_node_list = ['node', 'way', 'relation']
        xml_node_info = ''
        node_info = {}
        way_info = {}
        relation_info = {}
        for event, elem in tqdm(ET.iterparse(osm_path, events=('start',)), 'load osm data'):
            tag = elem.tag
            if 'node' == tag:
                xml_node_info = tag
                id = int(elem.attrib['id'])
                coords = [float(elem.attrib['lon']), float(elem.attrib['lat'])]
                node_info[id] = {}
                node_info[id]['coords'] = coords
                node_info[id]['properties'] = {}
            elif 'way' == tag:
                id = int(elem.attrib['id'])
                xml_node_info = tag
                way_info[id] = {}
                way_info[id]['ref'] = []
                way_info[id]['properties'] = {}
            elif 'relation' == tag:
                xml_node_info = tag
                id = int(elem.attrib['id'])
                relation_info[id] = {}
                relation_info[id]['member'] = {}
                relation_info[id]['member']['node'] = {}
                relation_info[id]['member']['way'] = {}
            else:
                if 'node' == xml_node_info:
                    if 'tag' == tag:
                        if 'ELEVATION' == elem.attrib['k']:
                            # node_info[id]['coords'].append(float(elem.attrib['v']))
                            node_info[id]['coords'].append(0.0)
                        else:
                            k = elem.attrib['k']
                            k = k[1:] if k.startswith('.') else k
                            node_info[id]['properties'][k] = elem.attrib['v']
                elif 'way' == xml_node_info:
                    if 'nd' == tag:
                        way_info[id]['ref'].append(int(elem.attrib['ref']))
                    else:
                        k = elem.attrib['k']
                        k = k[1:] if k.startswith('.') else k
                        way_info[id]['properties'][k] = elem.attrib['v']
                elif 'relation' == xml_node_info:
                    if 'member' == tag:
                        if elem.attrib['role'] in relation_info[id]['member'][elem.attrib['type']].keys():
                            relation_info[id]['member'][elem.attrib['type']][elem.attrib['role']].append(int(elem.attrib['ref']))
                        else:
                            relation_info[id]['member'][elem.attrib['type']][elem.attrib['role']] = []
                            relation_info[id]['member'][elem.attrib['type']][elem.attrib['role']].append(int(elem.attrib['ref']))
                    else:
                        k = elem.attrib['k']
                        k = k[1:] if k.startswith('.') else k
                        relation_info[id][k] = elem.attrib['v']

            elem.clear()
        
        
        meta = json.loads('{}')
        feature_collection = {
            'type': 'FeatureCollection',
            'features': [],
            'properties': {
                'geojson->osm': None,
                'osm->geojson': str(int(time.time() * 1000.0)),
                **meta,
            },
        }
        features = feature_collection['features']
        v_nodes = []
        r_nodes = []
        w_nodes = []
        y_nodes = []
        relation_info_keys = relation_info.keys()
        node_info_keys = node_info.keys()
        way_info_keys = way_info.keys()

        lane_group_info = {}
        lane_group_info_reverse = {}
        way_group_info = {}
        rc_way_group_info_reverse = {}
        lc_way_group_info_reverse = {}
        lc_way_group_info = {}
        node_group_info = {}
        rc_node_group_info_reverse = {}
        lc_node_group_info_reverse = {}
        lc_node_group_info = {}
        for relation_id, sub_relation_info in tqdm(relation_info.items(), 'set relation'):
            members = sub_relation_info['member']
            # 先处理车道线,边缘线
            # 取 lane group,
            relation_type = sub_relation_info['RELATION_TYPE']
            # 找到rc
            if 'LaneGroup' == relation_type:
                other_line_id = []
                if len(members['way']):
                    for member in members['way']['lgm']:
                        if 'LINE_TYPE' in way_info[member]['properties'].keys():
                            line_type = way_info[member]['properties']['LINE_TYPE']
                            if 'RoadCenter' == line_type:
                                rc_id = member
                            else:
                                other_line_id.append(member)
                            # elif 'RoadBorder' == line_type:
                            #     other_line_id.append(member)
                            # elif 'LaneBorder' == line_type:
                            #     other_line_id.append(member)
                    if rc_id:
                        lane_group_info[rc_id] = other_line_id
            # 找到pole
            if 'ObjectImpact' == relation_type:
                impact_type = sub_relation_info['IMPACT_TYPE']
                sub_type = sub_relation_info['SUB_TYPE']
                if 'RoadCenter' == impact_type:
                    rc_id = members['way']['impacted'][0]
                    # _ids = []
                    if 'PoleImpact' == sub_type or 'TrafficSignImpact' == sub_type:
                        for member in members['node']['object']:
                            if member in rc_node_group_info_reverse.keys():
                                rc_node_group_info_reverse[member].append(rc_id)
                            else:
                                rc_node_group_info_reverse[member] = [rc_id]
                    elif 'RoadMarkImpact' == sub_type:
                        for member in members['way']['object']:
                            if member in rc_way_group_info_reverse.keys():
                                rc_way_group_info_reverse[member].append(rc_id)
                            else:
                                rc_way_group_info_reverse[member] = [rc_id]
                elif 'LaneCenter' == impact_type:
                    lc_id = members['way']['impacted'][0]
                    object_ids = []
                    if 'PoleImpact' == sub_type or 'TrafficSignImpact' == sub_type:
                        for member in members['node']['object']:
                            if member in lc_node_group_info_reverse.keys():
                                lc_node_group_info_reverse[member].append(lc_id)
                            else:
                                lc_node_group_info_reverse[member] = [lc_id]
                            object_ids.append(member)
                        lc_node_group_info[lc_id] = object_ids
                    elif 'RoadMarkImpact' == sub_type:
                        for member in members['way']['object']:
                            # if member in lc_way_group_info_reverse.keys():
                            #     lc_way_group_info_reverse[member].append(lc_id)
                            # else:
                            #     lc_way_group_info_reverse[member] = [lc_id]
                            object_ids.append(member)
                        lc_way_group_info[lc_id] = object_ids

            

        for rc_id, other_line_ids in lane_group_info.items():
            for other_line_id in other_line_ids:
                lane_group_info_reverse[other_line_id] = rc_id
        for lc_id, object_ids in lc_node_group_info.items():
            if lc_id in lane_group_info_reverse.keys():
                rc_id = lane_group_info_reverse[lc_id]
                for object_id in object_ids:
                    lc_node_group_info_reverse[object_id] = rc_id
        for lc_id, object_ids in lc_way_group_info.items():
            if lc_id in lane_group_info_reverse.keys():
                rc_id = lane_group_info_reverse[lc_id]
                for object_id in object_ids:
                    if object_id in lc_way_group_info_reverse.keys():
                        lc_way_group_info_reverse[object_id].append(rc_id)
                    else:
                        lc_way_group_info_reverse[object_id] = [rc_id]
            

        for node_id, sub_node_info in tqdm(node_info.items(), 'set node properties'):
            properties = set_properties(sub_node_info['properties'])
            properties['id'] = 'n' + str(node_id)
            node_info[node_id]['properties'] = properties
        for way_id, sub_way_info in tqdm(way_info.items(), 'set way feature'):
            coords = []
            nds = sub_way_info['ref']
            if len(nds) == 0:
                continue
            for node_id in nds:
                if node_id in node_info_keys:
                    coords.append(node_info[node_id]['coords'])
            properties = set_properties(sub_way_info['properties'])
            properties['id'] = 'w' + str(way_id)
            if way_id in lane_group_info_reverse.keys():
                rc_id = lane_group_info_reverse[way_id]
                properties['rc_id'] = rc_id
            elif way_id in lc_way_group_info_reverse.keys():
                rc_id = lc_way_group_info_reverse[way_id]
                properties['rc_id'] = rc_id
            elif way_id in rc_way_group_info_reverse.keys():
                rc_id = rc_way_group_info_reverse[way_id]
                properties['rc_id'] = rc_id
            # way_info[way_id]['properties'] = properties

            features.append({
                'type': 'Feature',
                'geometry': {
                    'type': 'LineString',
                    'coordinates': coords,
                },
                'properties': properties,
            })
            # 用于查找虚实变化点
            if 'LANE_BORDER_TYPE' in properties.keys():
                status = properties['LANE_BORDER_TYPE']
                start_node = nds[0]
                end_node = nds[-1]

                if status == 1:#实线
                    r_nodes.append(start_node)
                    r_nodes.append(end_node)
                elif status == 2:#虚线
                    v_nodes.append(start_node)
                    v_nodes.append(end_node)
            # 用于查找颜色变化点
            if 'LANE_BORDER_COLOR' in properties.keys():
                color = properties['LANE_BORDER_COLOR']
                start_node = nds[0]
                end_node = nds[-1]
                if color == 1: #白线
                    w_nodes.append(start_node)
                    w_nodes.append(end_node)
                elif color == 2: # 黄线、
                    y_nodes.append(start_node)
                    y_nodes.append(end_node)
            # 用于查找纵向减速标线
            if 'LONGITUDINAL_DECELERATION_MARK' in properties.keys():
                if properties['LONGITUDINAL_DECELERATION_MARK'] != "None":
                    longitudinaldecelerationmarking_properties = copy.deepcopy(properties)
                    longitudinaldecelerationmarking_properties['type']='longitudinaldecelerationmarking'
                    features.append({
                        'type': 'Feature',
                        'geometry': {
                            'type': 'LineString',
                            'coordinates': coords,
                        },
                        'properties': longitudinaldecelerationmarking_properties,
                    })

        # 检查重复的点，重复点即为虚实变化点
        set_v_nodes = set(v_nodes)
        set_r_nodes = set(r_nodes)
        v_r_change_points = list(set_v_nodes.intersection(set_r_nodes))

        # 检查重复的点，重复点即为颜色变化点
        set_w_nodes = set(w_nodes)
        set_y_nodes = set(y_nodes)
        w_y_change_points = list(set_w_nodes.intersection(set_y_nodes))

        uuid2dashed_segment = defaultdict(dict)
        for id, sub_node_info in tqdm(node_info.items(), 'set node feature'):
            lla = sub_node_info['coords']
            properties = sub_node_info['properties']
            properties.pop('ele', None)
            properties.pop('.ele', None)
            if properties.get('type') == 'unknown':
                if id in v_r_change_points:
                    # 虚实变化点
                    properties['type']='v_r_change_point'
                    geometry_type = 'MultiPoint'
                    features.append({
                        'type': 'Feature',
                        'geometry': {
                            'type': geometry_type,
                            'coordinates': [lla],
                        },
                        'properties': properties,
                    })
                if id in w_y_change_points:
                    # 颜色变化点
                    properties['type']='w_y_change_point'
                    geometry_type = 'MultiPoint'
                    features.append({
                        'type': 'Feature',
                        'geometry': {
                            'type': geometry_type,
                            'coordinates': [lla],
                        },
                        'properties': properties,
                    })
            
            if len(properties) == 1 and properties.get('type') == 'unknown':
                continue
            keypoints = _get(properties, 'keypoints') or _get(
                properties, 'KEY_POINTS')
            if keypoints:
                floats = [
                    float(x) for x in re.findall(
                        r'([-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?)',
                        keypoints)
                ]
                keypoints = np.array(floats).reshape((-1, 3)).tolist()
                
                if not 0 == keypoints[0][0]:
                    keypoints = [[p[0], p[1], 0] for p in keypoints]
            geometry_type = 'Point' if properties.get(
                'type') == 'frame' else 'MultiPoint'
            coordinates = keypoints or [lla]
            if geometry_type == 'Point':
                coordinates = coordinates[0]
            if properties.get('type') == 'road_mark.lane_mark.dashed_segment':
                uuid2dashed_segment[properties['.uuid']][
                    properties['.position']] = coordinates[0], properties
                continue
            
            if id in rc_node_group_info_reverse.keys():
                rc_id = rc_node_group_info_reverse[id]
                properties['rc_id'] = rc_id
            elif id in lc_node_group_info_reverse.keys():
                rc_id = lc_node_group_info_reverse[id]
                properties['rc_id'] = rc_id

            features.append({
                'type': 'Feature',
                'geometry': {
                    'type': geometry_type,
                    'coordinates': coordinates,
                },
                'properties': properties,
            })
        
        for uid, seg in tqdm(uuid2dashed_segment.items(), 'set uuid2dasded_segment'):
            if len(seg) != 2:
                print(
                    f'something went wrong, nonpaired dashed segment, skip uuid:{uid}, seg:{seg}'
                )
                continue
            lla_s, endpoint_s = seg['start']
            lla_e, endpoint_e = seg['end']
            properties = {
                '.uuid': uid,
            }
            for k, v in endpoint_s.items():
                if k not in endpoint_e:
                    properties[k] = v
                    continue
                v2 = endpoint_e.pop(k)
                if v == v2:
                    properties[k] = v
                else:
                    properties[k] = [v, v2]
            properties.update(endpoint_e)
            features.append({
                'type': 'Feature',
                'geometry': {
                    'type': 'MultiPoint',
                    'coordinates': [lla_s, lla_e],
                },
                'properties': properties,
            })
        
        id2count = defaultdict(int)
        for feature in tqdm(features, 'set id'):
            feature['properties'].setdefault('id', f'landmark#{uuid()}')
            if feature['properties']['type'] == 'longitudinaldecelerationmarking':
                feature['properties']['id'] = f'longitudinaldecelerationmarking_landmark#{uuid()}'
            feature_id = feature['properties']['id']
            if feature_id in id2count:
                feature['properties'][
                    'id'] = f'{feature_id}_dup#{id2count[feature_id]}'
            id2count[feature_id] += 1
            feature_type = feature['properties']['type']
            if not isinstance(feature_type, str):
                feature['properties']['type'] = str(feature_type)
        feature_collection_size = getsize(feature_collection)
        free_mem = psutil.virtual_memory().free
        print('feature_collection_size:{}, system_free_memory:{}'.format(feature_collection_size, free_mem))
        feature_collection_json = json.dumps(feature_collection)
        feature_collection_json_size = getsize(feature_collection_json)
        free_mem = psutil.virtual_memory().free
        print('feature_collection_json_size:{}, system_free_memory:{}'.format(feature_collection_json_size, free_mem))
        geojson_info = geojson.loads(feature_collection_json)
        geojson_info_size = getsize(geojson_info)
        free_mem = psutil.virtual_memory().free
        print('geojson_info_size:{}, system_free_memory:{}'.format(geojson_info_size, free_mem))
        return geojson_info


if __name__ == '__main__':
    prog = 'python -m geojson2osm'
    description = ('convert osm map to geojson format')
    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.add_argument(
        'input_osm_path',
        type=str,
        help='input osm file path',
    )
    parser.add_argument(
        'output_geojson',
        nargs='?',
        type=str,
        default=None,
        help='output geojson path',
    )
    args = parser.parse_args()
    # args = parser.parse_args(args=[])
    Osm2Geojson.convert(args.input_osm_path, args.output_geojson)

    