import os
import json
import glob
import re
import base64

from django.http import JsonResponse
from django.http import FileResponse
from django.http import HttpResponse
from django.core.files import File

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.shortcuts import render

from datetime import datetime
from PIL import Image



# Create your views here.


@api_view(['GET'])
def get_stations(request):
    directory = "/home/Mobin/OUTPUT/CurrentWeather/30Current/"
    data = []
    for files in os.listdir(directory):
        file_path = os.path.join(directory, files)
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            name = json_data['name']
            lat = json_data['coord']['lat']
            long = json_data['coord']['lon']
            visibility = json_data['visibility']/1000
            temp = round(json_data['main']['temp'] - 273.15, 4)
            humidity = json_data['main']['humidity']
            pressure = json_data['main']['pressure']
            wind_speed = json_data['wind']['speed']
            wind_deg = json_data['wind']['deg']
            dt = datetime.fromtimestamp(json_data['dt']) 
            data.append({'Name': name, 
                         'Lat': lat, 'Lon': long ,
                         'Visibility':visibility,
                         'Temp':temp,
                         'Humidity':humidity,
                         'Pressure':pressure,
                         'Wind_speed':wind_speed,
                         'Wind_deg':wind_deg,
                         'Date Time':dt})
            
                    
    return JsonResponse(data , safe=False)                
            
                    
    
def list_images(request):
    image_folder = '/home/Mobin/OUTPUT/WRF01/wrfpostSitepro_v04/2023090800/ME_NV/' 
    png_files = glob.glob(os.path.join(image_folder, '*.png'))
    return JsonResponse({'images': png_files})    
    
    
    
@csrf_exempt
def get_image(request, image_name):
    image_folder = '/home/Mobin/OUTPUT/WRF01/wrfpostSitepro_v04/2023090800/ME_NV/'
    image_path = os.path.join(image_folder , image_name)
    print(image_path)

    if os.path.exists(image_path):
        return FileResponse(open(image_path, 'rb'), content_type='image/jpeg')
    else:
        return HttpResponse(status=404)
    
    
