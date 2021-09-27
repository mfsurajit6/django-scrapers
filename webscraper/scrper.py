import json
import logging
import random
import requests
from bs4 import BeautifulSoup
from celery import app, shared_task

from webscraper.config import LOG_LEVEL, LOG_FORMAT, LOG_DT_FORMAT
from webscraper.constant import ZIP_LAT_LANG, USER_AGENT
from webscraper.base_urls import BURGERKING_URL, PIZZAHUT_URL, STARBUCKS_URL, VERIZON_URL


class BurgerKing:
    """ Get BurgerKing outlet information form random locations of United States  in dictionary format"""
    def __init__(self):
        self.stores = {}
        self.url = BURGERKING_URL
        self.query = """
                query GetRestaurants($input: RestaurantsInput) {  restaurants(input: $input) {    pageInfo {      hasNextPage      endCursor      __typename    }    totalCount    nodes {      ...RestaurantNodeFragment      __typename    }    __typename  }}fragment RestaurantNodeFragment on RestaurantNode {  _id  storeId  isAvailable  posVendor  chaseMerchantId  curbsideHours {    ...OperatingHoursFragment    __typename  }  deliveryHours {    ...OperatingHoursFragment    __typename  }  diningRoomHours {    ...OperatingHoursFragment    __typename  }  distanceInMiles  drinkStationType  driveThruHours {    ...OperatingHoursFragment    __typename  }  driveThruLaneType  email  environment  franchiseGroupId  franchiseGroupName  frontCounterClosed  hasBreakfast  hasBurgersForBreakfast  hasCatering  hasCurbside  hasDelivery  hasDineIn  hasDriveThru  hasMobileOrdering  hasParking  hasPlayground  hasTakeOut  hasWifi  id  isDarkKitchen  isFavorite  isRecent  latitude  longitude  mobileOrderingStatus  name  number  parkingType  phoneNumber  physicalAddress {    address1    address2    city    country    postalCode    stateProvince    stateProvinceShort    __typename  }  playgroundType  pos {    vendor    __typename  }  posRestaurantId  restaurantImage {    asset {      _id      metadata {        lqip        palette {          dominant {            background            foreground            __typename          }          __typename        }        __typename      }      __typename    }    crop {      top      bottom      left      right      __typename    }    hotspot {      height      width      x      y      __typename    }    __typename  }  restaurantPosData {    _id    __typename  }  status  vatNumber  __typename}fragment OperatingHoursFragment on OperatingHours {  friClose  friOpen  monClose  monOpen  satClose  satOpen  sunClose  sunOpen  thrClose  thrOpen  tueClose  tueOpen  wedClose  wedOpen  __typename}
                """
        self.variables = {
            "input": {
                "filter": "NEARBY",
                "coordinates": {
                    "userLat": 0,
                    "userLng": 0,
                    "searchRadius": 32000
                },
                "first": 20,
                "status": "OPEN"
            }
        }
        self.headers = {
            'User-Agent': random.choice(USER_AGENT),
            "Upgrade-Insecure-Requests": "1",
            "DNT": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate"
        }
        logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT, datefmt=LOG_DT_FORMAT)

    def get_stores(self):
        """
        Get all the outlet details
        :return: dict, All Outlet Details
        """
        for i in range(len(ZIP_LAT_LANG)):
            lat = ZIP_LAT_LANG[i][1]
            long = ZIP_LAT_LANG[i][2]
            stores_from_location = self.get_details(lat, long)
            if stores_from_location is not None:
                for store in stores_from_location:
                    if store not in self.stores:
                        self.stores[store] = stores_from_location[store]
        return self.stores

    def get_details(self, lat, long):
        """
        Get Outlet Details of specific location
        :param lat: float, Latitude of the location
        :param long: float, Longitude of the location
        :return: dict, Stores of the specified location
        """
        local_stores = {}
        self.variables["input"]["coordinates"]["userLat"] = lat
        self.variables["input"]["coordinates"]["userLng"] = long
        try:
            response = requests.post(self.url, json={'query': self.query, 'variables': self.variables}, headers=self.headers)
            json_data = response.json()
            nodes = json_data.get("data").get("restaurants").get("nodes")
        except Exception as ex:
            logging.critical("BurgerKing says: %s", str(ex))
            return None
        for node in nodes:
            store = {}
            store_id = node.get("storeId")
            store_name_long = node.get("name")
            physical_address = node.get("physicalAddress")
            store_address = physical_address.get("address1")
            store_address += physical_address.get("address2") if physical_address.get("address2") != "" else ""
            store["name"] = store_name_long.split(',')[0]
            store["address"] = store_address
            store["city"] = physical_address.get("city")
            store["state"] = physical_address.get("stateProvince")
            store["zip"] = physical_address.get("postalCode").split("-")[0]
            store["phone"] = node.get("phoneNumber")
            store["latitude"] = node.get("latitude")
            store["longitude"] = node.get("longitude")
            if store_id not in local_stores:
                local_stores[store_id] = store
        return local_stores


