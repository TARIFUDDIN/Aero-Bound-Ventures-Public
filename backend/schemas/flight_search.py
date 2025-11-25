from pydantic import BaseModel, Field
from typing import Optional


class DepartureDateTimeRange(BaseModel):
    date: str

class OriginDestination(BaseModel):
    id: str
    originLocationCode: str
    destinationLocationCode: str
    departureDateTimeRange: DepartureDateTimeRange


class Traveler(BaseModel):
    id: str
    travelerType: str
    associatedAdultId: Optional[str] = None


class AdditionalInformation(BaseModel):
    chargeableCheckedBags: Optional[bool] = None
    brandedFares: Optional[bool] = None
    fareRules: Optional[bool] = None


class PricingOptions(BaseModel):
    includedCheckedBagsOnly: Optional[bool] = None


class CarrierRestrictions(BaseModel):
    blacklistedInEUAllowed: Optional[bool] = None
    includedCarrierCodes: Optional[list[str]] = None


class CabinRestriction(BaseModel):
    cabin: Optional[str] = None
    coverage: str = "MOST_SEGMENTS"
    originDestinationIds: Optional[list[str]] = None


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
    cabinRestrictions: Optional[list[CabinRestriction]] = None
    connectionRestriction: Optional[ConnectionRestriction] = None


class SearchCriteria(BaseModel):
    excludeAllotments: Optional[bool] = None
    addOneWayOffers: Optional[bool] = None
    maxFlightOffers: Optional[int] = 5
    allowAlternativeFareOptions: Optional[bool] = None
    oneFlightOfferPerDay: Optional[bool] = None
    additionalInformation: Optional[AdditionalInformation] = None
    pricingOptions: Optional[PricingOptions] = None
    flightFilters: Optional[FlightFilters] = None


class FlightSearchRequestPost(BaseModel):
    currencyCode: str
    originDestinations: list[OriginDestination]
    travelers: list[Traveler]
    sources: list[str]
    searchCriteria: Optional[SearchCriteria] = None


class FlightSearchRequestGet(BaseModel):
    originLocationCode: str
    destinationLocationCode: str
    departureDate: str
    adults: int = Field(default=1)
    max: int = Field(default=5)
    returnDate: Optional[str] = None
    children: Optional[int] = None
    infants: Optional[int] = None
    travelClass: Optional[str] = None
    includedAirlineCodes: Optional[str] = None
    excludedAirlineCodes: Optional[str] = None
    nonStop: Optional[bool] = None
    currencyCode: str = Field(default="USD")
    maxPrice: Optional[int] = None