def categorize_images(request):
    image_folder = '/home/Mobin/OUTPUT/WRF01/wrfpostSitepro_v04/2023090800/ME_NV/' 
    image_files = glob.glob(os.path.join(image_folder, 'IMG-*.png')) 
    
    categorized_images = {}  #
    

    patterns = [
        (r'IMG-AA001', 'Surface (10 meter) Wind Barbs, Streamlines, Isotachs [kts]'),
        (r'IMG-AA002', '#'),
        (r'IMG-AA102', '24-hour Average Surface Temperature [degC]'),
        (r'IMG-AA302', '24-hour Maximmum Surface Temperature [degC]'),
        (r'IMG-AA502', '24-hour Minumum Surface Temperature [degC]'),
        (r'IMG-AA202', '7 Days Average Surface Temperature [degC]'),
        (r'IMG-AA402', '7 Days Maximum Surface Temperature [degC]'),
        (r'IMG-AA602', '7 Days Minumum Surface Temperature [degC]'),
        (r'IMG-AA003', '200 mb Heights [m] Isotachs [kts] Temp [C]'),
        (r'IMG-AA004', '300 mb Heights [m] Isotachs [kts] Temp [C]'),
        (r'IMG-AA005', '500 mb Heights [m] and Rel. Vort [10-5 s-1]'),
        (r'IMG-AA006', '700 mb heights, Rel. Hum. [%], Vertical Velocity [Pa/s]'),
        (r'IMG-AA007', '850 mb Temperature [C], winds [kts] and Rel. Hum. [%]'),
        (r'IMG-AA008', '1000-500 Thickness [dm] and Sea Level Pressure [mb]'),
        (r'IMG-AA009', 'Previous 3-hr Precipitation Rate [mm] and Sea Level Pressure [mb]'),
        (r'IMG-AA109', 'Previous 6-hr Precipitation Rate [mm] and Sea Level Pressure [mb]'),
        (r'IMG-AA209', 'Previous 12-hr Precipitation Rate [mm] and Sea Level Pressure [mb]'),
        (r'IMG-AA309', 'Previous 24-hr Precipitation Rate [mm] and Sea Level Pressure [mb]'),
        (r'IMG-AA409', 'Previous 7 Days Precipitation Rate [mm] and Sea Level Pressure [mb]'),
        (r'IMG-AA010', '#'),
        (r'IMG-AA011', '30K-38K ft Clear Air Turbulence   9.14 - 11.6'),
        (r'IMG-AA012', '22K-30K ft Clear Air Turbulence   6700 - 9.14'),
        (r'IMG-AA013', '#'),
        (r'IMG-AA014', '#'),
        (r'IMG-AA015', 'Tropopause Pressure [mb]'),
        (r'IMG-AA016', 'K-Index'),
        (r'IMG-AA017', '#'),
        (r'IMG-AA018', '#'),
        (r'IMG-AA019', '#'),
        (r'IMG-AA020', '#'),
        (r'IMG-AA021', '#'),
        (r'IMG-AA022', '#'),
        (r'IMG-AA023', '#'),
        (r'IMG-AA024', '#'),
        (r'IMG-AA025', 'Sea Surface Temperature'),
        (r'IMG-AA026', '5000  ft Isotachs [kts], Rel. Hum. [%], Vertical Velocity [Pa/s]'),
        (r'IMG-AA027', '10000 ft Isotachs [kts], Rel. Hum. [%], Vertical Velocity [Pa/s]'),
        (r'IMG-AA028', '15000 ft Isotachs [kts], Rel. Hum. [%], Vertical Velocity [Pa/s]'),
        (r'IMG-AA029', '20000 ft Isotachs [kts], Rel. Hum. [%], Vertical Velocity [Pa/s]'),
        (r'IMG-AA030', '25000 ft Isotachs [kts], Rel. Hum. [%], Vertical Velocity [Pa/s]'),
        (r'IMG-AA031', '30000 ft Isotachs [kts], Rel. Hum. [%], Vertical Velocity [Pa/s]'),
        (r'IMG-AA032', '35000 ft Isotachs [kts], Rel. Hum. [%], Vertical Velocity [Pa/s]'),
        (r'IMG-AA033', '700 mb Vertical Velocity [Pa/s]'),
        (r'IMG-AA034', '200 mb Streamlines, Isotachs [kts]'),
        (r'IMG-AA035', 'Precipitable Water [mm], Convective Available Potential Energy [J/kg]'),
        (r'IMG-AA036', '800, 500 and 300 mb Relative Humidity [%]'),
        (r'IMG-AA037', 'Surface Winds [kts], Sea Level Pressure [mb]'),
        (r'IMG-AA040', 'Surface Dust Concentration [mg/m3]'),
    ]

    for image_file in image_files:
        image_name = os.path.basename(image_file)
        
        # بررسی هر الگو برای استخراج کلید
        for pattern, key in patterns:
            if re.search(pattern, image_name):
                if key not in categorized_images:
                    categorized_images[key] = []
                categorized_images[key].append(image_name)

    return JsonResponse({'categorized_images': categorized_images})  





@api_view(['GET'])
def get_dates(request):
    directory = "/home/Mobin/OUTPUT/WRF01/wrfpostSitepro_v04"
    
    folders = [name for name in os.listdir(directory) 
               if os.path.isdir(os.path.join(directory, name))]
    
    folders_sorted = sorted(folders)
    
    modified_folders = [folder[0:10] for folder in folders_sorted]
    
    json_response = {"dates": modified_folders}

    return JsonResponse(json_response, safe=False) 

@api_view(['GET'])
@permission_classes([AllowAny])
def show_image(request, date, nv_type, folder_pic, pic_name):
    try:
        if nv_type not in ['ME_NV', 'IR_NV']:
            return JsonResponse({'error': 'Invalid nv_type'}, status=400)
        folder_path = f"/home/Mobin/OUTPUT/WRF01/wrfpostSitepro_v04/{date}/"


        if not os.path.exists(folder_path):
            return JsonResponse({'error': 'Folder not found'}, status=404)


        nv_folder_path = os.path.join(folder_path, nv_type)


        if not os.path.exists(nv_folder_path):
            return JsonResponse({'error': f'{nv_type} folder not found'}, status=404)


        pic_folder_path = os.path.join(nv_folder_path, folder_pic)

        if not os.path.exists(pic_folder_path):
            return JsonResponse({'error': f'Folder {folder_pic} not found'}, status=404)


        pic_path = os.path.join(pic_folder_path, pic_name)


        if not os.path.exists(pic_path):
            return JsonResponse({'error': f'Picture {pic_name} not found'}, status=404)

        return FileResponse(open(pic_path, 'rb'), content_type='image/jpeg')
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['GET'])
def parametere_pic(request):
    model = request.GET.get("model")
    datetime = request.GET.get("datetime")
    domain = request.GET.get("domain")
    patameter = request.GET.get("parameter")
    pic_name = request.GET.get("pic_name")
    
    
    path = f'/home/Mobin/OUTPUT/{model}/wrfpostSitepro_v04/{datetime}/{domain}/{patameter}/{pic_name}.png'
    return FileResponse(open(path, 'rb'), content_type='image/png')


