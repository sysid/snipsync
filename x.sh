xxx=(
    "foo"
    "bar"
)
echo "Array: ${xxx[@]}"
echo "Index: ${!xxx[@]}"
echo "Size: ${#xxx[@]}"
for el in "${xxx[@]}"; do
    echo $el
done