class PizzaHut:
    """ Get PizzaHut outlet information form all over United States in dictionary format"""

    def __init__(self):
        self.stores = {}
        self.state_urls = {}
        self.outlet_urls = []
        self.base_url = PIZZAHUT_URL
        self.headers = {
            'User-Agent': random.choice(USER_AGENT),
            "Upgrade-Insecure-Requests": "1",
            "DNT": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate"
        }
        logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT, datefmt=LOG_DT_FORMAT)

    def get_stores(self):
        """
        Get all the outlet details
        :return: dict, All Store Details
        """
        self.get_states()
        for state, link in self.state_urls.items():
            # url = f'{url}lat={lat}&long={long}'
            state_url = f'{self.base_url}/{link}'
            # state_url = self.base_url + "/" + link
            res = requests.get(state_url, headers=self.headers)
            soup = BeautifulSoup(res.content, 'html.parser')
            urls = soup.find_all("a", {"class": "Directory-listLink"})
            for url in urls:
                self.outlet_urls.append(url.get("href"))
        self.get_details()
        return self.stores

    def get_states(self):
        """
        Finds the states and corresponding URLS and put it in state_urls list
        :return: None
       """
        res = requests.get(self.base_url, headers=self.headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        state_data = soup.find("ul", {"class": "Directory-listLinks"})
        states = state_data.find_all("a", {"class": "Directory-listLink"})
        for a in states:
            state = a.text
            state_url = a.get("href")
            self.state_urls[state] = state_url

    def get_details(self):
        """
        Find the outlet of evey states
        :return: None
        """
        store_id = 1
        for i in range(0, len(self.outlet_urls), 20):
            outleturl = self.outlet_urls[i]
            url = self.base_url + "/" + outleturl
            res = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(res.content, 'html.parser')
            outlets = soup.find_all("li", {"class": "Directory-listTeaser"})
            for outlet in outlets:
                store = {}
                store_address = outlet.find("span", {"class": "c-address-street-1"}).text
                store_address_1 = outlet.find("span", {"class": "c-address-street-2"})
                if store_address_1 is not None:
                    store_address += store_address_1.text
                store_state = outlet.find("abbr", {"class": "c-address-state"})
                store_phone = outlet.find("a", {"class": "c-phone-number-link c-phone-main-number-link"})
                store['name'] = outlet.find("span", {"class": "LocationName-geo"}).text
                store['address'] = store_address
                store['city'] = outlet.find("span", {"class": "c-address-city"}).text
                store['state'] = store_state.text if store_state is not None else ""
                store['zip'] = outlet.find("span", {"class": "c-address-postal-code"}).text
                store['phone'] = store_phone.text if store_phone is not None else ''
                self.stores[store_id] = store
                store_id += 1



class StarBucks:
    """ Get StarBucks outlet information form random locations of United States  in dictionary format"""
    def __init__(self):
        self.stores = {}
        self.base_url = STARBUCKS_URL
        self.headers = {
            "x-requested-with": "XMLHttpRequest",
            'User-Agent': random.choice(USER_AGENT),
            "Upgrade-Insecure-Requests": "1",
            "DNT": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate"
        }
        logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT, datefmt=LOG_DT_FORMAT)

    def get_stores(self):
        """
        Get all the outlet details
        :return: dict, All Outlet Details
        """
        for i in range(len(ZIP_LAT_LANG)):
            lat = ZIP_LAT_LANG[i][1]
            long = ZIP_LAT_LANG[i][2]
            stores_from_location = self.get_data(lat, long)
            if stores_from_location is not None:
                for s in stores_from_location:
                    if s not in self.stores:
                        self.stores[s] = stores_from_location[s]
        return self.stores

    def get_data(self, lat, long):
        """
        Get Outlet Details of specific location
        :param lat: float, Latitude of the location
        :param long: float, Longitude of the location
        :return: dict, Stores of the specified location
        """
        url = self.base_url
        url = f'{url}lat={lat}&lag={long}'
        try:
            res = requests.get(url, headers=self.headers)
            json_data = res.json()
        except Exception as ex:
            logging.critical("StarBucks says: %s", str(ex))
            return None

        local_stores = json_data.get('stores')
        stores_data = {}

        for i in range(len(local_stores)):
            s = local_stores[i]
            store = {}
            store_id = s.get('id')
            store['name'] = s.get('name')
            address = s.get('address')
            store['address'] = address.get('streetAddressLine1')
            store['city'] = address.get('city')
            store['state'] = address.get('countrySubdivisionCode')
            store['zip'] = address.get('postalCode')
            store['phone'] = s.get('phoneNumber')
            store['latitude'] = s['coordinates']['latitude']
            store['longitude'] = s['coordinates']['longitude']

            if store_id not in stores_data.keys():
                stores_data[store_id] = store

        return stores_data



