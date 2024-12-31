# Hotel Assistant Bot

An AI-powered travel assistant that helps users find hotel offers using OpenAI's GPT and Amadeus API. The assistant can search for hotels in specific cities, handle date-based queries, and provide detailed hotel information.

## Features

- Natural language interaction using OpenAI's GPT model
- City code lookup functionality
- Hotel search by city
- Real-time hotel offers with pricing
- Date-specific hotel availability search
- Automated conversation handling

## Prerequisites

- Python 3.x
- OpenAI API key
- Amadeus API credentials (Client ID and Secret)
- Required Python packages:
  - openai
  - amadeus
  - python-dotenv
  - PyPDF2

## Installation

1. Clone the repository:
```bash
git clone https://github.com/SizweVezi/AITravelAgent.git
cd [repository-name]
```

2. Install required packages:
```bash
pip install openai amadeus python-dotenv PyPDF2
```

3. Create a `.env` file in the project root with your API credentials:
```env
OPENAI_API_KEY=your_openai_api_key
CLIENT_ID=your_amadeus_client_id
CLIENT_SECRET=your_amadeus_client_secret
```

## Usage

The assistant can handle queries like:
```
"Find hotels in Las Vegas from November 22 to November 25"
"What are the available hotels in New York for next week?"
"Show me hotel options in Paris for tomorrow"
```

## Code Structure

### Core Functions

1. City Code Search:
```python
def city_code_search(city_name):
    # Converts city names to Amadeus city codes
```

2. Hotel Search:
```python
def hotel_city_search(cityCode):
    # Finds hotels in a specific city
```

3. Hotel Offers:
```python
def hotel_offers_search(hotelIds, checkInDate, checkOutDate):
    # Retrieves hotel offers for specific dates
```

### API Integration

1. OpenAI Setup:
```python
client = OpenAI(
    api_key=os.environ.get("openai_api_key")
)
```

2. Amadeus Setup:
```python
amadeus = Client(
    client_id=os.environ.get("CLIENT_ID"),
    client_secret=os.environ.get("CLIENT_SECRET")
)
```

## Error Handling

The application includes comprehensive error handling for:
- API authentication errors
- City code lookup failures
- Hotel search errors
- Invalid date formats
- Network issues

## Response Format

Hotel offers are returned in JSON format containing:
- Hotel information
- Price details
- Available rooms
- Booking conditions
- Check-in/out times

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## Future Improvements

- Add support for room preferences
- Include price filtering
- Add hotel ratings and reviews
- Implement booking functionality
- Add support for multiple cities comparison

## License

[Choose appropriate license]

## Disclaimer

This project uses the OpenAI API and Amadeus API, which may incur costs based on usage. Please review their pricing structures before use.

---

## Support

For issues and feature requests, please open an issue in the repository.
