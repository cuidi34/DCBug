# this is comment
# %1 for repo path
# %2 for commitID
# %3 for outputdir
# %4 for dict
echo "making directory"
mkdir $3

echo "collecting diff ..."
java -jar /home/cuidi/tool/archdiff/bin/ChangeExtractor.jar $1 $2 $3 
#
echo "collecting import files ..."
python /home/cuidi/tool/archdiff/bin/tool_import_list_collector.py $3/pre $4 $3/importlist1.txt
python /home/cuidi/tool/archdiff/bin/tool_import_list_collector.py $3/curr $4 $3/importlist2.txt
#
echo "merging import files ..."
python /home/cuidi/tool/archdiff/bin/tool_merge_import_list.py $3/importlist1.txt $3/importlist2.txt $3/importlist.txt
#
echo "checking import files ..."
java -jar /home/cuidi/tool/archdiff/bin/FileChecker.jar $1 $2 $3
#
echo "examining relations ..."
java -jar /home/cuidi/tool/archdiff/bin/depends.jar -d=$3 java $3/pre pre
java -jar /home/cuidi/tool/archdiff/bin/depends.jar -d=$3 java $3/curr curr
#
echo "summarizing relation diff ..."
python /home/cuidi/tool/archdiff/bin/tool_dep_diff.py $3
# 
echo "cleaning ..."
rm -rf $3/curr
rm -rf $3/pre
rm $3/importlist.txt
rm $3/importlist1.txt
rm $3/importlist2.txt
