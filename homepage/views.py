from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SearchForm
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthenticatedOrTokenHasPermission


def home(request):
    return render(request, 'home.html')

def explore_place(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            place_name = form.cleaned_data['place_name']
            print(f"User searched for: {place_name}")
            # Make a request to your backend API
            # api_url = f"http://localhost:8080/api/GetPlaceDetails/{place_name}"
            token=request.COOKIES.get('jwt_token')
            print(token)
            api_url = f"http://localhost:3030/api/GetPlaceDetails/{place_name}"
            response = requests.get(api_url)
            if response.status_code == 200:
                # Store the data in the session
                request.session['place_data'] = response.json()
                return redirect('explore_place_result')
            else:
                return HttpResponse("Failed to fetch place details.")
    else:
        form = SearchForm()
    return render(request, 'explore_place.html', {'form': form})

def explore_place_result(request):
    data = request.session.get('place_data')
    if not data:
        return HttpResponse("No data found.")
    
    if isinstance(data, list) and len(data) > 0:
        data = data[0]
    state_images = {
    'OD': 'https://media.istockphoto.com/id/1544985756/photo/odisha-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=W2R-rFG7DrDlyC-qMxHZD-Aw2Iuy3Gbb0jV-UG8FcBE=',
    'JH': 'https://media.istockphoto.com/id/1544985416/photo/jharkhand-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=P3uRE8g2s8NIi2Ef_2XvLoCMdK5tVzb7g1Lc91-jzkQ=',
    'SK': 'https://media.istockphoto.com/id/1544985948/photo/sikkim-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=d8vnYpuEga6yzHnMIXxagoHAISBn7HXv7oeHyhcueO4=',
    'PB': 'https://media.istockphoto.com/id/1544985944/photo/punjab-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=qtzjO6k3ID_OPcTXlEqF_NVuP_yX4zPi2YeM7kVCSaU=',
    'ML': 'https://media.istockphoto.com/id/1544985428/photo/meghalaya-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=lalaGG90nJd68L5QstAHixLxxJ1T6VIB9__tprwCTcg=',
    'MH': 'https://media.istockphoto.com/id/1544985420/photo/maharashtra-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=q_dxGh58hvk83ZElYT37f7UfiTsL8DFKzm-drfHc2cU=',
    'NL': 'https://static.vecteezy.com/system/resources/previews/036/124/901/original/nagaland-state-map-location-in-indian-3d-isometric-map-nagaland-map-illustration-vector.jpg',
    'UK': 'https://media.istockphoto.com/id/1544985958/photo/uttarakhand-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=rp9BidW9u9Q7QD7-MKnE5sD_K8i7UiZ2i6-JblJ_9NA=',
    'MZ': 'https://media.istockphoto.com/id/1544985947/photo/mizoram-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=48cW-20CLnIEQhXBY3gJDsyrbOVYZ-cxeIgCbI_yfBc=',
    'AR': 'https://media.istockphoto.com/id/1544984896/photo/arunachal-pradesh-and-nagaland-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=Zq2E05wuAbIHXIdd4tZQmH7ZFvYteLgAIej-G83mfRU=',
    'WB': 'https://media.istockphoto.com/id/1544985962/photo/west-bengal-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=CW-5Dk40HtHN7MpafPoeqjLh6868p9-yC0e-_5-GK7A=',
    'KL': 'https://media.istockphoto.com/id/1460444658/vector/india-map-graphic-travel-geography-icon-indian-region-kerala-vector-illustration.jpg?s=1024x1024&w=is&k=20&c=TsFOeVcQXzHHTmHM_XeWGBfv4o5v5mEDMq3bnj0jr84=',
    'CG': 'https://media.istockphoto.com/id/1184114632/vector/chhattisgarh-red-highlighted-in-map-of-india.jpg?s=1024x1024&w=is&k=20&c=nYAanpBZ5eY6ma_D1GYxkwYvrbEZWv6PEV5KQ7nIIVY=',
    'KA': 'https://media.istockphoto.com/id/1544985417/photo/karnataka-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=BVUOlyXXSpwY7fSzHTJ2jteVP74xLfHicxcd_jn0-cU=',
    'GJ': 'https://media.istockphoto.com/id/1544985405/photo/gujarat-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=PPHkgt0RpaaCsyNp6q6vhDrCika3tT0S8vKsj_tvMHU=',
    'MN': 'https://media.istockphoto.com/id/1544985427/photo/manipur-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=t87SwSX5_tdLm-043N9l5LU4ZpF428f8mnUgU8kBz60=',
    'BR': 'https://media.istockphoto.com/id/850869380/vector/bihar-red-on-gray-india-map-vector.jpg?s=1024x1024&w=is&k=20&c=e8XOp0PcJw81mrQcvXXPQRci0d_eBrd6r003Nxzy8vA=',
    'UP': 'https://media.istockphoto.com/id/1544985957/photo/uttar-pradesh-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=PTs-UNrzPFn7Swu0umveenbS-b7m7Kdks6lI9FDof44=',
    'HP': 'https://media.istockphoto.com/id/1544985411/photo/himachal-pradesh-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=DDERq8_7ps39l8PFrKB8Gv4FwSR8ehbp6C5ewMVGG_c=',
    'AP': 'https://media.istockphoto.com/id/1544984897/photo/andhra-pradesh-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=clBP8WsrpvwLdiUASL3g1MiEU6Cp-t0SHskOuqeMq6c=',
    'TN': 'https://media.istockphoto.com/id/1544985952/photo/tamil-nadu-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=UCA2p-JdeCcn_rELhwoXXvoeqvTIdJpdYC--EF6US8E=',
    'TR': 'https://media.istockphoto.com/id/1544985954/photo/tripura-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=FZEx7wcZBYv0Bce0jdogAhmbgKT6K82t9Kiy9sJ0NYY=',
    'RJ': 'https://media.istockphoto.com/id/1544985951/photo/rajasthan-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=C5eXesReNaNwh7XJ6T2f92RFFbHj6WG2omYynr6olwY=',
    'TS': 'https://media.istockphoto.com/id/1544985955/photo/telangana-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=YKeGjJVbgNPjSxjHDujCUII_NQm7XDSZA-fTC6d4K-I=',
    'MP': 'https://media.istockphoto.com/id/1544985421/photo/madhya-pradesh-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=SrSOcH7up3rtYFmBg0fXjEA5Z0WMq-aNEBl2DACkoB8=',
    'HR': 'https://static.vecteezy.com/system/resources/previews/036/124/850/original/haryana-map-location-in-indian-3d-isometric-map-haryana-map-illustration-vector.jpg',
    'AS': 'https://media.istockphoto.com/id/1544984892/photo/assam-state-location-within-india-map-3d-illustration.jpg?s=1024x1024&w=is&k=20&c=ITdRHu1nBsM42TnypyTfh-lVGHdi9cSOjQaay2oFrao=',
    'GA': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/IN-GA.svg/450px-IN-GA.svg.png',
}

    
    state_id = data.get('stateid')
    image_url = state_images.get(state_id, 'https://media.istockphoto.com/id/502811578/photo/india.jpg?s=1024x1024&w=is&k=20&c=Ls_9K3drasbw5O4MtG40wKjEmK7kE-EnppZBfxz_G2I=')
    # for specific json data
    context = {
        'state': data.get('state'),
        'place_name': data.get('placename'),
        'place_details': data.get('placedetails'),
        'image_url': image_url

    }
    return render(request, 'explore_place_result.html', context)
