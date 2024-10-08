# -*- coding: utf-8 -*-
"""
  edsm_keys.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 8.10.2024, 16:32:38
  
  Purpose: 
"""


from ..attribtool import ReadOnlyClass


class EdsmKeys(object, metaclass=ReadOnlyClass):
    """EDSM API Keys container class."""

    ABSOLUTE_MAGNITUDE: str = "absoluteMagnitude"
    AGE: str = "age"
    ALLEGIANCE: str = "allegiance"
    API_KEY: str = "apiKey"
    ARG_OF_PERIAPSIS: str = "argOfPeriapsis"
    AXIAL_TILT: str = "axialTilt"
    BODIES: str = "bodies"
    BODY_COUNT: str = "bodyCount"
    BODY_ID: str = "bodyId"
    BODY_NAME: str = "bodyName"
    BREAKDOWN: str = "breakdown"
    CARGO: str = "cargo"
    COMMANDER_NAME: str = "commanderName"
    COMMENT: str = "comment"
    CONTROLLING_FACTION: str = "controllingFaction"
    COORDS: str = "coords"
    COORDS_LOCKED: str = "coordsLocked"
    CREDITS: str = "credits"
    DATA: str = "data"
    DATE: str = "date"
    DAY: str = "day"
    DEATHS: str = "deaths"
    DISTANCE: str = "distance"
    DISTANCE_TO_ARRIVAL: str = "distanceToArrival"
    DUPLICATES: str = "duplicates"
    ECONOMY: str = "economy"
    END_DATE_TIME: str = "endDateTime"
    ESTIMATED_VALUE: str = "estimatedValue"
    ESTIMATED_VALUE_MAPPED: str = "estimatedValueMapped"
    FACTION: str = "faction"
    FACTION_STATE: str = "factionState"
    FIRST_DISCOVER: str = "firstDiscover"
    FROM_GAME_BUILD: str = "fromGameBuild"
    FROM_GAME_VERSION: str = "fromGameVersion"
    FROM_SOFTWARE: str = "fromSoftware"
    FROM_SOFTWARE_VERSION: str = "fromSoftwareVersion"
    GOVERNMENT: str = "government"
    HAVE_MARKET: str = "haveMarket"
    HAVE_SHIPYARD: str = "haveShipyard"
    HIDDEN_AT: str = "hidden_at"
    ID: str = "id"
    ID64: str = "id64"
    INCLUDE_HIDDEN: str = "includeHidden"
    INFLUENCE: str = "influence"
    INFLUENCE_HISTORY: str = "influenceHistory"
    INFORMATION: str = "information"
    INNER_RADIUS: str = "innerRadius"
    IS_MAIN_STAR: str = "isMainStar"
    IS_PLAYER: str = "isPlayer"
    IS_SCOOPABLE: str = "isScoopable"
    LAST_UPDATE: str = "lastUpdate"
    LOGS: str = "logs"
    LUMINOSITY: str = "luminosity"
    MARKET_ID: str = "marketId"
    MATERIALS: str = "materials"
    MERGED_TO: str = "mergedTo"
    MESSAGE: str = "message"
    MIN_RADIUS: str = "minRadius"
    MSG: str = "msg"
    MSG_NUM: str = "msgnum"
    NAME: str = "name"
    ONLY_KNOWN_COORDINATES: str = "onlyKnownCoordinates"
    ONLY_UNKNOWN_COORDINATES: str = "onlyUnknownCoordinates"
    ORBITAL_ECCENTRICITY: str = "orbitalEccentricity"
    ORBITAL_INCLINATION: str = "orbitalInclination"
    ORBITAL_PERIOD: str = "orbitalPeriod"
    OUTER_RADIUS: str = "outerRadius"
    PENDING_STATES: str = "pendingStates"
    PERIOD: str = "period"
    PERMIT_NAME: str = "permitName"
    POPULATION: str = "population"
    PROGRESS: str = "progress"
    QTY: str = "qty"
    RADIUS: str = "radius"
    RANKS: str = "ranks"
    RANKS_VERBOSE: str = "ranksVerbose"
    RECOVERING_STATES: str = "recoveringStates"
    REQUIRE_PERMIT: str = "requirePermit"
    RINGS: str = "rings"
    ROTATIONAL_PERIOD: str = "rotationalPeriod"
    ROTATIONAL_PERIOD_TIDALLY_LOCKED: str = "rotationalPeriodTidallyLocked"
    SECURITY: str = "security"
    SEMI_MAJOR_AXIS: str = "semiMajorAxis"
    SHIP_ID: str = "shipId"
    SHOW_COORDINATES: str = "showCoordinates"
    SHOW_HISTORY: str = "showHistory"
    SHOW_ID: str = "showId"
    SHOW_INFORMATION: str = "showInformation"
    SHOW_PERMIT: str = "showPermit"
    SHOW_PRIMARY_STAR: str = "showPrimaryStar"
    SIZE: str = "size"
    SOLAR_MASSES: str = "solarMasses"
    SOLAR_RADIUS: str = "solarRadius"
    START_DATE_TIME: str = "startDateTime"
    STATE: str = "state"
    STATE_HISTORY: str = "stateHistory"
    STATIONS: str = "stations"
    STATION_NAME: str = "stationName"
    STATUS: str = "status"
    SUB_TYPE: str = "subType"
    SURFACE_TEMPERATURE: str = "surfaceTemperature"
    SYSTEM: str = "system"
    SYSTEM_ID: str = "systemId"
    SYSTEM_NAME: str = "systemName"
    TOTAL: str = "total"
    TRAFFIC: str = "traffic"
    TREND: str = "trend"
    TYPE: str = "type"
    URL: str = "url"
    VALUABLE_BODIES: str = "valuableBodies"
    VALUE_MAX: str = "valueMax"
    WEEK: str = "week"
    X: str = "x"
    Y: str = "y"
    Z: str = "z"
    _MARKET_ID: str = "_marketId"
    _SHIP_ID: str = "_shipId"
    _STATION_NAME: str = "_stationName"
    _SYSTEM_ADDRESS: str = "_systemAddress"
    _SYSTEM_COORDINATES: str = "_systemCoordinates"
    _SYSTEM_NAME: str = "_systemName"


# #[EOF]#######################################################################