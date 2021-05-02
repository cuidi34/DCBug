:: this is comment
:: %1 for repo path
:: %2 for commitID
:: %3 for outputdir
:: %4 for dict

echo making directory
mkdir %3
echo collecting diff ...
java -jar C:\Scitool\archdiff\bin\ChangeExtractor.jar %1 %2 %3 
::
echo collecting import files ...
python C:\Scitool\archdiff\bin\tool_import_list_collector.py %3\pre %4 %3\importlist1.txt
python C:\Scitool\archdiff\bin\tool_import_list_collector.py %3\curr %4 %3\importlist2.txt
::
echo merging import files ...
python C:\Scitool\archdiff\bin\tool_merge_import_list.py %3\importlist1.txt %3\importlist2.txt %3\importlist.txt
::
echo checking import files ...
java -jar C:\Scitool\archdiff\bin\FileChecker.jar %1 %2 %3
::
echo examining relations ...
java -jar C:\Scitool\archdiff\bin\depends.jar -d=%3 java %3\pre pre
java -jar C:\Scitool\archdiff\bin\depends.jar -d=%3 java %3\curr curr
::
echo summarizing relation diff ...
python C:\Scitool\archdiff\bin\tool_dep_diff.py %3
:: 
echo cleaning ...
rd /s /q %3\curr
rd /s /q %3\pre
del /f /s /q %3\importlist.txt
del /f /s /q %3\importlist1.txt
del /f /s /q %3\importlist2.txt