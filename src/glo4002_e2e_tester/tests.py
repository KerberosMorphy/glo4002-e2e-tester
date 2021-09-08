from __future__ import annotations

from collections.abc import Callable, Collection, MutableSequence

from rich import print

from .models import (
    DinoGender,
    Dinosaurs,
    DinoSpecies,
    DuplicateNameError,
    GetResourcesResponse,
    InvalidGenderError,
    InvalidSpeciesError,
    InvalidWeightError,
    PostResourcesRequest,
    PostTurnResponse,
    Resource,
)
from .resources import (
    Status,
    get_dinosaur_by_name,
    get_dinosaurs,
    get_heartbeat,
    get_resources,
    post_dinosaurs,
    post_reset,
    post_resources,
    post_turn,
)

TestStory = Callable[[], None]

_test_stories: MutableSequence[TestStory] = []


def test_turn_reset_turn() -> None:
    get_heartbeat()
    post_reset()
    post_turn(expected_response=PostTurnResponse(turnNumber=1))
    post_reset()
    post_turn(expected_response=PostTurnResponse(turnNumber=1))


def test_4_turn_1_reset_1_turn() -> None:
    get_heartbeat()
    post_reset()
    post_turn(expected_response=PostTurnResponse(turnNumber=1))
    post_turn(expected_response=PostTurnResponse(turnNumber=2))
    post_turn(expected_response=PostTurnResponse(turnNumber=3))
    post_turn(expected_response=PostTurnResponse(turnNumber=4))
    post_reset()
    post_turn(expected_response=PostTurnResponse(turnNumber=1))


def test_mep2_expiration() -> None:
    post_reset()
    post_turn(expected_response=PostTurnResponse(turnNumber=1))
    post_turn(expected_response=PostTurnResponse(turnNumber=2))
    post_turn(expected_response=PostTurnResponse(turnNumber=3))
    post_turn(expected_response=PostTurnResponse(turnNumber=4))
    post_turn(expected_response=PostTurnResponse(turnNumber=5))
    post_turn(expected_response=PostTurnResponse(turnNumber=6))
    post_turn(expected_response=PostTurnResponse(turnNumber=7))
    post_turn(expected_response=PostTurnResponse(turnNumber=8))
    post_turn(expected_response=PostTurnResponse(turnNumber=9))
    post_turn(expected_response=PostTurnResponse(turnNumber=10))
    post_turn(expected_response=PostTurnResponse(turnNumber=11))
    get_resources(
        expected_response=GetResourcesResponse(
            fresh=Resource(qtyBurger=400, qtySalad=750, qtyWater=100000),
            expired=Resource(qtyBurger=700, qtySalad=2000, qtyWater=10000),
            consumed=Resource(qtyBurger=0, qtySalad=0, qtyWater=0),
        )
    )


def test_mep2_res_example() -> None:
    post_reset()
    post_resources(
        request_payload=PostResourcesRequest(qtyBurger=1),
    )
    get_resources(
        expected_response=GetResourcesResponse(
            fresh=Resource(qtyBurger=0, qtySalad=0, qtyWater=0),
            expired=Resource(qtyBurger=0, qtySalad=0, qtyWater=0),
            consumed=Resource(qtyBurger=0, qtySalad=0, qtyWater=0),
        )
    )
    post_turn(expected_response=PostTurnResponse(turnNumber=1))
    get_resources(
        expected_response=GetResourcesResponse(
            fresh=Resource(qtyBurger=101, qtySalad=250, qtyWater=10000),
            expired=Resource(qtyBurger=0, qtySalad=0, qtyWater=0),
            consumed=Resource(qtyBurger=0, qtySalad=0, qtyWater=0),
        )
    )
    post_turn(expected_response=PostTurnResponse(turnNumber=2))
    post_turn(expected_response=PostTurnResponse(turnNumber=3))
    post_turn(expected_response=PostTurnResponse(turnNumber=4))
    post_turn(expected_response=PostTurnResponse(turnNumber=5))
    get_resources(
        expected_response=GetResourcesResponse(
            fresh=Resource(qtyBurger=400, qtySalad=750, qtyWater=50000),
            expired=Resource(qtyBurger=101, qtySalad=500, qtyWater=0),
            consumed=Resource(qtyBurger=0, qtySalad=0, qtyWater=0),
        )
    )


