"""Test Axis event class.

pytest --cov-report term-missing --cov=axis.models.event tests/test_event.py
"""

from unittest.mock import patch

import pytest

from axis.models.event import Event, EventOperation

from .event_fixtures import (
    AUDIO_INIT,
    DAYNIGHT_INIT,
    FENCE_GUARD_INIT,
    FIRST_MESSAGE,
    GLOBAL_SCENE_CHANGE,
    LIGHT_STATUS_INIT,
    LOITERING_GUARD_INIT,
    MOTION_GUARD_INIT,
    OBJECT_ANALYTICS_INIT,
    PIR_CHANGE,
    PIR_INIT,
    PORT_0_INIT,
    PORT_ANY_INIT,
    PTZ_MOVE_INIT,
    PTZ_PRESET_INIT_1,
    RELAY_INIT,
    RULE_ENGINE_REGION_DETECTOR_INIT,
    STORAGE_ALERT_INIT,
    VMD3_INIT,
    VMD4_ANY_CHANGE,
    VMD4_ANY_INIT,
)


@pytest.mark.parametrize(
    ("input", "expected"),
    [
        (
            FIRST_MESSAGE,
            {
                "topic": "",
                "source": "",
                "source_idx": "",
                "type": "",
                "state": "",
                "tripped": False,
            },
        ),
        (
            AUDIO_INIT,
            {
                "topic": "onvif:AudioSource/axis:TriggerLevel",
                "source": "channel",
                "source_idx": "1",
                "type": "Sound",
                "state": "0",
                "tripped": False,
            },
        ),
        (
            DAYNIGHT_INIT,
            {
                "topic": "onvif:VideoSource/axis:DayNightVision",
                "source": "VideoSourceConfigurationToken",
                "source_idx": "1",
                "type": "DayNight",
                "state": "1",
                "tripped": True,
            },
        ),
        (
            FENCE_GUARD_INIT,
            {
                "topic": "axis:CameraApplicationPlatform/FenceGuard/Camera1Profile1",
                "source": "",
                "source_idx": "Camera1Profile1",
                "type": "Fence Guard",
                "state": "0",
                "tripped": False,
            },
        ),
        (
            LIGHT_STATUS_INIT,
            {
                "topic": "onvif:Device/axis:Light/Status",
                "source": "id",
                "source_idx": "0",
                "type": "Light",
                "state": "OFF",
                "tripped": False,
            },
        ),
        (
            LOITERING_GUARD_INIT,
            {
                "topic": "axis:CameraApplicationPlatform/LoiteringGuard/Camera1Profile1",
                "source": "",
                "source_idx": "Camera1Profile1",
                "type": "Loitering Guard",
                "state": "0",
                "tripped": False,
            },
        ),
        (
            MOTION_GUARD_INIT,
            {
                "topic": "axis:CameraApplicationPlatform/MotionGuard/Camera1ProfileANY",
                "source": "",
                "source_idx": "Camera1ProfileANY",
                "type": "Motion Guard",
                "state": "0",
                "tripped": False,
            },
        ),
        (
            OBJECT_ANALYTICS_INIT,
            {
                "topic": "axis:CameraApplicationPlatform/ObjectAnalytics/Device1Scenario1",
                "source": "",
                "source_idx": "Device1Scenario1",
                "type": "Object Analytics",
                "state": "0",
                "tripped": False,
            },
        ),
        (
            PIR_INIT,
            {
                "topic": "onvif:Device/axis:Sensor/PIR",
                "source": "sensor",
                "source_idx": "0",
                "type": "PIR",
                "state": "0",
                "tripped": False,
            },
        ),
        (
            PORT_0_INIT,
            {
                "topic": "onvif:Device/axis:IO/Port",
                "source": "port",
                "source_idx": "1",
                "type": "Input",
                "state": "0",
                "tripped": False,
            },
        ),
        (
            PORT_ANY_INIT,
            {
                "topic": "onvif:Device/axis:IO/Port",
                "source": "port",
                "source_idx": "ANY",
                "type": "Input",
                "state": "0",
                "tripped": False,
            },
        ),
        (
            PTZ_MOVE_INIT,
            {
                "topic": "onvif:PTZController/axis:Move/Channel_1",
                "source": "PTZConfigurationToken",
                "source_idx": "1",
                "type": "is_moving",
                "state": "0",
                "tripped": False,
            },
        ),
        (
            PTZ_PRESET_INIT_1,
            {
                "topic": "onvif:PTZController/axis:PTZPresets/Channel_1",
                "source": "PresetToken",
                "source_idx": "1",
                "type": "on_preset",
                "state": "1",
                "tripped": True,
            },
        ),
        (
            RELAY_INIT,
            {
                "topic": "onvif:Device/Trigger/Relay",
                "source": "RelayToken",
                "source_idx": "3",
                "type": "Relay",
                "state": "inactive",
                "tripped": False,
            },
        ),
        (
            VMD3_INIT,
            {
                "topic": "onvif:RuleEngine/axis:VMD3/vmd3_video_1",
                "source": "areaid",
                "source_idx": "0",
                "type": "VMD3",
                "state": "0",
                "tripped": False,
            },
        ),
        (
            VMD4_ANY_INIT,
            {
                "topic": "axis:CameraApplicationPlatform/VMD/Camera1ProfileANY",
                "source": "",
                "source_idx": "Camera1ProfileANY",
                "type": "VMD4",
                "state": "0",
                "tripped": False,
            },
        ),
        # Unsupported event
        (
            GLOBAL_SCENE_CHANGE,
            {
                "topic": "onvif:VideoSource/GlobalSceneChange/ImagingService",
                "source": "Source",
                "source_idx": "0",
                "type": "VMD4",
                "state": "0",
                "tripped": False,
            },
        ),
    ],
)
def test_create_event(input: bytes, expected: tuple) -> None:
    """Verify that a new audio event can be managed."""
    event = Event.decode(input)

    assert event.topic == expected["topic"]
    assert event.source == expected["source"]
    assert event.id == expected["source_idx"]
    assert event.state == expected["state"]
    assert event.is_tripped is expected["tripped"]


