#!/usr/bin/env python
# -*- coding: utf-8
# ---------------------------------------------------------------------------
# FusionVersion.py
# Created on: 2019-01-15 12:20:06.00000
# Description: Copiar en la carpeta TLSpath los archivos de TLS filtrados y cortados. Copiar en la carpeta E:\Palancia\TLS\1_Raw_Files\Photogrammetry la nube de puntos obtenida mediante fotogrametría.
# ---------------------------------------------------------------------------
import os, subprocess, tkinter, csv
from osgeo import ogr
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory



def GetValueCSV(CSVFile, row, column):
    with open(CSVFile, 'rb') as f:
        mycsv = csv.reader(f)
        mycsv = list(mycsv)
        text = mycsv[row][column]
        return text

def DTM2ASCII(dtmfile):
    process_name=".\\3rdParty\\FusionLDV\\DTM2ASCII.exe"
    arg=" /raster "+dtmfile
    subprocess.call(process_name+arg,shell=True)
    return ("Created the ASCII file "+dtmfile)


def LAS2SHPboundary(pointcloud, shapefile):
    #Obtencion del contorno en formato shp de los ficheros las
    process_name=".\\3rdParty\\LAStools\\bin\\lasboundary.exe"
    arg=" -i "+pointcloud+" -o "+shapefile
    subprocess.call(process_name+arg,shell=True)
    print ("Created the boundary file "+shapefile+", from the file "+pointcloud)

def LAS2GROUND(inputpath,outputpath,switcheslas2ground="",switcheslassplit=""):
    #Obtencion de un fichero LAS de puntos del terreno
    print ("Creating the ground file: "+outputpath+" ...")
    process_name=".\\3rdParty\\LAStools\\bin\\lasground.exe "
    arg= "-i "+inputpath+" -o "+outputpath+" -hyper_fine "+switcheslas2ground
    subprocess.call(process_name+arg,shell=True)

    process_name=".\\3rdParty\\LAStools\\bin\\lassplit.exe"
    arg=" -i "+outputpath+" -o "+outputpath+" -by_classification -keep_class 2 "+switcheslassplit
    subprocess.call(process_name+arg,shell=True)

    os.remove(outputpath)
    os.rename(os.path.splitext(outputpath)[0]+"_0000002.las", outputpath)


def LAS2RASTER (inputpath,outputpath):
    process_name=".\\3rdParty\\FusionLDV\\GridSurfaceCreate.exe"
    arg= " "+outputpath+" 0.05 m m 1 30 2 3 "+inputpath
    subprocess.call(process_name+arg,shell=True)
    DTM2ASCII(outputpath)

def LAS2CLIP (inputpath,shp,outputpath):
    process_name=".\\3rdParty\\LAStools\\bin\\lasclip.exe"
    arg=" -i "+inputpath+" -poly "+shp+" -split -o "+outputpath
    subprocess.call(process_name+arg,shell=True)

def LASCLOUDMETRICS(inputpath,outputpath):
    process_name=".\\3rdParty\\FusionLDV\\CloudMetrics.exe"
    arg=" "+inputpath+" "+outputpath
    subprocess.call(process_name+arg,shell=True)

def LAS2HEIGHTS(inputlas,inputground,output,switches):
    process_name=".\\3rdParty\\LAStools\\bin\\lasheight.exe"
    arg= " -i "+str(inputlas)+" -ground_points "+str(inputground)+" -o "+str(output)+" "+str(switches)
    subprocess.call(process_name+arg,shell=True)

