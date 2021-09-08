from __future__ import annotations

from collections.abc import Collection
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Literal, Optional, TypedDict, Union


class DinosaursDict(TypedDict):
    name: str
    weight: int
    gender: str
    species: str


class InvalidErrorDict(TypedDict):
    error: str
    description: str


class DinoGender(Enum):
    value: str
    MALE = "m"
    FEMALE = "f"
    INVALID = "INVALID"


class DinoSpecies(Enum):
    value: str
    ANKYLOSAURUS = "Ankylosaurus"
    BRACHIOSAURUS = "Brachiosaurus"
    DIPLODOCUS = "Diplodocus"
    STEGOSAURUS = "Stegosaurus"
    TRICERATOPS = "Triceratops"
    ALLOSAURUS = "Allosaurus"
    MEGALOSAURUS = "Megalosaurus"
    SPINOSAURUS = "Spinosaurus"
    TYRANNOSAURUS_REX = "Tyrannosaurus Rex"
    VELOCIRAPTOR = "Velociraptor"
    INVALID = "INVALID"


DinoCarnivore = {
    DinoSpecies.ALLOSAURUS,
    DinoSpecies.MEGALOSAURUS,
    DinoSpecies.SPINOSAURUS,
    DinoSpecies.TYRANNOSAURUS_REX,
    DinoSpecies.VELOCIRAPTOR,
}

DinoHerbivorous = {
    DinoSpecies.ANKYLOSAURUS,
    DinoSpecies.BRACHIOSAURUS,
    DinoSpecies.DIPLODOCUS,
    DinoSpecies.STEGOSAURUS,
    DinoSpecies.TRICERATOPS,
}


@dataclass(frozen=True)
class HeartBeatResponse:
    time: str = datetime.now().astimezone().isoformat()


@dataclass(frozen=True)
class PostTurnResponse:
    turnNumber: int

    def __post_init__(self) -> None:
        assert self.turnNumber >= 1


@dataclass(frozen=True)
class Resource:
    qtyBurger: int
    qtySalad: int
    qtyWater: int

    def __post_init__(self) -> None:
        assert self.qtyBurger >= 0
        assert self.qtySalad >= 0
        assert self.qtyWater >= 0


@dataclass(frozen=True)
class PostResourcesRequest:
    qtyBurger: int | None = None
    qtySalad: int | None = None
    qtyWater: int | None = None

    def __post_init__(self) -> None:
        assert any({self.qtyBurger, self.qtySalad, self.qtyWater})


@dataclass(frozen=True)
class PostResourcesInvalidResourceQuantityError:
    error: Literal["INVALID_RESOURCE_QUANTITY"] = "INVALID_RESOURCE_QUANTITY"
    description: Literal["Resource quantities must be positive."] = "Resource quantities must be positive."

    def __post_init__(self) -> None:
        assert self.error == "INVALID_RESOURCE_QUANTITY"
        assert self.description == "Resource quantities must be positive."


@dataclass(frozen=True)
class GetResourcesResponse:
    fresh: Resource
    expired: Resource
    consumed: Resource


@dataclass(frozen=True)
class Dinosaurs:
    name: str
    weight: int
    gender: DinoGender
    species: DinoSpecies

    def to_dict(self) -> DinosaursDict:
        return {
            "name": self.name,
            "weight": self.weight,
            "gender": self.gender.value,
            "species": self.species.value,
        }

    def force(self) -> float:
        return (
            self.weight
            * (1.5 if self.gender == DinoGender.FEMALE else 1)
            * (1.5 if self.species in DinoCarnivore else 1)
        )

    def __lt__(self, other) -> bool:
        return self.force() < other.force()

    def __eq__(self, other) -> bool:
        return self.force() == other.force()


@dataclass(frozen=True)
class InvalidError:
    error: str
    description: str

    def to_dict(self) -> InvalidErrorDict:
        return {"error": self.error, "description": self.description}


@dataclass(frozen=True)
class InvalidGenderError(InvalidError):
    error: Literal["INVALID_GENDER"] = "INVALID_GENDER"
    description: Literal[
        'The specified gender must be "m" or "f".'
    ] = 'The specified gender must be "m" or "f".'

    def __post_init__(self) -> None:
        assert self.error == "INVALID_GENDER"
        assert self.description == 'The specified gender must be "m" or "f".'


@dataclass(frozen=True)
class InvalidWeightError(InvalidError):
    error: Literal["INVALID_WEIGHT"] = "INVALID_WEIGHT"
    description: Literal[
        "The specified weight must be greater than 0."
    ] = "The specified weight must be greater than 0."

    def __post_init__(self) -> None:
        assert self.error == "INVALID_WEIGHT"
        assert self.description == "The specified weight must be greater than 0."


@dataclass(frozen=True)
class DuplicateNameError(InvalidError):
    error: Literal["DUPLICATE_NAME"] = "DUPLICATE_NAME"
    description: Literal[
        "The specified name already exists and must be unique."
    ] = "The specified name already exists and must be unique."

    def __post_init__(self) -> None:
        assert self.error == "DUPLICATE_NAME"
        assert self.description == "The specified name already exists and must be unique."


@dataclass(frozen=True)
class InvalidSpeciesError(InvalidError):
    error: Literal["INVALID_SPECIES"] = "INVALID_SPECIES"
    description: Literal[
        "The specified species is not supported."
    ] = "The specified species is not supported."

    def __post_init__(self) -> None:
        assert self.error == "INVALID_SPECIES"
        assert self.description == "The specified species is not supported."


@dataclass(frozen=True)
class NonExistentNameError(InvalidError):
    error: Literal["NON_EXISTENT_NAME"] = "NON_EXISTENT_NAME"
    description: Literal["The specified name does not exist."] = "The specified name does not exist."

    def __post_init__(self) -> None:
        assert self.error == "NON_EXISTENT_NAME"
        assert self.description == "The specified name does not exist."


GetDinosaursResponse = Collection[Dinosaurs]
GetDinosaurByNameResponses = Union[Dinosaurs, NonExistentNameError]
PostResourcesResponses = Optional[PostResourcesInvalidResourceQuantityError]
PostDinosaursResponses = Optional[
    Union[DuplicateNameError, InvalidGenderError, InvalidWeightError, InvalidSpeciesError]
]