class Verizon:
    """ Get Verizon outlet information form random locations of United States  in dictionary format"""
    def __init__(self):
        self.base_url = VERIZON_URL
        self.headers = {
            'User-Agent': random.choice(USER_AGENT),
            "Upgrade-Insecure-Requests": "1",
            "DNT": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate"
        }
        self.stores = {}
        logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT, datefmt=LOG_DT_FORMAT)

    def get_stores(self):
        """
        Get all the outlet details
        :return: dict, All Outlet Details
        """
        for i in range(len(ZIP_LAT_LANG)):
            lat = ZIP_LAT_LANG[i][1]
            long = ZIP_LAT_LANG[i][2]
            local_stores = self.get_data(lat, long)
            if local_stores is not None:
                for s in local_stores:
                    if s not in self.stores:
                        self.stores[s] = local_stores[s]
        return self.stores

    def get_data(self, lat, long):
        """
        Get Outlet Details of specific location
        :param lat: float, Latitude of the location
        :param long: float, Longitude of the location
        :return: dict, Stores of the specified location
        """
        url = self.base_url
        url = f'{url}lat={lat}&long={long}'
        local_stores = {}
        try:
            response = requests.get(url, headers=self.headers)
            local_stores = json.loads(response.content)
        except Exception as ex:
            logging.critical("Verizon says: %s", str(ex))

        stores_data = {}
        for local_store in local_stores:
            if isinstance(local_store, str):
                continue
            store = {}
            store['name'] = local_store.get('storeName')
            store['address'] = local_store.get('address')
            store['city'] = local_store.get('city')
            store['state'] = local_store.get('state')
            store['zip'] = local_store.get('zip')
            store['phone'] = local_store.get('phone')
            store['latitude'] = local_store.get('lat')
            store['longitude'] = local_store.get('lng')
            store_number = local_store.get('storeNumber')
            if store_number not in stores_data:
                stores_data[store_number] = store
        return stores_data

