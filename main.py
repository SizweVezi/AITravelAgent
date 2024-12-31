import os
from datetime import date, timedelta
import time
from http.client import responses

from openai import OpenAI, completions, models, api_key
from dotenv import load_dotenv, find_dotenv
import json
from amadeus import Client, ResponseError
import tools

#initiating environment variables.
_= load_dotenv(find_dotenv())

#integrating openai api
client = OpenAI(
    api_key=os.environ.get("openai_api_key")
  )

#Intergrating Amadeus api
amadeus = Client(
    client_id=os.environ.get("CLIENT_ID"),
    client_secret=os.environ.get("CLIENT_SECRET")
)

#City code function to retrieve city names by using city codes.
def city_code_search(city_name):
    try:
        response = amadeus.reference_data.locations.get(keyword=city_name, subType='CITY')
        return response.data[0]['address']['cityCode']
    except ResponseError as error:
        return str(error)

#Hotel city search. Fetches hotels by city code.
def hotel_city_search(cityCode):
    try:
        response = amadeus.reference_data.locations.hotels.by_city.get(cityCode = cityCode)
        hotel_names = [item['hotelId'] for item in response.data[:50]]
        return hotel_names
    except ResponseError as error:
        return str(error)

#Hotel offer search by hotelId check-in date and check-out date
def hotel_offers_search(hotelIds, checkInDate = date.today(), checkOutDate = date.today() + timedelta(days=1)):
    try:
        response = amadeus.shopping.hotel_offers_search.get(
            hotelIds = hotelIds,
            checkInDate = checkInDate,
            checkOutDate = checkOutDate
        )
        return response.data
    except ResponseError as error:
        return str(error)

#Get hotel offers wrapper

def get_hotel_offers(location, check_in_date=date.today(), check_out_date=date.today() + timedelta(days=1)):
    try:
        city_code = city_code_search(location)
        if not city_code:
            return json.dumps({"error": "City code not found"})

        hotel_ids = hotel_city_search(city_code)
        if not hotel_ids:
            return json.dumps({"error": "No hotels found"})

        hotel_offers = hotel_offers_search(hotel_ids, check_in_date, check_out_date)
        if not hotel_offers:
            return json.dumps({"error": "No offers found"})

        return json.dumps(hotel_offers)
    except Exception as e:
        return json.dumps({"error": str(e)})

#JSON Tools for assistant
assistant_tools=tools.tools

assistant = client.beta.assistants.create(
    instructions="You are a travel agent. Use the provided functions to answer questions. Please do not share the booking link",
    model="gpt-3.5-turbo",
    tools=assistant_tools
)

#Creating a thread that will represent the conversation
thread = client.beta.threads.create()
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=input('>' )
)
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)
#
# run_status = client.beta.threads.runs.retrieve(
#   thread_id=thread.id,
#   run_id=run.id
# )
#
# print(run_status)

while run.status != 'completed':
    time.sleep(1)
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    if run.status == "requires_action":
        required_action = run.required_action

        if required_action.type == "submit_tool_outputs":
            tool_outputs = []

            for tool_call in required_action.submit_tool_outputs.tool_calls:
                if tool_call.type == 'function':
                    function_name = tool_call.function.name
                    arguments_json = tool_call.function.arguments

                    try:
                        arguments = json.loads(arguments_json)
                        function_mapping = {
                            "get_hotel_offers": get_hotel_offers
                        }

                        if function_name in function_mapping:
                            print('Calling function: ', function_name, arguments_json)
                            response = function_mapping[function_name](**arguments)

                            # Ensure response is not None and is a string
                            if response is None:
                                response = json.dumps({"error": "No response from function"})
                            elif not isinstance(response, str):
                                response = json.dumps(response)

                            print('Function response:', response)
                            tool_outputs.append({
                                "tool_call_id": tool_call.id,
                                "output": response,
                            })
                    except Exception as e:
                        error_response = json.dumps({"error": str(e)})
                        tool_outputs.append({
                            "tool_call_id": tool_call.id,
                            "output": error_response,
                        })

            print('Submit the tool outputs to the thread and run')
            run = client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )






















"""
def get_hotel_offers(location, check_in_date = date.today(), check_out_date = date.today() + timedelta(days=1)):
    city_code = city_code_search(location)
    if isinstance(city_code, str) and "error" in city_code.lower():
        return json.dumps({"error": city_code})

    hotel_ids = hotel_city_search(city_code)
    if isinstance(hotel_ids, str) and "error" in hotel_ids.lower():
        return json.dumps({"error": hotel_ids})

    hotel_offers = hotel_offers_search(hotel_city_search(city_code_search(location)), check_in_date, check_out_date)
    if isinstance(hotel_offers, str) and "error" in hotel_offers.lower():
        return json.dumps({"error": hotel_offers})

        # return json.dumps(hotel_offers)
    # except Exception as e:
    #         return json.dumps({"error": str(e)})
"""









"""
while run.status != 'completed':
    time.sleep(1)
    run = client.beta.threads.runs.retrieve(
       thread_id=thread.id,
       run_id=run.id
    )
    if run.status == "requires_action":
        required_action = run.required_action

        if required_action.type == "submit_tool_outputs":
            tool_outputs = []

        for tool_call in required_action.submit_tool_outputs.tool_calls:
            if tool_call.type == 'function':
                function_name = tool_call.function.name
                arguments_json = tool_call.function.arguments

                arguments = json.loads(arguments_json)

                function_mapping = {
                    "get_hotel_offers":get_hotel_offers,
                 }

                if function_name in function_mapping:
                    print('Calling function: ', function_name, arguments_json)
                    response = function_mapping[function_name](**arguments)
                    print('Function response:', response)
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": response,
                    })
                    # print(tool_outputs)

                print('Submit the tool outputs to the thread and run')
                run = client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
"""