def createBuffer(inputfn, outputBufferfn, bufferDist):
    inputds = ogr.Open(inputfn)
    inputlyr = inputds.GetLayer()

    shpdriver = ogr.GetDriverByName('ESRI Shapefile')
    if os.path.exists(outputBufferfn):
        shpdriver.DeleteDataSource(outputBufferfn)
    outputBufferds = shpdriver.CreateDataSource(outputBufferfn)
    bufferlyr = outputBufferds.CreateLayer(outputBufferfn, geom_type=ogr.wkbPolygon)
    featureDefn = bufferlyr.GetLayerDefn()

    for feature in inputlyr:
        ingeom = feature.GetGeometryRef()
        geomBuffer = ingeom.Buffer(bufferDist)

        outFeature = ogr.Feature(featureDefn)
        outFeature.SetGeometry(geomBuffer)
        bufferlyr.CreateFeature(outFeature)
        outFeature = None

def DivideSHP (inputshp,outfolder):
    #Crea un fichero SHP por cada entidad del fichero SHP de input
    
    # Get the input Layer
    inShapefile = inputshp
    inDriver = ogr.GetDriverByName("ESRI Shapefile")
    inDataSource = inDriver.Open(inShapefile, 0)
    inLayer = inDataSource.GetLayer()
    
    # Add features to the output Layer
    for i in range(0, inLayer.GetFeatureCount()):
        inShapefile = inputshp
        inDriver = ogr.GetDriverByName("ESRI Shapefile")
        inDataSource = inDriver.Open(inShapefile, 0)
        inLayer = inDataSource.GetLayer()
        # Create the output Layer
        outShapefile = outfolder+"Polygon"+str(i).zfill(6)+".shp"
        outDriver = ogr.GetDriverByName("ESRI Shapefile")
        
        # Remove output shapefile if it already exists
        if os.path.exists(outShapefile):
            outDriver.DeleteDataSource(outShapefile)
        
        # Create the output shapefile
        outDataSource = outDriver.CreateDataSource(outShapefile)
        outLayer = outDataSource.CreateLayer("Polygon"+str(i).zfill(6), geom_type=ogr.wkbPolygon)
        
        # Add input Layer Fields to the output Layer
        inLayerDefn = inLayer.GetLayerDefn()
        for x in range(0, inLayerDefn.GetFieldCount()):
            fieldDefn = inLayerDefn.GetFieldDefn(x)
            outLayer.CreateField(fieldDefn)
            
    
    
        # Get the output Layer's Feature Definition
        outLayerDefn = outLayer.GetLayerDefn()
    
        inFeature = inLayer.GetNextFeature()
        n=0
        while inFeature:
            if n==i: 
                # get the input geometry
                geom = inFeature.GetGeometryRef()
                # create a new feature
                outFeature = ogr.Feature(outLayerDefn)
                # set the geometry and attribute
                outFeature.SetGeometry(geom)
                for iterator in range(0, outLayerDefn.GetFieldCount()):
                    outFeature.SetField(outLayerDefn.GetFieldDefn(iterator).GetNameRef(), inFeature.GetField(iterator))
                # add the feature to the shapefile
                outLayer.CreateFeature(outFeature)
                # dereference the features and get the next input feature
                outFeature = None
            inFeature = inLayer.GetNextFeature()
            n+=1
        inFeature = None
        outFeature = None
    
    # Save and close DataSources
    inDataSource = None
    outDataSource = None
    
    
    
    

# Local variables:
root = tkinter.Tk()
root.withdraw() # hide root
dirname = askdirectory(title="Select output directory")+"/"
#dirname = "E:/Palancia/_Canas/PRUEBA_DATOS_PNOA/"
shp_file = askopenfilename(title = "Select .SHP file",filetypes = [("SHP files","*.shp")])
#shp_file ="E:/Palancia/TLS/1_Raw_Files/SHP/cañas_palancia.shp"
las_raw_file= askopenfilename(title = "Select point cloud file (.LAS or .LAZ)",filetypes = [("LAS files","*.las"),("LAZ files","*.laz")])
#las_raw_file="E:/Palancia/_Canas/PRUEBA_DATOS_PNOA/1_Raw_Files/PNOA_2015_VAL_726-4400_ORT-CLA-RGB.laz"

Raw_Files=dirname+"1_Raw_Files/"
if not os.path.exists(Raw_Files):
    os.makedirs(Raw_Files)
    
