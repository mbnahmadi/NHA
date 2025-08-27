begin

  ;;;---> Reading coordinate values

  config_file = "Location-config.txt"  ;Text file containing coordinates values
  Coordinates = readAsciiTable("Location-config.txt", 4, "float", 1)

  start_lat       = Coordinates(0,0)
  end_lat         = Coordinates(0,1)
  start_lon       = Coordinates(0,2)
  end_lon         = Coordinates(0,3)


  ;;;---> Setting the directory path to read file

  path_config_file = "path-config-file-d01.txt"

; the first line of the text file to get the path to the WRF output file

  wrfoutput_file_path = asciiread("./path-config-file-d01.txt", -1, "string")
  printVarSummary(wrfoutput_file_path)

  
  a = addfile(wrfoutput_file_path, "r")

  date = wrf_user_getvar(a,"times",-1)
  print(date)


  ;;;---> Importing variables from the file

  lats  = wrf_user_getvar(a,"lat",0)
  lons  = wrf_user_getvar(a,"lon",0)
  z     = wrf_user_getvar(a,"z"  ,0)          ; grid point height
  printVarSummary(z)


  ;;;---> Setting color map and workstation

  ;dirOut = "/home/Mobin/OUTPUT/WRF01/WRF01_crossSection/WRF_d01"

  color_maps = (/"OceanLakeLandSnow","WhiteGreen","wh-bl-gr-ye-re","NCV_jet"/)
  wks = gsn_open_wks("png", dirOut +  "/wrfout_d01_" + date)
  plot = new(3,graphic)

  opt                                = True
  opt@latlon                         = True
  opt@linecoords                     = True  
  opt@autolevels                     = 80 
  opt@file_handle                    = a

  mpres                   	     = True
  mpres@gsnDraw              	     = False
  mpres@gsnFrame             	     = False 
  
  mpres@mpFillOn                     = True
  mpres@mpOceanFillColor             = "lightblue"
  mpres@mpLandFillColor              = "transparent"
  mpres@mpInlandWaterFillColor       = "lightblue"

  mpres@mpOutlineOn                  = True
  mpres@mpOutlineBoundarySets        = "AllBoundaries"    ; turn on states
  mpres@mpDataBaseVersion            = "MediumRes"        ; select database
  mpres@mpDataSetName                = "Earth..4"
  mpres@mpFillDrawOrder              = "PreDraw"

  mpres@pmTickMarkDisplayMode        = "Always"           ; Better ticmkark labels
  mpres@mpGeophysicalLineColor       = "Black"
  mpres@mpNationalLineColor          = "Black" 

  mpres@gsnCenterString              = "Cross section location"
  mpres@vpWidthF                     = 0.27
  mpres@vpHeightF                    = 0.25
  mpres@gsnStringFontHeightF         = 0.01
  mpres@tmXBLabelFontHeightF         = 0.0025


  mpres   = wrf_map_resources(a,mpres)                    ; Use WRF map projection
  plot(0) = gsn_csm_map(wks,mpres)


  ;;;---> Adding lat/lon interpolated line to plot

  mkres                             = True
  mkres@gsLineColor                 = "NavyBlue"
  mkres@gsLineThicknessF            = 10.0

  Line = wrf_user_interp_line(z,(/start_lon,start_lat,end_lon,end_lat/),opt)
  id   = gsn_add_polyline(wks,plot(0),Line@lons,Line@lats,mkres)
  ;;;-------------------------------------------------------------------


  rh = wrf_user_getvar(a, "rh",0)
  printVarSummary(rh)

  rh_latlon = wrf_user_vert_cross(rh,z,(/start_lon,start_lat,end_lon,end_lat/),opt)
 

  res                               = True
  res@gsnDraw                       = False
  res@gsnFrame                      = False

  res@cnFillOn                      = True              ; turn on contour fill
  res@cnLinesOn                     = True             ; turn off contour lines
  res@cnLineLabelsOn                = True             ; turn off line labels
  res@tiYAxisString                 = "Height (m)"
  res@tiYAxisFontHeightF            = 0.009

;  res@lbOrientation                 = "Vertical"
  res@lbLabelAngleF                 = 45.
  res@lbLabelFontHeightF            = 0.0075
  res@gsnStringFontHeightF          = 0.01
  res@tmXBLabelFontHeightF          = 0.0055
  res@tmXBLabelAngleF               = 45.

  res@vpWidthF                     = 0.25
  res@vpHeightF                    = 0.25

  res@cnFillPalette                 = color_maps(1)
;  res@cnLevelSelectionMode          = "ExplicitLevels" 
;  res@cnLevel                       = (/50, 75, 80/)
;  res@cnLevelSpacingF               = 10 


  ;;;---> Explicitly set lat/lon labels for X axis

  xvalues = ispan(0,dimsizes(rh_latlon(0,:))-1,1)
  ll_step = floattointeger( dimsizes(rh_latlon(0,:)) / 4. )   ; step interval for tickmarks
  print(ll_step)

  res@tmXBMode                      = "Explicit"
  res@tmXBValues                    = xvalues(::ll_step)
  res@tmXBLabels                    = sprintf("%6.2f",rh_latlon@lats(::ll_step)) + "~S~o~N~N~C~" + \
                                      sprintf("%6.2f",rh_latlon@lons(::ll_step)) + "~S~o~N~E"

  plot(1) = gsn_csm_contour(wks,rh_latlon,res)
  ;;;--------------------------------------------------------------------


  th = wrf_user_getvar(a, "th",0)
  printVarSummary(th)

  th_latlon = wrf_user_vert_cross(th,z,(/start_lon,start_lat,end_lon,end_lat/),opt)

  res@cnLinesOn                     = True            ; turn off contour lines
  res@cnLineLabelsOn                = True            ; turn off line labels
  res@cnLevelSelectionMode          = "ManualLevels"  ; manually set cont levels
  res@cnLevelSpacingF               = 3               ; spacing
  res@cnLineThicknessF              = 1.10            ; change line thickness
  res@cnFillPalette                 = color_maps(2)

  plot(2) = gsn_csm_contour(wks,th_latlon,res)
  ;;;-------------------------------------------------------------------


  Pres  		            = True
  Pres@gsnMaximize                  = True
;  Pres@gsnPanelDebug                = True
  Pres@gsnPanelMainString           =  "Cross section from ("+start_lat+","+start_lon+ \
                                                     ") to ("+end_lat + ","+end_lon+")"
  Pres@gsnPanelMainFont             = "helvetica-bold"
  Pres@gsnPanelYWhiteSpacePercent   = 4.0
  Pres@gsnPanelXWhiteSpacePercent   = 4.5 
  Pres@gsnPanelRowSpec		    = True
  Pres@gsnPanelBottom               = 0.14
  Pres@gsnPanelFigureStrings = (/"A","B","C"/)
  gsn_panel(wks, plot, (/1,2/), Pres)

end

