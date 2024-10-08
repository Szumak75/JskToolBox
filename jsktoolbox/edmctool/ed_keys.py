# -*- coding: utf-8 -*-
"""
  ed.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 8.10.2024, 14:15:25
  
  Purpose: 
"""


from ..attribtool import ReadOnlyClass


class EDKeys(object, metaclass=ReadOnlyClass):
    """Elite dangerous Keys container class."""

    AFMU_REPAIRS: str = "AfmuRepairs"
    APPLIED_TO_SQUADRON: str = "AppliedToSquadron"
    APPROACH_BODY: str = "ApproachBody"
    ASTEROID_CRACKED: str = "AsteroidCracked"
    BOOK_DROP_SHIP: str = "BookDropship"
    BOUNTY: str = "Bounty"
    CANCEL_DROPSHIP: str = "CancelDropship"
    CAP_SHIP_BOND: str = "CapShipBond"
    CARGO_TRANSFER: str = "CargoTransfer"
    CARRIER_BANK_TRANSFER: str = "CarrierBankTransfer"
    CARRIER_BUY: str = "CarrierBuy"
    CARRIER_CREW_SERVICES: str = "CarrierCrewServices"
    CARRIER_DECOMMISSION: str = "CarrierDecommission"
    CARRIER_DEPOSIT_FUEL: str = "CarrierDepositFuel"
    CARRIER_DOCKING_PERMISSION: str = "CarrierDockingPermission"
    CARRIER_FINANCE: str = "CarrierFinance"
    CARRIER_JUMP_CANCELLED: str = "CarrierJumpCancelled"
    CARRIER_JUMP_REQUEST: str = "CarrierJumpRequest"
    CARRIER_MODULE_PACK: str = "CarrierModulePack"
    CARRIER_NAME_CHANGE: str = "CarrierNameChange"
    CARRIER_STATS: str = "CarrierStats"
    CARRIER_TRADE_ORDER: str = "CarrierTradeOrder"
    CHANGE_CREW_ROLE: str = "ChangeCrewRole"
    CLEAR_SAVED_GAME: str = "ClearSavedGame"
    COCKPIT_BREACHED: str = "CockpitBreached"
    COLLECT_ITEMS: str = "CollectItems"
    COMMANDER: str = "Commander"
    CONTINUED: str = "Continued"
    CORIOLIS: str = "Coriolis"
    CREATE_SUIT_LOADOUT: str = "CreateSuitLoadout"
    CREW_ASSIGN: str = "CrewAssign"
    CREW_FIRE: str = "CrewFire"
    CREW_LAUNCH_FIGHTER: str = "CrewLaunchFighter"
    CREW_MEMBER_JOINS: str = "CrewMemberJoins"
    CREW_MEMBER_QUITS: str = "CrewMemberQuits"
    CREW_MEMBER_ROLE_CHANGE: str = "CrewMemberRoleChange"
    CRIME_VICTIM: str = "CrimeVictim"
    DATA_SCANNED: str = "DataScanned"
    DATA_LINK_SCAN: str = "DatalinkScan"
    DATA_LINK_VOUCHER: str = "DatalinkVoucher"
    DISBANDED_SQUADRON: str = "DisbandedSquadron"
    DISCOVERY_SCAN: str = "DiscoveryScan"
    DISEMBARK: str = "Disembark"
    DOCK_FIGHTER: str = "DockFighter"
    DOCK_SRV: str = "DockSRV"
    DOCKING_CANCELLED: str = "DockingCancelled"
    DOCKING_DENIED: str = "DockingDenied"
    DOCKING_GRANTED: str = "DockingGranted"
    DOCKING_REQUESTED: str = "DockingRequested"
    DOCKING_TIMEOUT: str = "DockingTimeout"
    DROP_ITEMS: str = "DropItems"
    DROPSHIP_DEPLOY: str = "DropshipDeploy"
    EDD_COMMODITY_PRICES: str = "EDDCommodityPrices"
    EDD_ITEM_SET: str = "EDDItemSet"
    ED_SHIPYARD: str = "EDShipyard"
    EMBARK: str = "Embark"
    END_CREW_SESSION: str = "EndCrewSession"
    ENGINEER_APPLY: str = "EngineerApply"
    ENGINEER_LEGACY_CONVERT: str = "EngineerLegacyConvert"
    ESCAPE_INTERDICTION: str = "EscapeInterdiction"
    FSS_BODY_SIGNALS: str = "FSSBodySignals"
    FSS_SIGNAL_DISCOVERED: str = "FSSSignalDiscovered"
    FACTION_KILL_BOND: str = "FactionKillBond"
    FIGHTER_DESTROYED: str = "FighterDestroyed"
    FIGHTER_REBUILT: str = "FighterRebuilt"
    FILEHEADER: str = "Fileheader"
    FUEL_SCOOP: str = "FuelScoop"
    HEAT_DAMAGE: str = "HeatDamage"
    HEAT_WARNING: str = "HeatWarning"
    HULL_DAMAGE: str = "HullDamage"
    INVITED_TO_SQUADRON: str = "InvitedToSquadron"
    JET_CONE_BOOST: str = "JetConeBoost"
    JET_CONE_DAMAGE: str = "JetConeDamage"
    JOINED_SQUADRON: str = "JoinedSquadron"
    KICK_CREW_MEMBER: str = "KickCrewMember"
    LAUNCH_DRONE: str = "LaunchDrone"
    LAUNCH_FIGHTER: str = "LaunchFighter"
    LAUNCH_SRV: str = "LaunchSRV"
    LEAVE_BODY: str = "LeaveBody"
    LEFT_SQUADRON: str = "LeftSquadron"
    LIFTOFF: str = "Liftoff"
    LOADOUT_EQUIP_MODULE: str = "LoadoutEquipModule"
    MARKET: str = "Market"
    MASS_MODULE_STORE: str = "MassModuleStore"
    MATERIAL_DISCOVERED: str = "MaterialDiscovered"
    MODULE_ARRIVED: str = "ModuleArrived"
    MODULE_INFO: str = "ModuleInfo"
    MODULE_STORE: str = "ModuleStore"
    MODULE_SWAP: str = "ModuleSwap"
    MUSIC: str = "Music"
    NAV_BEACON_SCAN: str = "NavBeaconScan"
    NAV_ROUTE: str = "NavRoute"
    NAV_ROUTE_CLEAR: str = "NavRouteClear"
    NEW_COMMANDER: str = "NewCommander"
    NPC_CREW_RANK: str = "NpcCrewRank"
    OUTFITTING: str = "Outfitting"
    PVP_KILL: str = "PVPKill"
    PASSENGERS: str = "Passengers"
    POWERPLAY_VOTE: str = "PowerplayVote"
    POWERPLAY_VOUCHER: str = "PowerplayVoucher"
    PROSPECTED_ASTEROID: str = "ProspectedAsteroid"
    REBOOT_REPAIR: str = "RebootRepair"
    RECEIVE_TEXT: str = "ReceiveText"
    REPAIR_DRONE: str = "RepairDrone"
    RESERVOIR_REPLENISHED: str = "ReservoirReplenished"
    SAA_SIGNALS_FOUND: str = "SAASignalsFound"
    SRV_DESTROYED: str = "SRVDestroyed"
    SCAN_BARY_CENTRE: str = "ScanBaryCentre"
    SCAN_ORGANIC: str = "ScanOrganic"
    SCANNED: str = "Scanned"
    SCREENSHOT: str = "Screenshot"
    SEND_TEXT: str = "SendText"
    SHARED_BOOKMARK_TO_SQUADRON: str = "SharedBookmarkToSquadron"
    SHIELD_STATE: str = "ShieldState"
    SHIP_ARRIVED: str = "ShipArrived"
    SHIP_TARGETED: str = "ShipTargeted"
    SHIPYARD: str = "Shipyard"
    SHIPYARD_NEW: str = "ShipyardNew"
    SHUT_DOWN: str = "ShutDown"
    SHUTDOWN: str = "Shutdown"
    SQUADRON_CREATED: str = "SquadronCreated"
    SQUADRON_STARTUP: str = "SquadronStartup"
    START_JUMP: str = "StartJump"
    STATUS: str = "Status"
    STORED_MODULES: str = "StoredModules"
    SUIT_LOADOUT: str = "SuitLoadout"
    SUPERCRUISE_ENTRY: str = "SupercruiseEntry"
    SUPERCRUISE_EXIT: str = "SupercruiseExit"
    SWITCH_SUIT_LOADOUT: str = "SwitchSuitLoadout"
    SYSTEMS_SHUTDOWN: str = "SystemsShutdown"
    TOUCHDOWN: str = "Touchdown"
    UNDER_ATTACK: str = "UnderAttack"
    VEHICLE_SWITCH: str = "VehicleSwitch"
    WING_ADD: str = "WingAdd"
    WING_INVITE: str = "WingInvite"
    WING_JOIN: str = "WingJoin"
    WING_LEAVE: str = "WingLeave"


# #[EOF]#######################################################################
