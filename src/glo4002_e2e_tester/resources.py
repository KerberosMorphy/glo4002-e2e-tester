from __future__ import annotations

from dataclasses import asdict
from enum import IntEnum
from pprint import pformat

from httpx import URL, Client, Headers
from rich import print

from .models import (
    Dinosaurs,
    GetDinosaurByNameResponses,
    GetDinosaursResponse,
    GetResourcesResponse,
    PostDinosaursResponses,
    PostResourcesRequest,
    PostResourcesResponses,
    PostTurnResponse,
)

CLIENT = Client(
    headers=Headers({"Content-Type": "application/json"}),
    base_url=URL(url="http://localhost:8181"),
)

TURN_ENDPOINT = "/turn"
RESET_ENDPOINT = "/reset"
RESOURCE_ENDPOINT = "/resources"
DINOSAURS_ENDPOINT = "/dinosaurs"
HEARTBEAT_ENDPOINT = "/heartbeat"


class Status(IntEnum):
    OK = 200
    BAD_REQUEST = 400
    NOT_FOUND = 404


def get_heartbeat(expected_status: Status = Status.OK) -> None:
    response = CLIENT.get(HEARTBEAT_ENDPOINT)

    assert expected_status.value == response.status_code, (
        f"GET `/hearthbeat: Invalid status code {pformat(expected_status, sort_dicts=False)}"
        f" != {pformat(response.status_code, sort_dicts=False)}"
    )
    payload = response.json()
    assert len(payload) == 1, "GET '/heartbeat': Response payload should have only 'time'"
    assert "time" in payload.keys(), "GET '/heartbeat': Response payload should have only 'time'"
    assert isinstance(payload["time"], str), "GET '/heartbeat': 'time' should be a string"


def post_turn(expected_response: PostTurnResponse, expected_status: Status = Status.OK) -> None:
    response = CLIENT.post(TURN_ENDPOINT)
    assert expected_status.value == response.status_code, (
        f"POST '/turn': Invalid status code {pformat(expected_status, sort_dicts=False)}"
        f" != {pformat(response.status_code, sort_dicts=False)}"
    )
    assert asdict(expected_response) == response.json(), (
        f"POST '/turn': Invalid payload\nExpected:\n{pformat(asdict(expected_response), sort_dicts=False)}\n "
        f" !=\nRECEIVED\n{pformat(response.json(), sort_dicts=False)}"
    )


def post_reset(expected_status: Status = Status.OK) -> None:
    response = CLIENT.post(RESET_ENDPOINT)

    assert expected_status.value == response.status_code, (
        f"POST '/reset': Invalid status code {pformat(expected_status, sort_dicts=False)}"
        f" != {pformat(response.status_code, sort_dicts=False)}"
    )


def post_resources(
    request_payload: PostResourcesRequest,
    expected_response: PostResourcesResponses = None,
    expected_status: Status = Status.OK,
) -> None:
    response = CLIENT.post(RESOURCE_ENDPOINT, json=asdict(request_payload))

    assert expected_status.value == response.status_code, (
        f"POST '/resources': Invalid status code {pformat(expected_status, sort_dicts=False)}"
        f" != {pformat(response.status_code, sort_dicts=False)}"
    )
    if expected_response is not None:
        assert asdict(expected_response) == response.json(), (
            "POST '/resources': Invalid"
            f" payload\nExpected:\n{pformat(asdict(expected_response), sort_dicts=False)}\n "
            f" !=\nRECEIVED\n{pformat(response.json(), sort_dicts=False)}"
        )


def get_resources(expected_response: GetResourcesResponse, expected_status: Status = Status.OK) -> None:
    response = CLIENT.get(RESOURCE_ENDPOINT)

    assert expected_status.value == response.status_code, (
        f"GET '/resources': Invalid status code {pformat(expected_status, sort_dicts=False)}"
        f" != {pformat(response.status_code, sort_dicts=False)}"
    )
    if expected_response is not None:
        assert asdict(expected_response) == response.json(), (
            "GET '/resources': Invalid"
            f" payload\nExpected:\n{pformat(asdict(expected_response), sort_dicts=False)}\n "
            f" !=\nRECEIVED\n{pformat(response.json(), sort_dicts=False)}"
        )


def post_dinosaurs(
    request_payload: Dinosaurs,
    expected_response: PostDinosaursResponses = None,
    expected_status: Status = Status.OK,
) -> None:
    response = CLIENT.post(DINOSAURS_ENDPOINT, json=request_payload.to_dict())

    assert expected_status.value == response.status_code, (
        f"POST '/dinosaurs': Invalid status code {pformat(expected_status, sort_dicts=False)}"
        f" != {pformat(response.status_code, sort_dicts=False)}"
    )
    if expected_response is not None:
        assert expected_response.to_dict() == response.json(), (
            "POST '/dinosaurs': Invalid"
            f" payload\nExpected:\n{pformat(expected_response.to_dict(), sort_dicts=False)}\n "
            f" !=\nRECEIVED\n{pformat(response.json(), sort_dicts=False)}"
        )


def get_dinosaur_by_name(
    dinosaur_name: str,
    expected_response: GetDinosaurByNameResponses,
    expected_status: Status = Status.OK,
) -> None:
    response = CLIENT.get(f"{DINOSAURS_ENDPOINT}/{dinosaur_name}")

    assert expected_status.value == response.status_code, (
        f"GET '/dinosaurs/{dinosaur_name}': Invalid status code {pformat(expected_status, sort_dicts=False)}"
        f" != {pformat(response.status_code, sort_dicts=False)}"
    )
    assert expected_response.to_dict() == response.json(), (
        f"GET '/dinosaurs/{dinosaur_name}': Invalid"
        f" payload\nExpected:\n{pformat(expected_response.to_dict(), sort_dicts=False)}\n !="
        f" {pformat(response.json(), sort_dicts=False)}"
    )


def get_dinosaurs(expected_response: GetDinosaursResponse, expected_status: Status = Status.OK) -> None:
    response = CLIENT.get(DINOSAURS_ENDPOINT)

    assert expected_status.value == response.status_code, (
        f"GET '/dinosaurs': Invalid status code {pformat(expected_status, sort_dicts=False)}"
        f" != {pformat(response.status_code, sort_dicts=False)}"
    )

    response_body = response.json()
    expected_dict = [dino.to_dict() for dino in expected_response]
    expected_dinos = [frozenset(dino.items()) for dino in expected_dict]
    received_dinos = [frozenset(dino.items()) for dino in response_body]
    assert len(expected_response) == len(response_body), (
        f"GET '/dinosaurs': Invalid payload\nExpected:\n{pformat(expected_dict, sort_dicts=False)}\n "
        f" !=\nRECEIVED\n{pformat(response_body, sort_dicts=False)}"
    )
    assert expected_dinos == received_dinos, (
        f"GET '/dinosaurs': Invalid payload\nExpected:\n{pformat(expected_dict, sort_dicts=False)}\n "
        f" !=\nRECEIVED\n{pformat(response_body, sort_dicts=False)}"
    )