def test_mep2_w_1_dino() -> None:
    dino_alpha = Dinosaurs(
        name="Alpha",
        weight=1,
        gender=DinoGender.MALE,
        species=DinoSpecies.ALLOSAURUS,
    )
    dino_charlie = Dinosaurs(
        name="Charlie",
        weight=1,
        gender=DinoGender.MALE,
        species=DinoSpecies.TRICERATOPS,
    )
    post_reset()
    post_dinosaurs(request_payload=dino_alpha)
    post_dinosaurs(request_payload=dino_charlie)
    post_turn(expected_response=PostTurnResponse(turnNumber=1))
    get_resources(
        expected_response=GetResourcesResponse(
            fresh=Resource(qtyBurger=98, qtySalad=248, qtyWater=9996),
            expired=Resource(qtyBurger=0, qtySalad=0, qtyWater=0),
            consumed=Resource(qtyBurger=2, qtySalad=2, qtyWater=4),
        )
    )
    get_dinosaurs(expected_response=[dino_alpha, dino_charlie])


def test_mep2_res_dino() -> None:
    dino_alpha = Dinosaurs(
        name="Alpha",
        weight=8000,
        gender=DinoGender.MALE,
        species=DinoSpecies.ALLOSAURUS,
    )
    dino_bravo = Dinosaurs(
        name="Bravo",
        weight=30000,
        gender=DinoGender.FEMALE,
        species=DinoSpecies.TYRANNOSAURUS_REX,
    )
    dino_charlie = Dinosaurs(
        name="Charlie",
        weight=40000,
        gender=DinoGender.MALE,
        species=DinoSpecies.TRICERATOPS,
    )
    post_reset()
    post_dinosaurs(request_payload=dino_alpha)
    post_turn(expected_response=PostTurnResponse(turnNumber=1))
    post_resources(request_payload=PostResourcesRequest(qtySalad=2, qtyWater=100000))
    post_resources(request_payload=PostResourcesRequest(qtyBurger=2))
    post_dinosaurs(request_payload=dino_bravo)
    post_dinosaurs(request_payload=dino_charlie)
    get_resources(
        expected_response=GetResourcesResponse(
            fresh=Resource(qtyBurger=84, qtySalad=250, qtyWater=400),
            expired=Resource(qtyBurger=0, qtySalad=0, qtyWater=0),
            consumed=Resource(qtyBurger=16, qtySalad=0, qtyWater=9600),
        )
    )
    get_dinosaurs(expected_response=[dino_alpha])
    post_turn(expected_response=PostTurnResponse(turnNumber=2))
    get_resources(
        expected_response=GetResourcesResponse(
            fresh=Resource(qtyBurger=118, qtySalad=302, qtyWater=21600),
            expired=Resource(qtyBurger=0, qtySalad=0, qtyWater=0),
            consumed=Resource(qtyBurger=84, qtySalad=200, qtyWater=98400),
        )
    )
    get_dinosaurs(expected_response=[dino_bravo, dino_charlie, dino_alpha])
    post_turn(expected_response=PostTurnResponse(turnNumber=3))
    get_resources(
        expected_response=GetResourcesResponse(
            fresh=Resource(qtyBurger=180, qtySalad=452, qtyWater=0),
            expired=Resource(qtyBurger=0, qtySalad=0, qtyWater=0),
            consumed=Resource(qtyBurger=122, qtySalad=300, qtyWater=130000),
        )
    )
    get_dinosaurs(expected_response=[dino_bravo])
    post_turn(expected_response=PostTurnResponse(turnNumber=4))
    get_resources(
        expected_response=GetResourcesResponse(
            fresh=Resource(qtyBurger=250, qtySalad=702, qtyWater=0),
            expired=Resource(qtyBurger=0, qtySalad=0, qtyWater=0),
            consumed=Resource(qtyBurger=152, qtySalad=300, qtyWater=140000),
        )
    )
    get_dinosaurs(expected_response=[])
    post_turn(expected_response=PostTurnResponse(turnNumber=5))
    get_resources(
        expected_response=GetResourcesResponse(
            fresh=Resource(qtyBurger=350, qtySalad=802, qtyWater=10000),
            expired=Resource(qtyBurger=0, qtySalad=150, qtyWater=0),
            consumed=Resource(qtyBurger=152, qtySalad=300, qtyWater=140000),
        )
    )
    get_dinosaurs(expected_response=[])
    post_turn(expected_response=PostTurnResponse(turnNumber=6))
    get_resources(
        expected_response=GetResourcesResponse(
            fresh=Resource(qtyBurger=418, qtySalad=802, qtyWater=20000),
            expired=Resource(qtyBurger=32, qtySalad=400, qtyWater=0),
            consumed=Resource(qtyBurger=152, qtySalad=300, qtyWater=140000),
        )
    )
    get_dinosaurs(expected_response=[])
    post_turn(expected_response=PostTurnResponse(turnNumber=7))
    get_resources(
        expected_response=GetResourcesResponse(
            fresh=Resource(qtyBurger=418, qtySalad=802, qtyWater=30000),
            expired=Resource(qtyBurger=132, qtySalad=650, qtyWater=0),
            consumed=Resource(qtyBurger=152, qtySalad=300, qtyWater=140000),
        )
    )
    get_dinosaurs(expected_response=[])
    post_turn(expected_response=PostTurnResponse(turnNumber=8))
    get_resources(
        expected_response=GetResourcesResponse(
            fresh=Resource(qtyBurger=418, qtySalad=802, qtyWater=40000),
            expired=Resource(qtyBurger=232, qtySalad=900, qtyWater=0),
            consumed=Resource(qtyBurger=152, qtySalad=300, qtyWater=140000),
        )
    )
    get_dinosaurs(expected_response=[])
    post_turn(expected_response=PostTurnResponse(turnNumber=9))
    get_resources(
        expected_response=GetResourcesResponse(
            fresh=Resource(qtyBurger=418, qtySalad=802, qtyWater=50000),
            expired=Resource(qtyBurger=332, qtySalad=1150, qtyWater=0),
            consumed=Resource(qtyBurger=152, qtySalad=300, qtyWater=140000),
        )
    )
    get_dinosaurs(expected_response=[])
    post_turn(expected_response=PostTurnResponse(turnNumber=10))
    get_resources(
        expected_response=GetResourcesResponse(
            fresh=Resource(qtyBurger=418, qtySalad=802, qtyWater=60000),
            expired=Resource(qtyBurger=432, qtySalad=1400, qtyWater=0),
            consumed=Resource(qtyBurger=152, qtySalad=300, qtyWater=140000),
        )
    )
    get_dinosaurs(expected_response=[])
    post_turn(expected_response=PostTurnResponse(turnNumber=11))
    get_resources(
        expected_response=GetResourcesResponse(
            fresh=Resource(qtyBurger=418, qtySalad=802, qtyWater=70000),
            expired=Resource(qtyBurger=532, qtySalad=1650, qtyWater=0),
            consumed=Resource(qtyBurger=152, qtySalad=300, qtyWater=140000),
        )
    )
    get_dinosaurs(expected_response=[])
    post_turn(expected_response=PostTurnResponse(turnNumber=12))
    get_resources(
        expected_response=GetResourcesResponse(
            fresh=Resource(qtyBurger=418, qtySalad=802, qtyWater=80000),
            expired=Resource(qtyBurger=632, qtySalad=1900, qtyWater=0),
            consumed=Resource(qtyBurger=152, qtySalad=300, qtyWater=140000),
        )
    )
    get_dinosaurs(expected_response=[])
    post_turn(expected_response=PostTurnResponse(turnNumber=13))
    get_resources(
        expected_response=GetResourcesResponse(
            fresh=Resource(qtyBurger=418, qtySalad=802, qtyWater=90000),
            expired=Resource(qtyBurger=732, qtySalad=2150, qtyWater=0),
            consumed=Resource(qtyBurger=152, qtySalad=300, qtyWater=140000),
        )
    )
    get_dinosaurs(expected_response=[])
    post_turn(expected_response=PostTurnResponse(turnNumber=14))
    get_resources(
        expected_response=GetResourcesResponse(
            fresh=Resource(qtyBurger=418, qtySalad=802, qtyWater=100000),
            expired=Resource(qtyBurger=832, qtySalad=2400, qtyWater=0),
            consumed=Resource(qtyBurger=152, qtySalad=300, qtyWater=140000),
        )
    )
    get_dinosaurs(expected_response=[])
    post_turn(expected_response=PostTurnResponse(turnNumber=15))
    get_resources(
        expected_response=GetResourcesResponse(
            fresh=Resource(qtyBurger=418, qtySalad=802, qtyWater=100000),
            expired=Resource(qtyBurger=932, qtySalad=2650, qtyWater=10000),
            consumed=Resource(qtyBurger=152, qtySalad=300, qtyWater=140000),
        )
    )
    get_dinosaurs(expected_response=[])


