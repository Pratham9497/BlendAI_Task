# api/views.py
import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .models import CustomUser, Watchlist

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_stock_info(request, symbol):
    """
    API endpoint to fetch stock information from Alpha Vantage.
    """
    # Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
    api_key = 'N78OB1PQIL0SI56P'
    base_url = 'https://www.alphavantage.co/query'
    
    # Define parameters for the API request
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '1min',  # Adjust interval as needed
        'apikey': api_key,
    }

    # Send request to Alpha Vantage API
    response = requests.get(base_url, params=params)

    # Check if request was successful
    if response.status_code == 200:
        data = response.json()
        # Extract latest stock price from the response
        latest_price = data['Time Series (1min)'][list(data['Time Series (1min)'].keys())[0]]['4. close']
        return Response({'symbol': symbol, 'latest_price': latest_price})
    else:
        return Response({'error': 'Failed to fetch stock information'}, status=response.status_code)

@api_view(['POST'])
@permission_classes([AllowAny])
def obtain_auth_token(request):
    """
    API endpoint to obtain authentication token.
    """
    # Delegate authentication to DRF's ObtainAuthToken view
    auth_view = ObtainAuthToken()
    response = auth_view(request)
    return response

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if username and password:
        user = CustomUser.objects.create_user(username=username, password=password)
        return Response({'message': 'User created successfully'})
    else:
        return Response({'error': 'Username and password required'}, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    auth_view = ObtainAuthToken()
    response = auth_view(request)
    token = Token.objects.get(key=response.data['token'])
    return Response({'token': token.key})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_watchlist(request):
    symbol = request.data.get('symbol')
    if symbol:
        watchlist = Watchlist(user=request.user, symbol=symbol)
        watchlist.save()
        return Response({'message': 'Symbol added to watchlist'})
    else:
        return Response({'error': 'Symbol required'}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_watchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user)
    symbols = [item.symbol for item in watchlist]
    return Response({'watchlist': symbols})