from rest_framework import status
from rest_framework.response import Response
from subprocess import run, PIPE
import tempfile
import os
from datetime import datetime, timedelta
#from .utils import get_folder_name
@api_view(['GET'])
def soundingView(request):
    model  = request.GET.get("model")
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")
    hour = int(request.GET.get("hour"))
    domain = request.GET.get("domain")
    cycle = request.GET.get("datetime")
    
    
    if hour==0:
        hour=cycle
    elif hour > 0:
        cycle_str = str(cycle)
        cycle_date = datetime.strptime(cycle_str, "%Y%m%d%H")
        cycle_date += timedelta(hours=hour)
        hour = cycle_date.strftime("%Y%m%d%H")
    print("houuuuurrrrrrrr",hour)   
             
    date = hour [0:8]
    time = hour [8:10]+ '00'

    script_path = '/home/Mobin/ArProject/Scripts/SQTPro/plotLowSkewT/genSkewT.sh'
    last_gfs = f'/home/Mobin/OUTPUT/{model}/{model}_output/wind_forecasts/gfs.{cycle}'
    print(last_gfs)
    # last_gfs = os.listdir('/home/Mobin/OUTPUT/WRF01_output/wind_forecasts/')[-1]
    # input_folder = last_gfs.split('.')[-1]
    input_folder = f"{cycle}"
    input_path = f'/home/Mobin/OUTPUT/{model}/{model}_output/wind_forecasts'
    pic_path = f'/home/Mobin/OUTPUT/{model}/{model}_Skewt/SkewTOUT/{lat}_{lon}/{date}_{time}.png' 
    out_path = f'/home/Mobin/OUTPUT/{model}/{model}_Skewt/SkewTOUT'
    cwd_path = os.path.dirname(script_path)

    #print(input_folder , d , input_path ,out_path, lat , lon , datetimes)
    #print(pic_path)
    if domain == "ME_NV":
        domain = "d01"
    elif domain == "IR_NV":
        domain = "d02"    

    result = run(['bash', script_path, input_folder , domain  , input_path ,out_path, lat , lon , hour], stdout=PIPE, stderr=PIPE , cwd=cwd_path)

    if result.returncode == 0:
        print(pic_path)
        return FileResponse(open(pic_path, 'rb'), content_type='image/png')
        #image_path = result.stdout.strip()

    else:
        return Response({'error': result.stderr}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


import subprocess
        
def CrossSectionView(request):
    model = request.GET.get("model")
    startlat = float(request.GET.get("startlat"))
    endlat = float(request.GET.get("endlat"))
    startlon = float(request.GET.get("startlon"))
    endlon = float(request.GET.get("endlon"))
    datetmes = int(request.GET.get("hour"))
    domain = request.GET.get("domain")
    cycle = request.GET.get("datetime")
    # last_gfs = os.listdir('/home/Mobin/OUTPUT/WRF01_output/wind_forecasts/')[-1]

    if datetmes==0:
        datetmes=cycle
    elif datetmes > 0:
        cycle_str = str(cycle)
        cycle_date = datetime.strptime(cycle_str, "%Y%m%d%H")
        cycle_date += timedelta(hours=datetmes)
        datetmes = cycle_date.strftime("%Y%m%d%H")
    print(datetmes) 

    dates = datetmes[0:8]
    initial_date = datetime.strptime(dates, "%Y%m%d")
    date = initial_date.strftime("%Y-%m-%d")
    time = datetmes[8:10]+ ':00:00'
    last_gfs = f'/home/Mobin/OUTPUT/{model}/{model}_output/wind_forecasts/gfs.{cycle}'
    location_config = f"/home/Mobin/OUTPUT/{model}/{model}_crossSection/Cross_Section_code/Location-config.txt"
    path_config_d01 = f"/home/Mobin/OUTPUT/{model}/{model}_crossSection/Cross_Section_code/path-config-file-d01.txt"
    path_config_d02 = f"/home/Mobin/OUTPUT/{model}/{model}_crossSection/Cross_Section_code/path-config-file-d02.txt"
    pic_pathd01 = f"/home/Mobin/OUTPUT/{model}/{model}_crossSection/WRF_d01/wrfout_d01_{date}_{time}.png"
    pic_pathd02 = f"/home/Mobin/OUTPUT/{model}/{model}_crossSection/WRF_d02/wrfout_d02_{date}_{time}.png"
    with open(location_config, 'r') as f:
        lines = f.readlines()
    lines = lines[:-1]
    new_line = f"{startlat} {endlat} {startlon} {endlon}"
    lines.append(new_line)

    with open(location_config, 'w') as f:
        f.writelines(lines)
    if domain == "ME_NV":  
        path_config = f"/home/Mobin/OUTPUT/{model}/{model}_output/wind_forecasts/" + f"gfs.{cycle}" + "/wrfout_d01_" + date + "_" + time + ".mean.nc"
        with open(path_config_d01, 'r') as f:
            lines = f.readlines()
        lines = lines[:-1]
        new_line = f"{path_config}"
        lines.append(new_line)
        with open(path_config_d01, 'w') as f:
            f.writelines(lines)
        # /home/wdmodel/OUTPUT/WRF01/WRF01_crossSection/WRF_d01
        ncl_script = f"/home/Mobin/OUTPUT/{model}/{model}_crossSection/Cross_Section_code/MainCode3Plots_d01.ncl"
        dirOut = f"dirOut=\"/home/Mobin/OUTPUT/{model}/{model}_crossSection/WRF_d01\""
        cwd_path = os.path.dirname(ncl_script)
        result = run(['ncl', ncl_script,dirOut], stdout=PIPE, stderr=PIPE , cwd=cwd_path)    
        if result.returncode == 0:
        	return FileResponse(open(pic_pathd01, 'rb'), content_type='image/png') 
        else:
            return Response({'error': result.stderr}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    elif domain == "IR_NV":
        path_config = f"/home/Mobin/OUTPUT/{model}/{model}_output/wind_forecasts/" + f"gfs.{cycle}" + "/wrfout_d02_" + date + "_" + time + ".mean.nc"
        with open(path_config_d02, 'r') as f:
            lines = f.readlines()
        lines = lines[:-1]
        new_line = f"{path_config}"
        lines.append(new_line)
        with open(path_config_d02, 'w') as f:
            f.writelines(lines)
        ncl_script = f"/home/Mobin/OUTPUT/{model}/{model}_crossSection/Cross_Section_code/MainCode3Plots_d02.ncl"
        dirOut = f"dirOut=\"/home/Mobin/OUTPUT/{model}/{model}_crossSection/WRF_d02\""
        cwd_path = os.path.dirname(ncl_script)
        result = run(['ncl', ncl_script,dirOut], stdout=PIPE, stderr=PIPE , cwd=cwd_path) 
           
        if result.returncode == 0:
            return FileResponse(open(pic_pathd02, 'rb'), content_type='image/png')
        else:
            return Response({'error': result.stderr}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # f"dirOut=\"/home/Mobin/OUTPUT/WRF01/WRF01_crossSection/WRF_d02\""
            # f"dirOut=\"/home/wdmodel/OUTPUT/{model}/{model}_crossSection/WRF_d02\""
            # /home/wdmodel/OUTPUT/WRF01/WRF01_output/gfs.2024051100/wrfout_d02_2024-05-11_07:00:00.mean.nc
            # /home/wdmodel/OUTPUT/WRF01/WRF01_crossSection/WRF_d02



def run_ncl_script(request):
    ncl_script_path = f"/home/wdmodel/OUTPUT/WRF01/WRF01_crossSection/Cross_Section_code/MainCode3Plots_d02.ncl"
    cwd_path = os.path.dirname(ncl_script_path)
    dirOut=f"dirOut=\"/home/Mobin/OUTPUT/WRF01/WRF01_crossSection/WRF_d02\""
    try:
        result = subprocess.run(['ncl', ncl_script_path,dirOut], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,cwd=cwd_path)
        print("Standard Output:")
        print(result.stdout.decode('utf-8'))
        print("Standard Error:")
        print(result.stderr.decode('utf-8'))
        if result.returncode == 0:
            return JsonResponse("Script executed successfully!",safe=False)
        else:
            return JsonResponse("Script execution failed with return code:", result.returncode,safe=False)
    except subprocess.CalledProcessError as called_process_error:
        return JsonResponse("Script execution failed:", called_process_error, safe=False)