Individual_SHP=Raw_Files+"Individual_SHP/"
if not os.path.exists(Individual_SHP):
    os.makedirs(Individual_SHP)

Photogrammetry_Clip=dirname+"2_Photogrammetry_Clip/"
if not os.path.exists(Photogrammetry_Clip):
    os.makedirs(Photogrammetry_Clip)

Ground=dirname+"3_Ground/"
if not os.path.exists(Ground):
    os.makedirs(Ground)

MDT=dirname+"4_MDT/"
if not os.path.exists(MDT):
    os.makedirs(MDT)

NormalizedClouds=dirname+"5_Normalized_Clouds/"
if not os.path.exists(NormalizedClouds):
    os.makedirs(NormalizedClouds)

ClippedFolder=dirname+"6_Normalized_Clouds_Clipped/"
if not os.path.exists(ClippedFolder):
    os.makedirs(ClippedFolder)

Cloud_Metrics=dirname+"7_CloudMetrics/"
if not os.path.exists(Cloud_Metrics):
    os.makedirs(Cloud_Metrics)



#Create Buffer
distancebuffer = float(input("Introduce distance of analysis: "))
createBuffer(shp_file, Raw_Files+"shp_file_buffer.shp", distancebuffer)
shp_file_Buffer = Raw_Files+"shp_file_buffer.shp"

#Create 1 SHP per entity
DivideSHP (shp_file,Individual_SHP)

print ("Clipping the point cloud...")

LAS2CLIP(las_raw_file,shp_file_Buffer,Photogrammetry_Clip+"Canas_clip.las")

print ("Clip finished.")


#Diccionario vacio para incluir los nombres y rutas de los ficheros
diccFilesTLS = {}
  
#Lista con todos los ficheros del directorio:
lstDir = os.walk(Photogrammetry_Clip)
  
#Crea un diccionario de los ficheros las que existen en el directorio y los incluye al diccionario
for root, dirs, files in lstDir:
    for fichero in files:
        (nombreFichero, extension) = os.path.splitext(fichero)
        if(extension == ".las"):
            diccFilesTLS.update({nombreFichero:Photogrammetry_Clip+nombreFichero+extension})
print ("Number of UAV files = ", len(diccFilesTLS))

if os.path.exists(Cloud_Metrics+"Statistics_summary.csv"):
    os.remove(Cloud_Metrics+"Statistics_summary.csv")
resultcsv=open(Cloud_Metrics+"Statistics_summary.csv","a")

filenumber=1
#Recorre los ficheros TLS
for FileNameTLS,PathTLS in diccFilesTLS.items():
  
    LAS2GROUND(Photogrammetry_Clip+FileNameTLS+".las",Ground+FileNameTLS+"_ground.las")
   
    LAS2RASTER(Ground+FileNameTLS+"_ground.las",MDT+FileNameTLS+"_ground.mdt")
   
    LAS2HEIGHTS(Photogrammetry_Clip+FileNameTLS+".las",Ground+FileNameTLS+"_ground.las",NormalizedClouds+FileNameTLS+"_Normalized.las"," -replace_z -drop_below -0.005")
 
    LAS2CLIP(NormalizedClouds+FileNameTLS+"_Normalized.las",Individual_SHP+"Polygon"+FileNameTLS[-6:]+".shp",ClippedFolder+FileNameTLS+"_Normalized_Clipped.las")
     
    LASCLOUDMETRICS(ClippedFolder+FileNameTLS+"_Normalized_Clipped_000000.las ",Cloud_Metrics+FileNameTLS+".csv ")


    f = open(Cloud_Metrics+FileNameTLS+".csv")
    if filenumber!=1:
        next(f) # skip the header
        for line in f:
            resultcsv.write(line)
        f.close() # not really needed
    else:
        for line in f:
            resultcsv.write(line)
        f.close() # not really needed
    filenumber=filenumber+1
    os.remove(Cloud_Metrics+FileNameTLS+".csv")
resultcsv.close()



