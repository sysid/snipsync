filename=$(basename -- "$fullfile")
extension="${filename##*.}"
filename="${filename%.*}"

xxx

filename=$(basename -- "$fullfile")
extension="${filename##*.}"
filename="${filename%.*}"
suffix

${1:arr}=(
	"foo"
	"bar"
)
echo "Array: ${${0:$1}[@]}"
echo "Index: ${!${0:$1}[@]}"
echo "Size: ${#${0:$1}[@]}"
for el in "${${0:$1}[@]}"; do
	echo $el
done
