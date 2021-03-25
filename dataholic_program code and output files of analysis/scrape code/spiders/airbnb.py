# -*- coding: utf-8 -*-

import scrapy
import json




class AirbnbSpider(scrapy.Spider):
    name = 'airbnb'
    allowed_domains = ['www.airbnb.com']

    def start_requests(self):

        yield scrapy.Request(
            url='https://www.airbnb.com/api/v2/explore_tabs?_format=for_explore_search_web&auto_ib=true&client_session_id=250ad5ec-9986-42d5-a679-11c347c9ddfc&currency=HKD&current_tab_id=home_tab&experiences_per_grid=20&fetch_filters=true&guidebooks_per_grid=20&has_zero_guest_treatment=true&hide_dates_and_guests_filters=true&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true&items_per_grid=18&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en&map_toggle=false&metadata_only=false&place_id=ChIJByjqov3-AzQR2pT0dDW0bUg&query=Hong%20Kong&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&satori_version=1.1.14&screen_height=1187&screen_size=large&screen_width=1600&search_type=unknown&selected_tab_id=home_tab&show_groupings=true&source=mc_search_bar&supports_for_you_v3=true&timezone_offset=480&version=1.6.2',
            callback=self.parse_id)

    def parse_page(self, response):
        ## Scraping API of individual listing
        id = response.request.meta['id']
        data = json.loads(response.body)
        info = data.get('pdp_listing_detail')
        listing_details ={}
        listing_details['id'] = id
        listing_details['host_name'] = info.get('primary_host').get('host_name')
        listing_details['member_since'] = info.get('primary_host').get('member_since')
        listing_details['amenities'] = info.get('sectioned_description').get('access')
        listing_details['notes'] = info.get('sectioned_description').get('notes')
        listing_details['transit'] = info.get('sectioned_description').get('transit')
        listing_details['space'] = info.get('sectioned_description').get('space')
        listing_details['description'] = info.get('sectioned_description').get('description')
        listing_details['neighborhood_overview'] = info.get('sectioned_description').get('neighborhood_overview')
        listing_details['neighborhood_id'] = info.get('neighborhood_id')
        listing_details['review_score'] = info.get('review_details_interface').get('review_score')
        listing_details['summary'] = info.get('sectioned_description').get('summary')

        listing_details['Accuracy'] = info.get('review_details_interface').get('review_summary')[0].get('value')
        listing_details['Accuracy_localized'] = info.get('review_details_interface').get('review_summary')[0].get(
            'localized_rating')

        listing_details['Communication'] = info.get('review_details_interface').get('review_summary')[1].get('value')
        listing_details['Communication_localized'] = info.get('review_details_interface').get('review_summary')[1].get(
            'localized_rating')

        listing_details['Cleanliness'] = info.get('review_details_interface').get('review_summary')[2].get('value')
        listing_details['Cleanliness_localized'] = info.get('review_details_interface').get('review_summary')[2].get(
            'localized_rating')

        listing_details['Location'] = info.get('review_details_interface').get('review_summary')[3].get('value')
        listing_details['Location_localized'] = info.get('review_details_interface').get('review_summary')[3].get(
            'localized_rating')

        listing_details['Check-in'] = info.get('review_details_interface').get('review_summary')[4].get('value')
        listing_details['Check-in_localized'] = info.get('review_details_interface').get('review_summary')[4].get(
            'localized_rating')

        listing_details['Value'] = info.get('review_details_interface').get('review_summary')[5].get('value')
        listing_details['Value_localized'] = info.get('review_details_interface').get('review_summary')[5].get('localized_rating')

        yield listing_details

    def parse_reviews(self, response):
        # Scraping listing reviews from Reviews API
        id = response.request.meta['id']
        data = json.loads(response.body)
        reviews = data.get('reviews')
        num_of_review=0
        reviews_dict = {}
        for x in reviews:
            num_of_review += 1
            reviews_dict['listing_id'] = id
            reviews_dict['review_num'] = num_of_review
            reviews_dict['review'] = x.get('comments')
            reviews_dict['review_rating'] = x.get('rating')
            reviews_dict['review_date'] = x.get('created_at')
            reviews_dict['reviewer_id'] = x.get('reviewer').get('id')
            reviews_dict['review_id'] = x.get('id')
            yield reviews_dict

    def parse_id(self, response):
        # Acquire search page API in json file
        data = json.loads(response.body)

        # Detect if API is on the first page
        pagination_metadata = data.get('explore_tabs')[0].get('pagination_metadata')
        if pagination_metadata.get('has_previous_page'):
            section_number = 0
        else:
            section_number = 1
        ##Iterate through individual listings to acquire information available on search page API#
        rooms = data.get('explore_tabs')[0].get('sections')[section_number].get('listings')
        for room in rooms:
            id = room.get('listing').get('id')
            name = room.get('listing').get('name')
            lng = room.get('listing').get('lng')
            lat = room.get('listing').get('lat')
            star_rating = room.get('listing').get('star_rating')
            avg_rating = room.get('listing').get('avg_rating')
            price = room.get('pricing_quote').get('rate').get('amount')
            bathrooms = room.get('listing').get('bathrooms')
            bathroom_label = room.get('listing').get('bathroom_label')
            bedroom_label = room.get('listing').get('bedroom_label')
            beds = room.get('listing').get('beds')
            guest_label = room.get('listing').get('guest_label')

            room_type = room.get('listing').get('room_type')
            room_and_property_type = room.get('listing').get('room_and_property_type')
            neighbourhood = room.get('listing').get('neighbourhood')
            localized_neighbourhood = room.get('listing').get('localized_neighbourhood')
            user_id = room.get('listing').get('user').get('id')
            host_languages = room.get('listing').get('host_languages')
            is_new_listing = room.get('listing').get('is_new_listing')
            is_superhost = room.get('listing').get('is_superhost')
            reviews_count = room.get('listing').get('reviews_count')
            # Create 'Items' Dictionary to store information of individual listing
            items = {
                 'id': id,
                'name': name,
                'lng': lng,
                'lat': lat,
                'star_rating': star_rating,
                'avg_rating': avg_rating,
                'price': price,
                'bathrooms': bathrooms,
                'bathroom_label': bathroom_label,
                'bedroom_label': bedroom_label,
                'beds': beds,
                'guest_label': guest_label,
                'reviews_count': reviews_count,
                'room_type': room_type,
                'room_and_property_type': room_and_property_type,
                'neighbourhood': neighbourhood,
                'localized_neighbourhood': localized_neighbourhood,
                'user_id': user_id,
                'host_languages': host_languages,
                'is_new_listing': is_new_listing,
                'is_superhost': is_superhost
            }

            room_url = 'https://www.airbnb.com/api/v2/pdp_listing_details/{}?_format=for_rooms_show&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&'.format(id)
            room_reviews_api = 'https://www.airbnb.com/api/v2/homes_pdp_reviews?currency=HKD&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en&listing_id={}&_format=for_p3&limit=10000&offset=0&order=language_country'.format(id)
            yield items
            # Call function to scrape data only available on URL of individual listings (Details API)
            yield scrapy.Request(url=room_url, callback=self.parse_page, meta={'id': id})
            # Call function to scrape data only available on Reviews API
            yield scrapy.Request(url=room_reviews_api, callback=self.parse_reviews, meta={'id': id})



        # Pagination for Infinity Scrolling search page
        if pagination_metadata.get('has_next_page'):
            items_offset = pagination_metadata.get('items_offset')
            section_offset = pagination_metadata.get('section_offset')
            new_api = 'https://www.airbnb.com/api/v2/explore_tabs?_format=for_explore_search_web&auto_ib=true&client_session_id=250ad5ec-9986-42d5-a679-11c347c9ddfc&currency=HKD&current_tab_id=home_tab&experiences_per_grid=20&federated_search_session_id=d468fb24-b41e-4603-a586-9079a05f01d0&fetch_filters=true&guidebooks_per_grid=20&has_zero_guest_treatment=true&hide_dates_and_guests_filters=true&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true&items_offset={0}&items_per_grid=18&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&last_search_session_id=2ef27f8e-6856-46b4-bebd-d462604c34a8&locale=en&map_toggle=false&metadata_only=false&place_id=ChIJByjqov3-AzQR2pT0dDW0bUg&query=Hong%20Kong&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&s_tag=2D8gqHpx&satori_version=1.1.14&screen_height=773&screen_size=large&screen_width=1169&search_type=unknown&section_offset={1}&selected_tab_id=home_tab&show_groupings=true&source=mc_search_bar&supports_for_you_v3=true&tab_id=home_tab&timezone_offset=480&version=1.6.2'.format(
                items_offset, section_offset)
            yield scrapy.Request(url=new_api, callback=self.parse_id)