@pytest.mark.parametrize(
    ("input", "expected"),
    [
        (
            FIRST_MESSAGE,
            {},
        ),
        (
            PIR_INIT,
            {
                "operation": "Initialized",
                "topic": "onvif:Device/axis:Sensor/PIR",
                "source": "sensor",
                "source_idx": "0",
                "type": "state",
                "value": "0",
            },
        ),
        (
            PIR_CHANGE,
            {
                "operation": "Changed",
                "topic": "onvif:Device/axis:Sensor/PIR",
                "source": "sensor",
                "source_idx": "0",
                "type": "state",
                "value": "1",
            },
        ),
        (
            RULE_ENGINE_REGION_DETECTOR_INIT,
            {
                "operation": "Initialized",
                "source": "VideoSource",
                "source_idx": "0",
                "topic": "onvif:RuleEngine/MotionRegionDetector/Motion",
                "type": "State",
                "value": "0",
            },
        ),
        (
            STORAGE_ALERT_INIT,
            {
                "operation": "Initialized",
                "source": "disk_id",
                "source_idx": "NetworkShare",
                "topic": "axis:Storage/Alert",
                "type": "overall_health",
                "value": "-3",
            },
        ),
        (
            VMD4_ANY_INIT,
            {
                "operation": "Initialized",
                "topic": "axis:CameraApplicationPlatform/VMD/Camera1ProfileANY",
                "source": "",
                "source_idx": "",
                "type": "active",
                "value": "0",
            },
        ),
        (
            VMD4_ANY_CHANGE,
            {
                "operation": "Changed",
                "topic": "axis:CameraApplicationPlatform/VMD/Camera1ProfileANY",
                "source": "",
                "source_idx": "",
                "type": "active",
                "value": "1",
            },
        ),
    ],
)
def test_parse_event_xml(input: bytes, expected: dict):
    """Verify parse_event_xml output."""
    with patch.object(Event, "_decode_from_dict") as mock_decode_from_dict:
        assert Event.decode(input)
        assert mock_decode_from_dict.call_args[0][0] == expected


def test_unknown_event_operation():
    """Verify unknown event operation is caught."""
    assert EventOperation("") == EventOperation.UNKNOWN