def test_mep2_dino() -> None:
    dino_alpha = Dinosaurs(
        name="Alpha",
        weight=1000,
        gender=DinoGender.MALE,
        species=DinoSpecies.ALLOSAURUS,
    )
    dino_bravo = Dinosaurs(
        name="Bravo",
        weight=2000,
        gender=DinoGender.FEMALE,
        species=DinoSpecies.TYRANNOSAURUS_REX,
    )
    dino_charlie = Dinosaurs(
        name="Charlie",
        weight=3000,
        gender=DinoGender.MALE,
        species=DinoSpecies.TRICERATOPS,
    )
    dino_invalid_gender = Dinosaurs(
        name="Alpha",
        weight=1000,
        gender=DinoGender.INVALID,
        species=DinoSpecies.ALLOSAURUS,
    )
    dino_invalid_weight = Dinosaurs(
        name="Alpha",
        weight=-1000,
        gender=DinoGender.MALE,
        species=DinoSpecies.ALLOSAURUS,
    )
    dino_invalid_species = Dinosaurs(
        name="Alpha",
        weight=1000,
        gender=DinoGender.MALE,
        species=DinoSpecies.INVALID,
    )
    get_heartbeat()
    post_reset()
    get_dinosaurs(expected_response=[])
    post_dinosaurs(request_payload=dino_alpha)
    get_dinosaurs(expected_response=[])
    post_turn(expected_response=PostTurnResponse(turnNumber=1))
    get_dinosaur_by_name(dinosaur_name=dino_alpha.name, expected_response=dino_alpha)
    get_dinosaurs(expected_response=[dino_alpha])
    post_dinosaurs(
        request_payload=dino_invalid_gender,
        expected_response=InvalidGenderError(),
        expected_status=Status.BAD_REQUEST,
    )
    post_dinosaurs(
        request_payload=dino_invalid_weight,
        expected_response=InvalidWeightError(),
        expected_status=Status.BAD_REQUEST,
    )
    post_dinosaurs(
        request_payload=dino_invalid_species,
        expected_response=InvalidSpeciesError(),
        expected_status=Status.BAD_REQUEST,
    )
    post_dinosaurs(request_payload=dino_bravo)
    post_dinosaurs(request_payload=dino_charlie)
    get_dinosaurs(expected_response=[dino_alpha])
    post_turn(expected_response=PostTurnResponse(turnNumber=2))
    get_dinosaurs(expected_response=sorted([dino_alpha, dino_bravo, dino_charlie], reverse=True))
    post_dinosaurs(
        request_payload=dino_alpha,
        expected_response=DuplicateNameError(),
        expected_status=Status.BAD_REQUEST,
    )
    get_dinosaurs(expected_response=sorted([dino_alpha, dino_bravo, dino_charlie], reverse=True))
    post_turn(expected_response=PostTurnResponse(turnNumber=3))


def run_test_stories(stories: Collection[int] | None) -> None:
    if stories is None:
        test_stories_to_run = _test_stories
    else:
        test_stories_to_run = [_test_stories[story] for story in stories]
    print("Run tests")
    for test_story in test_stories_to_run or _test_stories:
        try:
            test_story()
            print(f" - PASS : {test_story.__name__}")
        except AssertionError as err:
            print(f" - FAIL : {test_story.__name__} - {err}")
        except Exception as err:
            print(f" - ERROR: {test_story.__name__} - {err}")


def list_test_stories() -> None:
    print("Registered Stories")
    for i, test_story in enumerate(_test_stories):
        print(f" - {i:>2}: {test_story.__name__}")


def register_test_story_builder(test_story: TestStory) -> None:
    _test_stories.append(test_story)


register_test_story_builder(test_turn_reset_turn)
register_test_story_builder(test_4_turn_1_reset_1_turn)
register_test_story_builder(test_mep2_res_example)
register_test_story_builder(test_mep2_dino)
register_test_story_builder(test_mep2_res_dino)
register_test_story_builder(test_mep2_expiration)
register_test_story_builder(test_mep2_w_1_dino)
