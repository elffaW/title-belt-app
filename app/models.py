from enum import Enum


class NhlTeams(str, Enum):
    ANA = "Anaheim Ducks"
    BOS = "Boston Bruins"
    BUF = "Buffalo Sabres"
    CGY = "Calgary Flames"
    CAR = "Carolina Hurricanes"
    CHI = "Chicago Blackhawks"
    COL = "Colorado Avalanche"
    CBJ = "Columbus Blue Jackets"
    DAL = "Dallas Stars"
    DET = "Detroit Red Wings"
    EDM = "Edmonton Oilers"
    FLA = "Florida Panthers"
    LAK = "LA Kings"
    MIN = "Minnesota Wild"
    MTL = "Montreal Canadiens"
    NSH = "Nashville Predators"
    NJD = "New Jersey Devils"
    NYI = "New York Islanders"
    NYR = "New York Rangers"
    OTT = "Ottawa Senators"
    PHI = "Philadelphia Flyers"
    PIT = "Pittsburgh Penguins"
    SJS = "San Jose Sharks"
    SEA = "Seattle Kraken"
    STL = "St Louis Blues"
    TBL = "Tampa Bay Lightning"
    TOR = "Toronto Maple Leafs"
    UTA = "Utah Hockey Club"
    VAN = "Vancouver Canucks"
    VGK = "Vegas Golden Knights"
    WSH = "Washington Capitals"
    WPG = "Winnipeg Jets"

    def __str__(self) -> str:
        return self.value
