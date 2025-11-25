from pydantic import BaseModel, Field
import enum
from typing import Any, Optional, List


# ============================================================
# ENUMS
# ============================================================

class TravelerType(str, enum.Enum):
    ADULT = "ADULT"
    CHILD = "CHILD"
    HELD_INFANT = "HELD_INFANT"


class CabinType(str, enum.Enum):
    ECONOMY = "ECONOMY"
    PREMIUM_ECONOMY = "PREMIUM_ECONOMY"
    BUSINESS = "BUSINESS"
    FIRST = "FIRST"


# ============================================================
# REQUEST MODELS - CLEAN & AMADEUS COMPLIANT
# ============================================================

class DepartureDateTimeRange(BaseModel):
    date: str
    time: Optional[str] = None   # Amadeus allows only date


class OriginDestination(BaseModel):
    id: str
    originLocationCode: str
    destinationLocationCode: str
    departureDateTimeRange: DepartureDateTimeRange


class Traveler(BaseModel):
    id: str
    travelerType: TravelerType
    associatedAdultId: Optional[str] = None


class AdditionalInformation(BaseModel):
    chargeableCheckedBags: Optional[bool] = None
    brandedFares: Optional[bool] = None
    fareRules: Optional[bool] = None


class PricingOptions(BaseModel):
    includedCheckedBagsOnly: Optional[bool] = None


class CarrierRestrictions(BaseModel):
    blacklistedInEUAllowed: Optional[bool] = None
    includedCarrierCodes: Optional[List[str]] = None


class CabinRestriction(BaseModel):
    cabin: Optional[CabinType] = None
    coverage: Optional[str] = "MOST_SEGMENTS"
    originDestinationIds: Optional[List[str]] = None


class ConnectionRestriction(BaseModel):
    airportChangeAllowed: Optional[bool] = None
    technicalStopsAllowed: Optional[bool] = None


class FlightFilters(BaseModel):
    crossBorderAllowed: Optional[bool] = None
    moreOvernightsAllowed: Optional[bool] = None
    returnToDepartureAirport: Optional[bool] = None
    railSegmentAllowed: Optional[bool] = None
    busSegmentAllowed: Optional[bool] = None
    carrierRestrictions: Optional[CarrierRestrictions] = None
    cabinRestrictions: Optional[List[CabinRestriction]] = None
    connectionRestriction: Optional[ConnectionRestriction] = None


class SearchCriteria(BaseModel):
    excludeAllotments: Optional[bool] = None
    addOneWayOffers: Optional[bool] = None
    maxFlightOffers: Optional[int] = 250
    allowAlternativeFareOptions: Optional[bool] = None
    oneFlightOfferPerDay: Optional[bool] = None
    additionalInformation: Optional[AdditionalInformation] = None
    pricingOptions: Optional[PricingOptions] = None
    flightFilters: Optional[FlightFilters] = None


# ============================================================
# REQUEST BODY ROOT
# ============================================================

class FlightSearchRequestPost(BaseModel):
    currencyCode: str = "USD"
    originDestinations: List[OriginDestination]
    travelers: List[Traveler]
    sources: List[str] = ["GDS"]
    searchCriteria: Optional[SearchCriteria] = None


# ============================================================
# RESPONSE MODELS (UNCHANGED)
# ============================================================

class Location(BaseModel):
    iataCode: str
    terminal: Optional[str] = None
    at: str


class Aircraft(BaseModel):
    code: str


class Operating(BaseModel):
    carrierCode: str


class Segment(BaseModel):
    departure: Location
    arrival: Location
    carrierCode: str
    number: str
    aircraft: Aircraft
    operating: Operating
    duration: str
    id: str
    numberOfStops: int
    blacklistedInEU: Optional[bool] = None


class Itinerary(BaseModel):
    duration: str
    segments: List[Segment]


class Fee(BaseModel):
    amount: str
    type: str


class AdditionalService(BaseModel):
    amount: str
    type: str


class Price(BaseModel):
    currency: str
    total: str
    base: str
    fees: Optional[List[Fee]] = None
    grandTotal: str
    additionalServices: Optional[List[AdditionalService]] = None


class PricingOptionsResponse(BaseModel):
    fareType: Optional[List[str]] = None
    includedCheckedBagsOnly: Optional[bool] = None


class Bags(BaseModel):
    quantity: int


class AmenityProvider(BaseModel):
    name: str


class Amenity(BaseModel):
    description: str
    isChargeable: bool
    amenityType: str
    amenityProvider: AmenityProvider


class FareDetailsBySegment(BaseModel):
    segmentId: str
    cabin: str
    fareBasis: str
    brandedFare: Optional[str] = None
    brandedFareLabel: Optional[str] = None
    class_: str = Field(..., alias="class")
    includedCheckedBags: Optional[Bags] = None
    includedCabinBags: Optional[Bags] = None
    amenities: Optional[List[Amenity]] = None


class TravelerPrice(BaseModel):
    currency: str
    total: str
    base: str


class TravelerPricing(BaseModel):
    travelerId: str
    fareOption: str
    travelerType: str
    price: TravelerPrice
    fareDetailsBySegment: List[FareDetailsBySegment]


class FlightOffer(BaseModel):
    type: str
    id: str
    source: str
    instantTicketingRequired: Optional[bool] = None
    nonHomogeneous: Optional[bool] = None
    oneWay: Optional[bool] = None
    isUpsellOffer: Optional[bool] = None
    lastTicketingDate: Optional[str] = None
    lastTicketingDateTime: Optional[str] = None
    numberOfBookableSeats: Optional[int] = None
    itineraries: Optional[List[Any]] = None
    price: Optional[Any] = None
    pricingOptions: Optional[Any] = None
    validatingAirlineCodes: Optional[List[str]] = None
    travelerPricings: Optional[List[Any]] = None
    totalPrice: Optional[str] = None
    totalPriceBase: Optional[str] = None
    fareType: Optional[str] = None


class FlightSearchResponse(BaseModel):
    data: List[FlightOffer]
    dictionaries: Optional[dict[str, Any]] = None
    meta: Optional[dict[str, Any]] = None


class FlightPricingResponse(BaseModel):
    data: Optional[dict[str, Any]] = None
    result: Optional[dict[str, Any]] = None
    meta: Optional[dict[str, Any]] = None
