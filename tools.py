#define a tools array. Each tool is a function like from the one above we created with their specified parameters.
tools = [
    {
        "type": "function",
        "function" : {
            "name": "get_hotel_offers",
            "description": "Get the hotel offers in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "city/state, e.g. Portland/OR",
                    },
                    "check_in_date": {
                    "type" : "string",
                    "description": "Check-in date of the stay (hotel local date). Format YYYY-MM-DD.\
                      The lowest accepted value is the present date (no dates in the past).\
                      If not present, the default value will be today's date in the GMT time zone. \
                      Example : 2025-11-22"
                    },
                    "check_out_date": {
                    "type" : "string",
                    "description": "Check-out date of the stay (hotel local date). Format YYYY-MM-DD.\
                      The lowest accepted value is check_in_date+1. If not present, it will default to check_in_date +1. Example : 2025-11-23 "
                    },
                },
                "required":["location"],
            },
        }
    }
]