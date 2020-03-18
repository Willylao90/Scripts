python waf distclean && ^
python waf configure --product=%1 --environment=unit --build-type=debug makeproj
if NOT [%2]==[] goto end
start M0.uvproj.lnk && ^
start M4.uvproj.lnk
:end